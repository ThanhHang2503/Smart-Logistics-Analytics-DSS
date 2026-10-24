"""
Module: load.py
Mô tả: Nạp dữ liệu vào Staging và Star Schema Warehouse (PostgreSQL / SQLite).
       Bảo đảm tính Idempotent (chạy lại an toàn không sinh bản ghi trùng hay xung đột khóa).
Tuân thủ:
  - Hiến pháp Dự án (.specify/memory/constitution.md) - Section 5.1 (Idempotent Loading BẤT BIẾN)
  - Sprint 4 Specification (docs/sprint_3_4_spec.md)
"""

import os
import logging
from typing import Dict, Optional, Any
import pandas as pd
from sqlalchemy import create_engine, Engine, text
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


def get_db_engine() -> Engine:
    """Khởi tạo Engine kết nối Database (PostgreSQL hoặc SQLite fallback)"""
    use_sqlite = os.getenv("USE_SQLITE_FALLBACK", "false").lower() == "true"
    if use_sqlite:
        sqlite_path = os.getenv("SQLITE_DB_PATH", "data/sladss_local.db")
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        return create_engine(f"sqlite:///{sqlite_path}")

    db_user = os.getenv("DB_USER", "sladss_user")
    db_pass = os.getenv("DB_PASSWORD", "sladss_password")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "sladss_db")
    url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    return create_engine(url)


def load_staging_data(
    cleaned_data: Dict[str, pd.DataFrame],
    engine: Optional[Engine] = None,
) -> Dict[str, int]:
    """
    Nạp dữ liệu vào các bảng Staging tác nghiệp (schema 'staging').
    Áp dụng cơ chế TRUNCATE & RELOAD để bảo đảm tính Idempotent.
    """
    if engine is None:
        engine = get_db_engine()

    is_sqlite = engine.dialect.name == "sqlite"
    schema = None if is_sqlite else "staging"
    loaded_summary: Dict[str, int] = {}

    logger.info("Bắt đầu nạp Staging tables (Schema: %s, Idempotent: TRUNCATE & RELOAD)...", schema)

    with engine.begin() as conn:
        for table_name, df in cleaned_data.items():
            if df.empty:
                continue
            
            # Tên bảng trong staging: orders, shipments, returns, return_costs, products, regions, carriers
            target_table = table_name

            # Truncate trước khi nạp để bảo đảm idempotent
            try:
                if is_sqlite:
                    conn.execute(text(f"DELETE FROM {target_table}"))
                else:
                    conn.execute(text(f"TRUNCATE TABLE staging.{target_table} CASCADE"))
            except Exception as tr_err:
                logger.debug("Không thể truncate bảng '%s' (có thể chưa tồn tại): %s", target_table, str(tr_err))

            # Nạp dữ liệu
            df.to_sql(
                name=target_table,
                con=conn,
                schema=schema,
                if_exists="append",
                index=False,
            )
            loaded_summary[target_table] = len(df)
            logger.info("Đã nạp Staging '%s': %d dòng.", target_table, len(df))

    return loaded_summary


def load_warehouse_data(
    star_schema: Dict[str, pd.DataFrame],
    engine: Optional[Engine] = None,
) -> Dict[str, int]:
    """
    Nạp dữ liệu vào các bảng Warehouse Star Schema (schema 'warehouse').
    Áp dụng cơ chế TRUNCATE & RELOAD theo đúng thứ tự (Facts trước, Dims sau) để bảo toàn khóa ngoại.
    """
    if engine is None:
        engine = get_db_engine()

    is_sqlite = engine.dialect.name == "sqlite"
    schema = None if is_sqlite else "warehouse"
    loaded_summary: Dict[str, int] = {}

    logger.info("Bắt đầu nạp Warehouse Star Schema (Schema: %s)...", schema)

    # Thứ tự nạp: Dims trước, Facts sau
    dim_order = ["dim_date", "dim_product", "dim_region", "dim_carrier", "dim_return_reason"]
    fact_order = ["fact_orders", "fact_shipments", "fact_returns", "fact_return_costs"]

    with engine.begin() as conn:
        # Xóa dữ liệu cũ theo thứ tự ngược: Facts trước, Dims sau
        for t in reversed(fact_order + dim_order):
            if t in star_schema:
                try:
                    if is_sqlite:
                        conn.execute(text(f"DELETE FROM {t}"))
                    else:
                        conn.execute(text(f"TRUNCATE TABLE warehouse.{t} CASCADE"))
                except Exception as del_err:
                    logger.debug("Không thể truncate bảng '%s': %s", t, str(del_err))

        # Nạp Dims
        for t in dim_order:
            if t in star_schema and not star_schema[t].empty:
                df = star_schema[t]
                df.to_sql(name=t, con=conn, schema=schema, if_exists="append", index=False)
                loaded_summary[t] = len(df)
                logger.info("Đã nạp Dimension '%s': %d dòng.", t, len(df))

        # Nạp Facts
        for t in fact_order:
            if t in star_schema and not star_schema[t].empty:
                df = star_schema[t]
                df.to_sql(name=t, con=conn, schema=schema, if_exists="append", index=False)
                loaded_summary[t] = len(df)
                logger.info("Đã nạp Fact '%s': %d dòng.", t, len(df))

    return loaded_summary


def load_quality_logs(
    quality_logs_df: pd.DataFrame,
    engine: Optional[Engine] = None,
) -> int:
    """
    Ghi nhận toàn bộ bản ghi vi phạm QC vào bảng staging.data_quality_log (Append mode).
    """
    if quality_logs_df.empty:
        return 0

    if engine is None:
        engine = get_db_engine()

    is_sqlite = engine.dialect.name == "sqlite"
    schema = None if is_sqlite else "staging"

    logger.info("Nạp %d bản ghi vi phạm vào data_quality_log...", len(quality_logs_df))
    try:
        quality_logs_df.to_sql(
            name="data_quality_log",
            con=engine,
            schema=schema,
            if_exists="append",
            index=False,
        )
        return len(quality_logs_df)
    except Exception as e:
        logger.error("Lỗi khi ghi data_quality_log: %s", str(e))
        return 0


def load_data(
    tables: Dict[str, pd.DataFrame],
    schema: Optional[str] = None,
    engine: Optional[Engine] = None,
    if_exists: str = "replace",
) -> Dict[str, int]:
    """Hàm nạp dữ liệu đa năng tương thích ngược"""
    if engine is None:
        engine = get_db_engine()

    is_sqlite = engine.dialect.name == "sqlite"
    target_schema = None if is_sqlite else schema
    summary = {}

    for table_name, df in tables.items():
        df.to_sql(
            name=table_name,
            con=engine,
            schema=target_schema,
            if_exists=if_exists,
            index=False,
        )
        summary[table_name] = len(df)

    return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    eng = create_engine("sqlite:///:memory:")
    t_df = {"test_tbl": pd.DataFrame({"id": [1, 2], "val": ["A", "B"]})}
    res = load_data(t_df, engine=eng)
    print("Test loaded:", res)
