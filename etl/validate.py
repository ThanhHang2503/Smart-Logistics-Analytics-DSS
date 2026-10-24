"""
Module: validate.py
Mô tả: Kiểm tra chất lượng dữ liệu (Data Quality Checks) theo các quy tắc QC-001 -> QC-005.
       Tách biệt bản ghi sạch và bản ghi vi phạm. Ghi toàn bộ vi phạm vào staging.data_quality_log.
Tuân thủ:
  - Hiến pháp Dự án (.specify/memory/constitution.md) - Section 5.2 (Zero Silent Drop)
  - Sprint 4 Specification (docs/sprint_3_4_spec.md)
"""

import logging
import uuid
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd

logger = logging.getLogger(__name__)

# Danh mục trạng thái hợp lệ
VALID_DELIVERY_STATUSES = {"delivered", "delivery_failed", "in_transit", "returned_to_warehouse"}
VALID_RETURN_STATUSES = {"completed", "processing", "rejected", "pending"}


def validate_data(
    raw_data: Dict[str, pd.DataFrame],
    run_id: Optional[str] = None,
) -> Tuple[Dict[str, pd.DataFrame], pd.DataFrame, Dict[str, int]]:
    """
    Thực hiện kiểm tra chất lượng dữ liệu toàn diện.

    :param raw_data: Từ điển chứa các DataFrame thô từ extract.
    :param run_id: UUID của chu trình pipeline hiện tại.
    :return:
      - cleaned_data: Dict các DataFrame đã loại bỏ bản ghi lỗi logic.
      - quality_logs_df: DataFrame chứa toàn bộ bản ghi vi phạm QC để ghi vào data_quality_log.
      - stats: Thống kê {'rows_read': int, 'rows_valid': int, 'rows_rejected': int}.
    """
    logger.info("Bắt đầu kiểm tra chất lượng dữ liệu (Data Quality Validation)...")
    
    if run_id is None:
        run_id = str(uuid.uuid4())

    cleaned_data: Dict[str, pd.DataFrame] = {}
    logs: List[dict] = []
    
    total_rows_read = 0

    # --------------------------------------------------------------------------
    # 0. Nạp Master Reference Keys để kiểm tra QC-005 (Foreign Key Orphan)
    # --------------------------------------------------------------------------
    valid_carriers = set(raw_data["carriers"]["carrier_id"].dropna().unique()) if "carriers" in raw_data else set()
    valid_products = set(raw_data["products"]["product_id"].dropna().unique()) if "products" in raw_data else set()
    valid_regions = set(raw_data["regions"]["region_id"].dropna().unique()) if "regions" in raw_data else set()

    for entity in ["products", "regions", "carriers"]:
        if entity in raw_data:
            cleaned_data[entity] = raw_data[entity].copy()
            total_rows_read += len(raw_data[entity])

    # --------------------------------------------------------------------------
    # 1. Validate Orders
    # --------------------------------------------------------------------------
    valid_order_ids = set()
    order_date_map: Dict[str, pd.Timestamp] = {}

    if "orders" in raw_data:
        df_orders = raw_data["orders"].copy()
        total_rows_read += len(df_orders)
        invalid_order_indices = set()

        for idx, row in df_orders.iterrows():
            order_id = row.get("order_id")
            order_val = row.get("order_value")
            carrier_id = row.get("carrier_id")
            product_id = row.get("product_id")
            region_id = row.get("region_id")

            # QC-001: Khóa chính order_id không được NULL hoặc rỗng
            if pd.isna(order_id) or str(order_id).strip() == "" or str(order_id).lower() == "nan":
                logs.append({
                    "run_id": run_id,
                    "source_file": "orders.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-001",
                    "column_name": "order_id",
                    "raw_value": str(order_id),
                    "message": "Khóa chính order_id bị NULL hoặc rỗng",
                })
                invalid_order_indices.add(idx)
                continue

            # QC-002: Giá trị đơn hàng không được âm
            if pd.notna(order_val) and float(order_val) < 0:
                logs.append({
                    "run_id": run_id,
                    "source_file": "orders.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-002",
                    "column_name": "order_value",
                    "raw_value": str(order_val),
                    "message": f"Giá trị đơn hàng bị âm: {order_val}",
                })
                invalid_order_indices.add(idx)

            # QC-005: Khóa ngoại tham chiếu đến dimension không tồn tại
            if valid_carriers and carrier_id not in valid_carriers:
                logs.append({
                    "run_id": run_id,
                    "source_file": "orders.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-005",
                    "column_name": "carrier_id",
                    "raw_value": str(carrier_id),
                    "message": f"Mã carrier_id '{carrier_id}' không tồn tại trong danh mục carriers",
                })
                invalid_order_indices.add(idx)

            if valid_products and product_id not in valid_products:
                logs.append({
                    "run_id": run_id,
                    "source_file": "orders.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-005",
                    "column_name": "product_id",
                    "raw_value": str(product_id),
                    "message": f"Mã product_id '{product_id}' không tồn tại trong danh mục products",
                })
                invalid_order_indices.add(idx)

            if valid_regions and region_id not in valid_regions:
                logs.append({
                    "run_id": run_id,
                    "source_file": "orders.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-005",
                    "column_name": "region_id",
                    "raw_value": str(region_id),
                    "message": f"Mã region_id '{region_id}' không tồn tại trong danh mục regions",
                })
                invalid_order_indices.add(idx)

        # Lọc bỏ đơn hàng lỗi và lưu thông tin đơn hàng hợp lệ
        clean_orders = df_orders.drop(index=list(invalid_order_indices)).copy()
        cleaned_data["orders"] = clean_orders
        valid_order_ids = set(clean_orders["order_id"].dropna().unique())
        
        # Lưu map order_date phục vụ kiểm tra QC-003 cho return
        for _, r in clean_orders.iterrows():
            order_date_map[r["order_id"]] = pd.to_datetime(r["order_date"], errors="coerce")

    # --------------------------------------------------------------------------
    # 2. Validate Shipments
    # --------------------------------------------------------------------------
    if "shipments" in raw_data:
        df_shipments = raw_data["shipments"].copy()
        total_rows_read += len(df_shipments)
        invalid_shipment_indices = set()

        for idx, row in df_shipments.iterrows():
            shipment_id = row.get("shipment_id")
            order_id = row.get("order_id")
            shipped_at = pd.to_datetime(row.get("shipped_at"), errors="coerce")
            delivered_at = pd.to_datetime(row.get("delivered_at"), errors="coerce")
            status = row.get("delivery_status")

            # QC-001: Khóa chính shipment_id NULL
            if pd.isna(shipment_id) or str(shipment_id).strip() == "" or str(shipment_id).lower() == "nan":
                logs.append({
                    "run_id": run_id,
                    "source_file": "shipments.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-001",
                    "column_name": "shipment_id",
                    "raw_value": str(shipment_id),
                    "message": "Khóa chính shipment_id bị NULL hoặc rỗng",
                })
                invalid_shipment_indices.add(idx)
                continue

            # QC-005: Khóa ngoại order_id không tồn tại trong orders hợp lệ
            if order_id not in valid_order_ids:
                logs.append({
                    "run_id": run_id,
                    "source_file": "shipments.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-005",
                    "column_name": "order_id",
                    "raw_value": str(order_id),
                    "message": f"Mã order_id '{order_id}' không tồn tại hoặc đã bị loại bỏ do lỗi",
                })
                invalid_shipment_indices.add(idx)

            # QC-003: Thứ tự thời gian delivered_at < shipped_at
            if pd.notna(shipped_at) and pd.notna(delivered_at) and delivered_at < shipped_at:
                logs.append({
                    "run_id": run_id,
                    "source_file": "shipments.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-003",
                    "column_name": "delivered_at",
                    "raw_value": f"delivered_at={delivered_at} < shipped_at={shipped_at}",
                    "message": "Thời gian giao hàng (delivered_at) diễn ra trước thời gian gửi hàng (shipped_at)",
                })
                invalid_shipment_indices.add(idx)

            # QC-004: Trạng thái nằm ngoài danh mục định nghĩa
            if pd.isna(status) or str(status).lower() not in VALID_DELIVERY_STATUSES:
                logs.append({
                    "run_id": run_id,
                    "source_file": "shipments.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-004",
                    "column_name": "delivery_status",
                    "raw_value": str(status),
                    "message": f"Trạng thái giao hàng '{status}' không hợp lệ (không thuộc danh mục cho phép)",
                })
                invalid_shipment_indices.add(idx)

        cleaned_data["shipments"] = df_shipments.drop(index=list(invalid_shipment_indices)).copy()

    # --------------------------------------------------------------------------
    # 3. Validate Returns
    # --------------------------------------------------------------------------
    valid_return_ids = set()

    if "returns" in raw_data:
        df_returns = raw_data["returns"].copy()
        total_rows_read += len(df_returns)
        invalid_return_indices = set()

        for idx, row in df_returns.iterrows():
            return_id = row.get("return_id")
            order_id = row.get("order_id")
            return_date = pd.to_datetime(row.get("return_date"), errors="coerce")
            return_status = row.get("return_status")

            # QC-001: Khóa chính return_id NULL
            if pd.isna(return_id) or str(return_id).strip() == "" or str(return_id).lower() == "nan":
                logs.append({
                    "run_id": run_id,
                    "source_file": "returns.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-001",
                    "column_name": "return_id",
                    "raw_value": str(return_id),
                    "message": "Khóa chính return_id bị NULL hoặc rỗng",
                })
                invalid_return_indices.add(idx)
                continue

            # QC-005: Khóa ngoại order_id không tồn tại trong orders hợp lệ
            if order_id not in valid_order_ids:
                logs.append({
                    "run_id": run_id,
                    "source_file": "returns.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-005",
                    "column_name": "order_id",
                    "raw_value": str(order_id),
                    "message": f"Mã order_id '{order_id}' trong returns không tồn tại trong orders hợp lệ",
                })
                invalid_return_indices.add(idx)

            # QC-003: Ngày hoàn trước ngày tạo đơn
            if order_id in order_date_map and pd.notna(return_date):
                ord_date = order_date_map[order_id]
                if pd.notna(ord_date) and return_date < ord_date:
                    logs.append({
                        "run_id": run_id,
                        "source_file": "returns.csv",
                        "row_number": int(idx) + 2,
                        "rule_code": "QC-003",
                        "column_name": "return_date",
                        "raw_value": f"return_date={return_date.date()} < order_date={ord_date.date()}",
                        "message": "Ngày yêu cầu hoàn trả (return_date) diễn ra trước ngày tạo đơn (order_date)",
                    })
                    invalid_return_indices.add(idx)

            # QC-004: Trạng thái hoàn không hợp lệ
            if pd.isna(return_status) or str(return_status).lower() not in VALID_RETURN_STATUSES:
                logs.append({
                    "run_id": run_id,
                    "source_file": "returns.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-004",
                    "column_name": "return_status",
                    "raw_value": str(return_status),
                    "message": f"Trạng thái hoàn trả '{return_status}' không hợp lệ",
                })
                invalid_return_indices.add(idx)

        clean_returns = df_returns.drop(index=list(invalid_return_indices)).copy()
        cleaned_data["returns"] = clean_returns
        valid_return_ids = set(clean_returns["return_id"].dropna().unique())

    # --------------------------------------------------------------------------
    # 4. Validate Return Costs
    # --------------------------------------------------------------------------
    if "return_costs" in raw_data:
        df_costs = raw_data["return_costs"].copy()
        total_rows_read += len(df_costs)
        invalid_cost_indices = set()

        for idx, row in df_costs.iterrows():
            cost_id = row.get("cost_id")
            return_id = row.get("return_id")
            amount = row.get("amount")

            # QC-001: Khóa chính cost_id NULL
            if pd.isna(cost_id) or str(cost_id).strip() == "" or str(cost_id).lower() == "nan":
                logs.append({
                    "run_id": run_id,
                    "source_file": "return_costs.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-001",
                    "column_name": "cost_id",
                    "raw_value": str(cost_id),
                    "message": "Khóa chính cost_id bị NULL hoặc rỗng",
                })
                invalid_cost_indices.add(idx)
                continue

            # QC-005: Khóa ngoại return_id không tồn tại trong returns hợp lệ
            if return_id not in valid_return_ids:
                logs.append({
                    "run_id": run_id,
                    "source_file": "return_costs.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-005",
                    "column_name": "return_id",
                    "raw_value": str(return_id),
                    "message": f"Mã return_id '{return_id}' không tồn tại trong các sự kiện hoàn hợp lệ",
                })
                invalid_cost_indices.add(idx)

            # QC-002: Chi phí hoàn trả âm
            if pd.notna(amount) and float(amount) < 0:
                logs.append({
                    "run_id": run_id,
                    "source_file": "return_costs.csv",
                    "row_number": int(idx) + 2,
                    "rule_code": "QC-002",
                    "column_name": "amount",
                    "raw_value": str(amount),
                    "message": f"Chi phí hoàn trả bị âm: {amount}",
                })
                invalid_cost_indices.add(idx)

        cleaned_data["return_costs"] = df_costs.drop(index=list(invalid_cost_indices)).copy()

    # --------------------------------------------------------------------------
    # 5. Tổng kết và đóng gói Data Quality Log
    # --------------------------------------------------------------------------
    quality_logs_df = pd.DataFrame(
        logs,
        columns=["run_id", "source_file", "row_number", "rule_code", "column_name", "raw_value", "message"]
    )

    total_valid = sum(len(df) for df in cleaned_data.values())
    total_rejected = len(quality_logs_df)

    stats = {
        "rows_read": total_rows_read,
        "rows_valid": total_valid,
        "rows_rejected": total_rejected,
    }

    logger.info(
        "Hoàn tất kiểm tra chất lượng. Tổng dòng đọc: %d | Hợp lệ: %d | Vi phạm ghi log: %d",
        total_rows_read,
        total_valid,
        total_rejected,
    )

    return cleaned_data, quality_logs_df, stats


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_raw = {
        "carriers": pd.DataFrame({"carrier_id": ["VNPOST", "GHN"], "carrier_name": ["VNPost", "GHN"]}),
        "orders": pd.DataFrame({
            "order_id": ["ORD_1", None, "ORD_3", "ORD_4"],
            "order_date": ["2026-03-01", "2026-03-02", "2026-03-03", "2026-03-04"],
            "carrier_id": ["VNPOST", "VNPOST", "UNKNOWN_CARRIER", "GHN"],
            "order_value": [500000, 300000, 200000, -100000],
        })
    }
    clean, q_logs, stat = validate_data(test_raw)
    print("Violations logged:")
    print(q_logs[["rule_code", "column_name", "message"]])
    print("Stats:", stat)
