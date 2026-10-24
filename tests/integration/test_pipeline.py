"""
Integration test cho toàn bộ luồng ETL: Validate -> Transform -> Load
"""

import pandas as pd
from etl.validate import validate_data
from etl.transform import transform_data
from etl.load import load_warehouse_data


def test_end_to_end_pipeline_flow(mock_raw_data, in_memory_db):
    # 1. Validate
    cleaned, logs, stats = validate_data(mock_raw_data)
    assert len(cleaned["orders"]) == 2
    assert stats["rows_rejected"] == 0

    # 2. Transform
    star_schema = transform_data(cleaned)
    assert "fact_orders" in star_schema
    assert "fact_returns" in star_schema

    # 3. Load vào DB
    summary = load_warehouse_data(star_schema, engine=in_memory_db)
    assert summary["fact_orders"] == 2
    assert summary["fact_returns"] == 1
