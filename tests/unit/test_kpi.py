"""
Unit tests cho các công thức tính chỉ số KPI cốt lõi
Tuân thủ: Section 4.3 & 9 của Hiến pháp Dự án
"""

import pytest
import pandas as pd


def calculate_return_rate(total_orders: int, returned_orders: int) -> float:
    """Hàm phụ trợ tính tỷ lệ hoàn trả"""
    if total_orders == 0:
        return 0.0
    return round((returned_orders / total_orders) * 100, 2)


def test_calculate_return_rate_normal():
    rate = calculate_return_rate(100, 15)
    assert rate == 15.0


def test_calculate_return_rate_zero_orders():
    rate = calculate_return_rate(0, 0)
    assert rate == 0.0


def test_no_fanout_join_simulation():
    """Kiểm tra nguyên tắc chống fanout khi tổng hợp đa grain"""
    # 1 Order có 2 khoản chi phí
    orders = pd.DataFrame([{"order_id": "ORD_1", "order_value": 1000.0}])
    costs = pd.DataFrame([
        {"order_id": "ORD_1", "cost": 50.0},
        {"order_id": "ORD_1", "cost": 70.0},
    ])

    # Tổng hợp costs trước khi merge
    agg_costs = costs.groupby("order_id", as_index=False)["cost"].sum()
    merged = orders.merge(agg_costs, on="order_id", how="left")

    assert len(merged) == 1
    assert merged.loc[0, "order_value"] == 1000.0
    assert merged.loc[0, "cost"] == 120.0
