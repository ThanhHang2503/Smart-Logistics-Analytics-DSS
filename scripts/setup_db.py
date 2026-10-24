"""
Script: setup_db.py
Mô tả: Thiết lập cơ sở dữ liệu và bảng schema cho SLADSS (PostgreSQL hoặc SQLite fallback).
Tuân thủ: Section 4 và Section 8.2 của Hiến pháp Dự án (.specify/memory/constitution.md)
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def setup_database():
    """Khởi tạo database schema từ file sql/ddl/init_schema.sql"""
    use_sqlite = os.getenv("USE_SQLITE_FALLBACK", "false").lower() == "true"
    
    if use_sqlite:
        sqlite_path = os.getenv("SQLITE_DB_PATH", "data/sladss_local.db")
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        db_url = f"sqlite:///{sqlite_path}"
        logger.info("Khởi tạo database SQLite cục bộ tại: %s", sqlite_path)
    else:
        db_user = os.getenv("DB_USER", "sladss_user")
        db_pass = os.getenv("DB_PASSWORD", "sladss_password")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "sladss_db")
        db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        logger.info("Kết nối tới PostgreSQL: %s@%s:%s/%s", db_user, db_host, db_port, db_name)

    engine = create_engine(db_url)
    
    # Thứ tự thực thi DDL chuẩn theo Sprint 2
    ddl_files = [
        os.path.join("sql", "ddl", "01_staging_and_logs.sql"),
        os.path.join("sql", "ddl", "02_star_schema.sql"),
        os.path.join("sql", "marts", "logistics_kpi_views.sql"),
    ]
    
    # Fallback nếu chưa chia tách file
    if not any(os.path.exists(p) for p in ddl_files):
        ddl_files = [os.path.join("sql", "ddl", "init_schema.sql")]

    with engine.connect() as conn:
        for ddl_file in ddl_files:
            if not os.path.exists(ddl_file):
                logger.warning("Bỏ qua file DDL không tìm thấy: %s", ddl_file)
                continue
            
            logger.info("Thực thi kịch bản DDL: %s...", ddl_file)
            with open(ddl_file, "r", encoding="utf-8") as f:
                ddl_content = f.read()

            if use_sqlite:
                raw_statements = ddl_content.split(";")
                for raw_stmt in raw_statements:
                    lines = [line for line in raw_stmt.splitlines() if not line.strip().startswith("--")]
                    clean_stmt = "\n".join(lines).strip()
                    if not clean_stmt:
                        continue
                    if clean_stmt.upper().startswith("CREATE SCHEMA") or clean_stmt.upper().startswith("COMMENT ON"):
                        continue
                    clean_stmt = (
                        clean_stmt.replace("staging.", "")
                        .replace("warehouse.", "")
                        .replace("marts.", "")
                        .replace("CREATE OR REPLACE VIEW", "CREATE VIEW IF NOT EXISTS")
                        .replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
                        .replace("BIGSERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
                        .replace("TIMESTAMPTZ", "TIMESTAMP")
                        .replace("UUID PRIMARY KEY DEFAULT gen_random_uuid()", "TEXT PRIMARY KEY")
                        .replace("::NUMERIC", "")
                        .replace("::INT", "")
                        .replace("EXTRACT(YEAR FROM fs.created_at)", "CAST(strftime('%Y', fs.created_at) AS INT)")
                        .replace("EXTRACT(MONTH FROM fs.created_at)", "CAST(strftime('%m', fs.created_at) AS INT)")
                        .replace("(d_return.date - d_order.date)", "CAST(julianday(d_return.date) - julianday(d_order.date) AS INT)")
                    )
                    if "CREATE VIEW" in clean_stmt.upper():
                        # Đảm bảo drop view cũ nếu tồn tại
                        for v in ["v_carrier_performance", "v_monthly_product_returns", "v_return_reason_cost_breakdown", "v_reverse_logistics_cycle_time"]:
                            if v in clean_stmt:
                                try:
                                    conn.execute(text(f"DROP VIEW IF EXISTS {v}"))
                                except Exception:
                                    pass
                    try:
                        conn.execute(text(clean_stmt))
                    except Exception as ex:
                        logger.debug("Bỏ qua lệnh không tương thích SQLite trong %s: %s", ddl_file, str(ex))
                conn.commit()
            else:
                conn.execute(text(ddl_content))
                conn.commit()

    logger.info("Khởi tạo cấu trúc Database hoàn tất thành công!")


if __name__ == "__main__":
    setup_database()
