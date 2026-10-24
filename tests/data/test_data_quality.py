"""
Kiểm thử các quy tắc chất lượng dữ liệu (Data Quality Tests)
Tuân thủ:
  - Section 5.2 của Hiến pháp Dự án (.specify/memory/constitution.md)
  - Quy tắc QC-001 -> QC-005 (docs/sprint_3_4_spec.md)
"""

import pandas as pd
from etl.validate import validate_data


def test_validate_orders_with_null_and_negative():
    raw_data = {
        "carriers": pd.DataFrame([{"carrier_id": "VNPOST", "carrier_name": "VNPost"}]),
        "products": pd.DataFrame([{"product_id": "PRD_001", "category": "Elec", "product_name": "P1"}]),
        "regions": pd.DataFrame([{"region_id": "REG_NORTH", "region_name": "Bac", "province_or_area": "HN"}]),
        "orders": pd.DataFrame({
            "order_id": ["ORD_1", None, "ORD_3"],
            "order_date": ["2026-03-01", "2026-03-02", "2026-03-03"],
            "carrier_id": ["VNPOST", "VNPOST", "VNPOST"],
            "product_id": ["PRD_001", "PRD_001", "PRD_001"],
            "region_id": ["REG_NORTH", "REG_NORTH", "REG_NORTH"],
            "order_value": [500000.0, 300000.0, -100000.0],
        }),
    }

    cleaned_data, quality_logs, stats = validate_data(raw_data)

    # Dòng rỗng order_id và dòng order_value âm phải bị loại bỏ
    assert len(cleaned_data["orders"]) == 1
    assert "ORD_1" in cleaned_data["orders"]["order_id"].values

    # Vi phạm phải được ghi vào quality_logs
    rule_codes = quality_logs["rule_code"].tolist()
    assert "QC-001" in rule_codes
    assert "QC-002" in rule_codes


def test_validate_chronology_and_status_violation():
    raw_data = {
        "orders": pd.DataFrame([{
            "order_id": "ORD_10", "order_date": "2026-05-10", "order_value": 200000.0,
            "carrier_id": "VNPOST", "product_id": "PRD_001", "region_id": "REG_NORTH"
        }]),
        "shipments": pd.DataFrame([
            # Hợp lệ
            {
                "shipment_id": "SHIP_1", "order_id": "ORD_10",
                "shipped_at": "2026-05-10 10:00:00", "delivered_at": "2026-05-12 10:00:00",
                "delivery_status": "delivered", "delivery_attempts": 1
            },
            # QC-003: delivered_at < shipped_at
            {
                "shipment_id": "SHIP_2", "order_id": "ORD_10",
                "shipped_at": "2026-05-10 10:00:00", "delivered_at": "2026-05-08 10:00:00",
                "delivery_status": "delivered", "delivery_attempts": 1
            },
            # QC-004: Trạng thái không hợp lệ
            {
                "shipment_id": "SHIP_3", "order_id": "ORD_10",
                "shipped_at": "2026-05-10 10:00:00", "delivered_at": "2026-05-13 10:00:00",
                "delivery_status": "fake_unknown_status", "delivery_attempts": 1
            },
        ]),
    }

    cleaned_data, quality_logs, stats = validate_data(raw_data)
    rule_codes = quality_logs["rule_code"].tolist()
    assert "QC-003" in rule_codes
    assert "QC-004" in rule_codes
    assert len(cleaned_data["shipments"]) == 1


def test_validate_foreign_key_orphan():
    raw_data = {
        "carriers": pd.DataFrame([{"carrier_id": "VNPOST", "carrier_name": "VNPost"}]),
        "orders": pd.DataFrame([{
            "order_id": "ORD_99", "order_date": "2026-01-01", "order_value": 150000.0,
            "carrier_id": "NON_EXISTING_CARRIER"
        }]),
    }

    cleaned_data, quality_logs, stats = validate_data(raw_data)
    rule_codes = quality_logs["rule_code"].tolist()
    assert "QC-005" in rule_codes
    assert len(cleaned_data["orders"]) == 0
