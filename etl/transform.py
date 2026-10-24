"""
Module: transform.py
Mô tả: Chuyển đổi dữ liệu sạch sang mô hình Data Warehouse Star Schema.
       Bảo toàn nguyên tắc Grain và tạo surrogate keys chuẩn hóa.
Tuân thủ:
  - Hiến pháp Dự án (.specify/memory/constitution.md) - Section 4.2 (Grain Integrity BẤT BIẾN)
  - Sprint 4 Specification (docs/sprint_3_4_spec.md)
"""

import logging
from typing import Dict, Tuple
import pandas as pd

logger = logging.getLogger(__name__)


def transform_data(cleaned_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Chuyển đổi dữ liệu đã làm sạch sang 5 Dimension tables và 4 Fact tables của Star Schema.
    Đồng thời chuẩn bị các bảng Staging tương ứng để nạp vào cơ sở dữ liệu.

    :param cleaned_data: Dict các DataFrame đã được kiểm tra chất lượng.
    :return: Dict[tên_bảng, DataFrame] chứa toàn bộ các bảng Dimensions và Facts.
    """
    logger.info("Bắt đầu chuyển đổi dữ liệu sang mô hình Star Schema chuẩn Grain...")
    star_schema: Dict[str, pd.DataFrame] = {}

    # ==========================================================================
    # 1. Dimension Tables
    # ==========================================================================

    # 1.1 dim_product
    product_map = {}
    if "products" in cleaned_data and not cleaned_data["products"].empty:
        df_p = cleaned_data["products"].copy()
        df_p["product_key"] = range(1, len(df_p) + 1)
        star_schema["dim_product"] = df_p
        product_map = dict(zip(df_p["product_id"], df_p["product_key"]))

    # 1.2 dim_region
    region_map = {}
    if "regions" in cleaned_data and not cleaned_data["regions"].empty:
        df_r = cleaned_data["regions"].copy()
        df_r["region_key"] = range(1, len(df_r) + 1)
        star_schema["dim_region"] = df_r
        region_map = dict(zip(df_r["region_id"], df_r["region_key"]))

    # 1.3 dim_carrier
    carrier_map = {}
    if "carriers" in cleaned_data and not cleaned_data["carriers"].empty:
        df_c = cleaned_data["carriers"].copy()
        df_c["carrier_key"] = range(1, len(df_c) + 1)
        star_schema["dim_carrier"] = df_c
        carrier_map = dict(zip(df_c["carrier_id"], df_c["carrier_key"]))

    # 1.4 dim_return_reason
    reason_map = {}
    if "returns" in cleaned_data and "return_reason" in cleaned_data["returns"].columns:
        unique_reasons = sorted(
            cleaned_data["returns"]["return_reason"].dropna().astype(str).unique().tolist()
        )
        df_reason = pd.DataFrame({"return_reason": unique_reasons})
        df_reason["reason_key"] = range(1, len(df_reason) + 1)
        star_schema["dim_return_reason"] = df_reason
        reason_map = dict(zip(df_reason["return_reason"], df_reason["reason_key"]))

    # 1.5 dim_date (Tập hợp toàn bộ ngày từ Orders, Shipments, Returns)
    dates_set = set()
    if "orders" in cleaned_data and "order_date" in cleaned_data["orders"].columns:
        dates_set.update(pd.to_datetime(cleaned_data["orders"]["order_date"], errors="coerce").dropna().dt.date)
    
    if "shipments" in cleaned_data:
        if "shipped_at" in cleaned_data["shipments"].columns:
            dates_set.update(pd.to_datetime(cleaned_data["shipments"]["shipped_at"], errors="coerce").dropna().dt.date)
        if "delivered_at" in cleaned_data["shipments"].columns:
            dates_set.update(pd.to_datetime(cleaned_data["shipments"]["delivered_at"], errors="coerce").dropna().dt.date)

    if "returns" in cleaned_data and "return_date" in cleaned_data["returns"].columns:
        dates_set.update(pd.to_datetime(cleaned_data["returns"]["return_date"], errors="coerce").dropna().dt.date)

    if dates_set:
        sorted_dates = sorted(list(dates_set))
        df_dates = pd.DataFrame({"date": sorted_dates})
        df_dates["date"] = pd.to_datetime(df_dates["date"])
        df_dates["date_key"] = df_dates["date"].dt.strftime("%Y%m%d").astype(int)
        df_dates["day"] = df_dates["date"].dt.day
        df_dates["month"] = df_dates["date"].dt.month
        df_dates["quarter"] = df_dates["date"].dt.quarter
        df_dates["year"] = df_dates["date"].dt.year
        df_dates["day_of_week"] = df_dates["date"].dt.dayofweek + 1
        df_dates["day_name"] = df_dates["date"].dt.day_name()
        df_dates["month_name"] = df_dates["date"].dt.month_name()
        df_dates["is_weekend"] = df_dates["day_of_week"].isin([6, 7])
        df_dates["date"] = df_dates["date"].dt.date
        star_schema["dim_date"] = df_dates

    # ==========================================================================
    # 2. Fact Tables (Bảo toàn mức chi tiết Grain)
    # ==========================================================================

    # 2.1 fact_orders: 1 dòng = 1 đơn hàng (Grain: 1 row / order)
    order_key_map = {}
    if "orders" in cleaned_data and not cleaned_data["orders"].empty:
        df_fo = cleaned_data["orders"].copy()
        df_fo["order_key"] = range(1, len(df_fo) + 1)
        order_key_map = dict(zip(df_fo["order_id"], df_fo["order_key"]))

        df_fo["order_date_key"] = (
            pd.to_datetime(df_fo["order_date"], errors="coerce")
            .dt.strftime("%Y%m%d")
            .fillna(19000101)
            .astype(int)
        )
        df_fo["product_key"] = (
            df_fo["product_id"].map(product_map).fillna(1).astype(int)
            if "product_id" in df_fo.columns
            else 1
        )
        df_fo["region_key"] = (
            df_fo["region_id"].map(region_map).fillna(1).astype(int)
            if "region_id" in df_fo.columns
            else 1
        )
        df_fo["carrier_key"] = (
            df_fo["carrier_id"].map(carrier_map).fillna(1).astype(int)
            if "carrier_id" in df_fo.columns
            else 1
        )
        
        # Giữ đúng các cột định nghĩa trong DDL
        star_schema["fact_orders"] = df_fo[[
            "order_key",
            "order_id",
            "order_date_key",
            "customer_key",
            "product_key",
            "region_key",
            "carrier_key",
            "order_value",
        ]]

    # 2.2 fact_shipments: 1 dòng = 1 lần giao hàng (Grain: 1 row / shipment)
    if "shipments" in cleaned_data and not cleaned_data["shipments"].empty:
        df_fs = cleaned_data["shipments"].copy()
        # Chỉ giữ shipments tham chiếu đến orders đã có trong fact_orders
        df_fs = df_fs[df_fs["order_id"].isin(order_key_map)].copy()
        
        df_fs["shipment_key"] = range(1, len(df_fs) + 1)
        df_fs["order_key"] = df_fs["order_id"].map(order_key_map).astype(int)
        df_fs["carrier_key"] = df_fs["carrier_id"].map(carrier_map).fillna(1).astype(int)

        df_fs["shipped_date_key"] = (
            pd.to_datetime(df_fs["shipped_at"], errors="coerce")
            .dt.strftime("%Y%m%d")
            .fillna(19000101)
            .astype(int)
        )
        df_fs["delivered_date_key"] = (
            pd.to_datetime(df_fs["delivered_at"], errors="coerce")
            .dt.strftime("%Y%m%d")
            .fillna(19000101)
            .astype(int)
        )

        star_schema["fact_shipments"] = df_fs[[
            "shipment_key",
            "shipment_id",
            "order_key",
            "carrier_key",
            "shipped_date_key",
            "delivered_date_key",
            "delivery_status",
            "delivery_attempts",
        ]]

    # 2.3 fact_returns: 1 dòng = 1 sự kiện hoàn hàng (Grain: 1 row / return event)
    return_key_map = {}
    if "returns" in cleaned_data and not cleaned_data["returns"].empty:
        df_fr = cleaned_data["returns"].copy()
        df_fr = df_fr[df_fr["order_id"].isin(order_key_map)].copy()

        df_fr["return_key"] = range(1, len(df_fr) + 1)
        return_key_map = dict(zip(df_fr["return_id"], df_fr["return_key"]))

        df_fr["order_key"] = df_fr["order_id"].map(order_key_map).astype(int)
        df_fr["return_date_key"] = (
            pd.to_datetime(df_fr["return_date"], errors="coerce")
            .dt.strftime("%Y%m%d")
            .fillna(19000101)
            .astype(int)
        )
        df_fr["reason_key"] = df_fr["return_reason"].map(reason_map).fillna(1).astype(int)

        star_schema["fact_returns"] = df_fr[[
            "return_key",
            "return_id",
            "order_key",
            "return_date_key",
            "reason_key",
            "return_status",
        ]]

    # 2.4 fact_return_costs: 1 dòng = 1 khoản chi phí phát sinh (Grain: 1 row / cost item)
    if "return_costs" in cleaned_data and not cleaned_data["return_costs"].empty:
        df_frc = cleaned_data["return_costs"].copy()
        df_frc = df_frc[df_frc["return_id"].isin(return_key_map)].copy()

        df_frc["cost_key"] = range(1, len(df_frc) + 1)
        df_frc["return_key"] = df_frc["return_id"].map(return_key_map).astype(int)
        df_frc["cost_amount"] = df_frc["amount"]

        star_schema["fact_return_costs"] = df_frc[[
            "cost_key",
            "cost_id",
            "return_key",
            "cost_type",
            "cost_amount",
            "currency",
        ]]

    logger.info("Hoàn tất chuyển đổi Star Schema: %d bảng Facts & Dimensions sẵn sàng.", len(star_schema))
    return star_schema


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample = {
        "products": pd.DataFrame([{"product_id": "P1", "category": "C", "product_name": "N"}]),
        "regions": pd.DataFrame([{"region_id": "R1", "region_name": "N", "province_or_area": "A"}]),
        "carriers": pd.DataFrame([{"carrier_id": "C1", "carrier_name": "N"}]),
        "orders": pd.DataFrame([{
            "order_id": "O1", "order_date": "2026-03-01", "customer_key": "CK",
            "product_id": "P1", "region_id": "R1", "carrier_id": "C1", "order_value": 1000
        }]),
    }
    res = transform_data(sample)
    print("Star schema tables:", list(res.keys()))
