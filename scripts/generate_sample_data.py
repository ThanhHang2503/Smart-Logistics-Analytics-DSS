"""
Script: generate_sample_data.py
Mô tả: Sinh bộ dữ liệu mô phỏng thực tế logistics ngược (1.000+ orders, 6-12 tháng)
       và cố tình chèn 3-5% lỗi logic kiểm thử (QC-001 -> QC-005).
Tuân thủ:
  - Hiến pháp Dự án (.specify/memory/constitution.md) - Section 1.4 (Zero PII, Synthetic Data)
  - Sprint 3 Specification (docs/sprint_3_4_spec.md)
"""

import os
import sys
import random
import uuid
from datetime import datetime, timedelta
import pandas as pd

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Đảm bảo tính tái lập (Reproducibility)
random.seed(42)

OUTPUT_DIR = "data/sample"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. Master Data Dimensions (15-20 Sản phẩm, 5 Khu vực, 5 Hãng vận chuyển)
# ------------------------------------------------------------------------------

PRODUCTS = [
    # Electronics
    {"product_id": "PRD_001", "category": "Electronics", "product_name": "Tai nghe Bluetooth chống ồn TWS"},
    {"product_id": "PRD_002", "category": "Electronics", "product_name": "Chuột không dây Silent Click"},
    {"product_id": "PRD_003", "category": "Electronics", "product_name": "Bàn phím cơ không dây RGB"},
    {"product_id": "PRD_004", "category": "Electronics", "product_name": "Sạc dự phòng nhanh 20000mAh"},
    {"product_id": "PRD_005", "category": "Electronics", "product_name": "Camera an ninh Wi-Fi 360"},
    # Fashion
    {"product_id": "PRD_006", "category": "Fashion", "product_name": "Áo sơ mi nam Oxford Slimfit"},
    {"product_id": "PRD_007", "category": "Fashion", "product_name": "Váy dạ hội dáng xòe cao cấp"},
    {"product_id": "PRD_008", "category": "Fashion", "product_name": "Quần jean denim ống suông"},
    {"product_id": "PRD_009", "category": "Fashion", "product_name": "Áo khoác gió thể thao chống nước"},
    {"product_id": "PRD_010", "category": "Fashion", "product_name": "Giày sneaker unisex Classic"},
    # Home & Living / Appliance
    {"product_id": "PRD_011", "category": "Home Appliance", "product_name": "Nồi chiên không dầu điện tử 6L"},
    {"product_id": "PRD_012", "category": "Home Appliance", "product_name": "Máy hút bụi cầm tay không dây"},
    {"product_id": "PRD_013", "category": "Home Appliance", "product_name": "Bình đun siêu tốc inox 304"},
    {"product_id": "PRD_014", "category": "Home Appliance", "product_name": "Máy sấy tóc ion âm bảo vệ tóc"},
    # FMCG & Beauty
    {"product_id": "PRD_015", "category": "FMCG", "product_name": "Hộp viên giặt xả sinh học 3 trong 1"},
    {"product_id": "PRD_016", "category": "FMCG", "product_name": "Nước hoa xịt phòng hữu cơ 300ml"},
    {"product_id": "PRD_017", "category": "Beauty", "product_name": "Kem dưỡng ẩm phục hồi da ban đêm"},
    {"product_id": "PRD_018", "category": "Beauty", "product_name": "Serum Vitamin C làm sáng da"},
]

REGIONS = [
    {"region_id": "REG_NORTH", "region_name": "Miền Bắc", "province_or_area": "Hà Nội, Hải Phòng, Bắc Ninh, Quảng Ninh"},
    {"region_id": "REG_CENTRAL", "region_name": "Miền Trung", "province_or_area": "Đà Nẵng, Thừa Thiên Huế, Quảng Nam, Nghệ An"},
    {"region_id": "REG_SOUTH", "region_name": "Miền Nam", "province_or_area": "TP. Hồ Chí Minh, Bình Dương, Đồng Nai, Bà Rịa - Vũng Tàu"},
    {"region_id": "REG_HIGHLAND", "region_name": "Tây Nguyên", "province_or_area": "Đắk Lắk, Gia Lai, Lâm Đồng"},
    {"region_id": "REG_WEST", "region_name": "Miền Tây", "province_or_area": "Cần Thơ, An Giang, Tiền Giang, Kiên Giang"},
]

CARRIERS = [
    {"carrier_id": "VNPOST", "carrier_name": "Vietnam Post Logistics"},
    {"carrier_id": "VTP", "carrier_name": "Viettel Post"},
    {"carrier_id": "GHN", "carrier_name": "Giao Hàng Nhanh Express"},
    {"carrier_id": "GHTK", "carrier_name": "Giao Hàng Tiết Kiệm"},
    {"carrier_id": "SPX", "carrier_name": "SPX Express"},
]

