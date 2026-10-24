"""
Fixtures dùng chung cho kiểm thử Pytest
"""

import pytest
import pandas as pd
from sqlalchemy import create_engine


@pytest.fixture
def mock_raw_data():
    """Tập dữ liệu mẫu tối thiểu phục vụ unit test và integration test"""
    carriers = pd.DataFrame([{"carrier_id": "VNPOST", "carrier_name": "VNPost"}])
    products = pd.DataFrame([{"product_id": "PRD_001", "category": "Electronics", "product_name": "Tai nghe"}])
    regions = pd.DataFrame([{"region_id": "REG_NORTH", "region_name": "Miền Bắc", "province_or_area": "Hà Nội"}])

    orders = pd.DataFrame(
        [
            {
                "order_id": "ORD_001",
                "order_date": "2026-03-01",
                "customer_key": "CUST_001",
                "product_id": "PRD_001",
                "region_id": "REG_NORTH",
                "carrier_id": "VNPOST",
                "order_value": 500000.0,
            },
            {
                "order_id": "ORD_002",
                "order_date": "2026-03-02",
                "customer_key": "CUST_002",
                "product_id": "PRD_001",
                "region_id": "REG_NORTH",
                "carrier_id": "VNPOST",
                "order_value": 300000.0,
            },
        ]
    )
    returns = pd.DataFrame(
        [
            {
                "return_id": "RET_001",
                "order_id": "ORD_001",
                "return_date": "2026-03-05",
                "return_reason": "Damaged",
                "return_status": "completed",
            }
        ]
    )
    return_costs = pd.DataFrame(
        [
            {
                "cost_id": "CST_001",
                "return_id": "RET_001",
                "cost_type": "Shipping",
                "amount": 35000.0,
                "currency": "VND",
            }
        ]
    )
    return {
        "carriers": carriers,
        "products": products,
        "regions": regions,
        "orders": orders,
        "returns": returns,
        "return_costs": return_costs,
    }


@pytest.fixture
def in_memory_db():
    """SQLite in-memory engine phục vụ test load và query không cần kết nối network"""
    return create_engine("sqlite:///:memory:")
