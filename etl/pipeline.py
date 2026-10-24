"""
Module: pipeline.py
Mô tả: Bộ điều phối luồng ETL toàn diện (Pipeline Orchestrator).
       Quản lý toàn bộ vòng đời thực thi, từ Extract, Validate, Transform, Load
       đến việc ghi nhật ký chi tiết vào staging.pipeline_run và staging.data_quality_log.
Tuân thủ:
  - Hiến pháp Dự án (.specify/memory/constitution.md) - Section 5.3 & 5.4
  - Sprint 4 Specification (docs/sprint_3_4_spec.md)
"""

import sys
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd
from sqlalchemy import text

from etl.extract import extract_data
from etl.validate import validate_data
from etl.transform import transform_data
from etl.load import (
    get_db_engine,
    load_staging_data,
    load_warehouse_data,
    load_quality_logs,
)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("SLADSS_Pipeline")


def create_pipeline_run_record(engine, run_id: str, started_at: datetime, source_dir: str):
    """Ghi nhận bản ghi khởi tạo pipeline_run với trạng thái RUNNING"""
    is_sqlite = engine.dialect.name == "sqlite"
    schema = None if is_sqlite else "staging"
    
    df_run = pd.DataFrame([{
        "run_id": run_id,
        "source_file": source_dir,
        "started_at": started_at,
        "ended_at": None,
        "status": "RUNNING",
        "rows_read": 0,
        "rows_valid": 0,
        "rows_rejected": 0,
        "rows_loaded": 0,
        "error_detail": None,
    }])
    df_run.to_sql(
        name="pipeline_run",
        con=engine,
        schema=schema,
        if_exists="append",
        index=False,
    )


def update_pipeline_run_record(
    engine,
    run_id: str,
    ended_at: datetime,
    status: str,
    rows_read: int,
    rows_valid: int,
    rows_rejected: int,
    rows_loaded: int,
    error_detail: Optional[str] = None,
):
    """Cập nhật kết quả cuối cùng của chu trình pipeline vào pipeline_run"""
    is_sqlite = engine.dialect.name == "sqlite"
    table_name = "pipeline_run" if is_sqlite else "staging.pipeline_run"
    
    sql = text(f"""
        UPDATE {table_name}
        SET ended_at = :ended_at,
            status = :status,
            rows_read = :rows_read,
            rows_valid = :rows_valid,
            rows_rejected = :rows_rejected,
            rows_loaded = :rows_loaded,
            error_detail = :error_detail
        WHERE run_id = :run_id
    """)

    with engine.begin() as conn:
        conn.execute(
            sql,
            {
                "ended_at": ended_at,
                "status": status,
                "rows_read": rows_read,
                "rows_valid": rows_valid,
                "rows_rejected": rows_rejected,
                "rows_loaded": rows_loaded,
                "error_detail": error_detail,
                "run_id": run_id,
            },
        )


def run_pipeline(data_dir: str = "data/sample") -> Dict[str, Any]:
    """
    Hàm điều phối luồng chạy ETL end-to-end hoàn chỉnh:
      1. Khởi tạo pipeline_run (RUNNING)
      2. Extract từ CSV nguồn
      3. Validate dữ liệu & ghi log lỗi vào data_quality_log
      4. Load vào Staging tables (Idempotent TRUNCATE & RELOAD)
      5. Transform sang Star Schema (5 Dims & 4 Facts)
      6. Load vào Warehouse tables (Idempotent TRUNCATE & RELOAD)
      7. Cập nhật pipeline_run (SUCCESS / FAILED)
    """
    engine = get_db_engine()
    run_id = str(uuid.uuid4())
    started_at = datetime.now()

    logger.info("==================================================================")
    logger.info("BẮT ĐẦU CHU TRÌNH ETL PIPELINE (Run ID: %s)", run_id)
    logger.info("Thư mục nguồn dữ liệu: %s", data_dir)
    logger.info("Database Target: %s", engine.dialect.name)
    logger.info("==================================================================")

    # 1. Khởi tạo bản ghi giám sát
    try:
        create_pipeline_run_record(engine, run_id, started_at, data_dir)
    except Exception as run_err:
        logger.warning("Không thể khởi tạo bản ghi pipeline_run (có thể bảng chưa được tạo): %s", str(run_err))

    rows_read = 0
    rows_valid = 0
    rows_rejected = 0
    rows_loaded = 0

    try:
        # 2. Extract
        raw_data = extract_data(data_dir)
        if not raw_data:
            raise ValueError(f"Không tìm thấy dữ liệu hợp lệ trong thư mục '{data_dir}'")

        # 3. Validate
        cleaned_data, quality_logs_df, stats = validate_data(raw_data, run_id=run_id)
        rows_read = stats["rows_read"]
        rows_valid = stats["rows_valid"]
        rows_rejected = stats["rows_rejected"]

        # 4. Ghi nhận Data Quality Logs (Zero silent drop)
        logged_violations = load_quality_logs(quality_logs_df, engine=engine)
        logger.info("Đã lưu %d vi phạm chất lượng dữ liệu vào staging.data_quality_log", logged_violations)

        # 5. Load Staging
        staging_summary = load_staging_data(cleaned_data, engine=engine)

        # 6. Transform Star Schema
        star_schema = transform_data(cleaned_data)

        # 7. Load Warehouse
        warehouse_summary = load_warehouse_data(star_schema, engine=engine)
        rows_loaded = sum(warehouse_summary.values())

        # 8. Cập nhật trạng thái SUCCESS
        ended_at = datetime.now()
        duration = (ended_at - started_at).total_seconds()

        try:
            update_pipeline_run_record(
                engine=engine,
                run_id=run_id,
                ended_at=ended_at,
                status="SUCCESS",
                rows_read=rows_read,
                rows_valid=rows_valid,
                rows_rejected=rows_rejected,
                rows_loaded=rows_loaded,
                error_detail=None,
            )
        except Exception as upd_err:
            logger.warning("Không thể cập nhật pipeline_run: %s", str(upd_err))

        logger.info("==================================================================")
        logger.info("CHU TRÌNH ETL HOÀN TẤT THÀNH CÔNG TRONG %.2f GIÂY", duration)
        logger.info("• Tổng dòng đọc:        %d", rows_read)
        logger.info("• Dòng hợp lệ:           %d", rows_valid)
        logger.info("• Dòng lỗi ghi log:      %d (QC violations)", rows_rejected)
        logger.info("• Dòng nạp vào kho DW:   %d (Fact & Dim)", rows_loaded)
        logger.info("==================================================================")

        return {
            "run_id": run_id,
            "status": "SUCCESS",
            "duration_seconds": duration,
            "rows_read": rows_read,
            "rows_valid": rows_valid,
            "rows_rejected": rows_rejected,
            "rows_loaded": rows_loaded,
            "staging_summary": staging_summary,
            "warehouse_summary": warehouse_summary,
        }

    except Exception as e:
        ended_at = datetime.now()
        logger.error("PIPELINE THẤT BẠI: %s", str(e), exc_info=True)
        try:
            update_pipeline_run_record(
                engine=engine,
                run_id=run_id,
                ended_at=ended_at,
                status="FAILED",
                rows_read=rows_read,
                rows_valid=rows_valid,
                rows_rejected=rows_rejected,
                rows_loaded=rows_loaded,
                error_detail=str(e),
            )
        except Exception:
            pass
        raise


if __name__ == "__main__":
    result = run_pipeline()
    print("Pipeline Execution Result:")
    for k, v in result.items():
        print(f"  {k}: {v}")