RETURN_REASONS = [
    "Hàng hỏng hóc / móp méo trong quá trình vận chuyển",
    "Giao sai sản phẩm / màu sắc / kích thước",
    "Khách hàng đổi ý / không còn nhu cầu nhận hàng",
    "Không liên lạc được người nhận quá 3 lần",
    "Giao hàng quá trễ so với cam kết SLA",
    "Sản phẩm lỗi kỹ thuật / không hoạt động",
]

COST_TYPES = [
    "Phí vận chuyển chiều về",
    "Phí kiểm định & lưu kho",
    "Phí đóng gói lại",
    "Phí xử lý giao dịch hoàn tiền",
]


def generate_dataset(num_orders: int = 1200):
    print(f"=== Bắt đầu sinh tập dữ liệu mô phỏng SLADSS ({num_orders} đơn hàng, 10-12 tháng) ===")

    # 1. Ghi file Master Dimensions
    df_products = pd.DataFrame(PRODUCTS)
    df_products.to_csv(os.path.join(OUTPUT_DIR, "products.csv"), index=False, encoding="utf-8")

    df_regions = pd.DataFrame(REGIONS)
    df_regions.to_csv(os.path.join(OUTPUT_DIR, "regions.csv"), index=False, encoding="utf-8")

    df_carriers = pd.DataFrame(CARRIERS)
    df_carriers.to_csv(os.path.join(OUTPUT_DIR, "carriers.csv"), index=False, encoding="utf-8")

    # 2. Sinh Orders, Shipments, Returns, Return Costs
    orders = []
    shipments = []
    returns = []
    return_costs = []

    start_date = datetime(2025, 10, 1)  # Giả lập 1 năm dữ liệu
    carrier_ids = [c["carrier_id"] for c in CARRIERS]
    product_ids = [p["product_id"] for p in PRODUCTS]
    region_ids = [r["region_id"] for r in REGIONS]

    return_counter = 1
    cost_counter = 1

    # Theo dõi số lượng lỗi được cài cắm để báo cáo
    injected_errors = {
        "QC-001 (Null PK)": 0,
        "QC-002 (Negative Value)": 0,
        "QC-003 (Chronology Violation)": 0,
        "QC-004 (Invalid Status)": 0,
        "QC-005 (Orphan FK)": 0,
    }

    for i in range(1, num_orders + 1):
        order_id = f"ORD_{i:06d}"
        days_offset = random.randint(0, 360)
        order_date = start_date + timedelta(days=days_offset)
        
        # Hard Constraint: Mã giả UUID, zero PII
        customer_key = f"CUST_{uuid.uuid4().hex[:12].upper()}"

        product_id = random.choice(product_ids)
        region_id = random.choice(region_ids)
        carrier_id = random.choice(carrier_ids)
        order_value = round(random.uniform(120000, 4800000), -3)

        # ----------------------------------------------------------------------
        # Cố tình cài cắm lỗi có kiểm soát (~3-5% tổng số dòng)
        # ----------------------------------------------------------------------
        # QC-001: Rỗng order_id (khoảng 0.8% đơn)
        if random.random() < 0.008:
            order_id = None
            injected_errors["QC-001 (Null PK)"] += 1

        # QC-002: Giá trị đơn hàng âm (khoảng 0.8% đơn)
        elif random.random() < 0.008:
            order_value = -abs(order_value)
            injected_errors["QC-002 (Negative Value)"] += 1

        # QC-005: Khóa ngoại không tồn tại trong Master Dimensions (khoảng 0.8% đơn)
        elif random.random() < 0.008:
            carrier_id = "UNKNOWN_CARRIER_99"
            injected_errors["QC-005 (Orphan FK)"] += 1

        orders.append({
            "order_id": order_id,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "customer_key": customer_key,
            "product_id": product_id,
            "region_id": region_id,
            "carrier_id": carrier_id,
            "order_value": order_value,
        })

        if not order_id:
            # Nếu order_id bị NULL thì không tạo shipment hợp lệ tương ứng
            continue

        # ----------------------------------------------------------------------
        # Sinh Shipment tương ứng
        # ----------------------------------------------------------------------
        shipment_id = f"SHIP_{i:06d}"
        shipped_at = order_date + timedelta(hours=random.randint(4, 28))
        
        # Mô phỏng tỷ lệ thất bại khoảng 10-12%
        is_delivery_failed = random.random() < 0.11
        delivery_attempts = random.randint(2, 3) if is_delivery_failed else 1

        if is_delivery_failed:
            delivery_status = "delivery_failed"
            delivered_at = shipped_at + timedelta(days=random.randint(2, 5))
        else:
            delivery_status = "delivered"
            delivered_at = shipped_at + timedelta(days=random.randint(1, 4))

        # Cài cắm QC-003 trong Shipments: ngày giao trước ngày gửi (0.5% shipments)
        if random.random() < 0.006:
            delivered_at = shipped_at - timedelta(days=2)
            injected_errors["QC-003 (Chronology Violation)"] += 1

        # Cài cắm QC-004 trong Shipments: trạng thái ngoài enum (0.5% shipments)
        elif random.random() < 0.006:
            delivery_status = "lost_in_transit_unknown"
            injected_errors["QC-004 (Invalid Status)"] += 1

        shipments.append({
            "shipment_id": shipment_id,
            "order_id": order_id,
            "carrier_id": carrier_id,
            "shipped_at": shipped_at.strftime("%Y-%m-%d %H:%M:%S"),
            "delivered_at": delivered_at.strftime("%Y-%m-%d %H:%M:%S"),
            "delivery_status": delivery_status,
            "delivery_attempts": delivery_attempts,
        })

        # ----------------------------------------------------------------------
        # Sinh Returns (100% đơn giao thất bại + ~7% đơn giao thành công bị hoàn)
        # ----------------------------------------------------------------------
        is_returned = is_delivery_failed or (random.random() < 0.07)

        if is_returned:
            return_id = f"RET_{return_counter:06d}"
            return_counter += 1
            
            return_date = delivered_at.date() + timedelta(days=random.randint(1, 5))
            reason = (
                "Không liên lạc được người nhận quá 3 lần"
                if is_delivery_failed
                else random.choice(RETURN_REASONS)
            )
            return_status = "completed"

            # Cài cắm QC-003 trong Returns: ngày hoàn trước ngày tạo đơn (0.5% returns)
            if random.random() < 0.008:
                return_date = order_date.date() - timedelta(days=3)
                injected_errors["QC-003 (Chronology Violation)"] += 1

            returns.append({
                "return_id": return_id,
                "order_id": order_id,
                "return_date": return_date.strftime("%Y-%m-%d"),
                "return_reason": reason,
                "return_status": return_status,
            })

            # ------------------------------------------------------------------
            # Sinh Return Costs (1-2 khoản phí trên mỗi sự kiện hoàn)
            # ------------------------------------------------------------------
            num_cost_lines = random.randint(1, 2)
            for _ in range(num_cost_lines):
                cost_id = f"CST_{cost_counter:06d}"
                cost_counter += 1
                c_type = random.choice(COST_TYPES)
                c_amount = round(random.uniform(30000, 150000), -3)

                # Cài cắm QC-002: Chi phí hoàn trả âm (0.6% costs)
                if random.random() < 0.008:
                    c_amount = -abs(c_amount)
                    injected_errors["QC-002 (Negative Value)"] += 1

                return_costs.append({
                    "cost_id": cost_id,
                    "return_id": return_id,
                    "cost_type": c_type,
                    "amount": c_amount,
                    "currency": "VND",
                })

    # 3. Ghi toàn bộ ra CSV
    df_orders = pd.DataFrame(orders)
    df_orders.to_csv(os.path.join(OUTPUT_DIR, "orders.csv"), index=False, encoding="utf-8")

    df_shipments = pd.DataFrame(shipments)
    df_shipments.to_csv(os.path.join(OUTPUT_DIR, "shipments.csv"), index=False, encoding="utf-8")

    df_returns = pd.DataFrame(returns)
    df_returns.to_csv(os.path.join(OUTPUT_DIR, "returns.csv"), index=False, encoding="utf-8")

    df_costs = pd.DataFrame(return_costs)
    df_costs.to_csv(os.path.join(OUTPUT_DIR, "return_costs.csv"), index=False, encoding="utf-8")

    total_records = len(df_orders) + len(df_shipments) + len(df_returns) + len(df_costs)
    total_injected = sum(injected_errors.values())
    error_rate = (total_injected / total_records) * 100

    print(f"Hoàn thành sinh dữ liệu tại '{OUTPUT_DIR}':")
    print(f"  • products.csv:     {len(df_products):>5} dòng")
    print(f"  • regions.csv:      {len(df_regions):>5} dòng")
    print(f"  • carriers.csv:     {len(df_carriers):>5} dòng")
    print(f"  • orders.csv:       {len(df_orders):>5} dòng")
    print(f"  • shipments.csv:    {len(df_shipments):>5} dòng")
    print(f"  • returns.csv:      {len(df_returns):>5} dòng")
    print(f"  • return_costs.csv: {len(df_costs):>5} dòng")
    print(f"=== Tổng bản ghi tác nghiệp: {total_records:,} dòng ===")
    print(f"=== Thống kê lỗi được cài cắm ({total_injected} lỗi ~ {error_rate:.2f}%): ===")
    for err, count in injected_errors.items():
        print(f"  - {err}: {count} vi phạm")


if __name__ == "__main__":
    generate_dataset()
