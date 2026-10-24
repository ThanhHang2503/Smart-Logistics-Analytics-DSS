# SLADSS Specification: Sprint 3 & Sprint 4
> System: Smart Logistics Analytics & Decision Support System (SLADSS)  
> Scope: Synthetic Data Generation (with QC edge cases) & Production-grade ETL Pipeline  
> Governing Documents: `.specify/memory/constitution.md` & `docs/roadmap_spec.md`

---

## 1. Mục tiêu Sprint 3 (Data Generation & QC Violations)
Nâng cấp `scripts/generate_sample_data.py` để sinh tập dữ liệu lớn và chân thực hơn:
- **Quy mô**: 1.000+ orders, mô phỏng 6-12 tháng tác nghiệp logistics.
- **Thực thể sinh ra**:
  - `products.csv` (15-20 mã sản phẩm phân chia theo ngành hàng: Electronics, Fashion, FMCG, Home Appliance).
  - `regions.csv` (Miền Bắc, Miền Trung, Miền Nam, Tây Nguyên và các tỉnh/thành phố).
  - `carriers.csv` (4-5 đơn vị vận chuyển: VNPost, ViettelPost, GHN, GHTK, SPX).
  - `orders.csv` (order_id, order_date, customer_key giả lập UUID, product_id, region_id, carrier_id, order_value).
  - `shipments.csv` (shipment_id, order_id, carrier_id, shipped_at, delivered_at, delivery_status).
  - `returns.csv` (return_id, order_id, return_date, return_reason, return_status).
  - `return_costs.csv` (cost_id, return_id, cost_type, amount, currency).
- **Edge Cases có kiểm soát (Cố tình chèn 3-5% lỗi để test QC-001 -> QC-007)**:
  - `QC-001` (Null Primary Key): Chèn một số dòng rỗng `order_id` hoặc `shipment_id`.
  - `QC-002` (Negative Values): Chèn `order_value < 0` hoặc `cost_amount < 0`.
  - `QC-003` (Date Chronology Violation): `return_date < order_date` hoặc `delivered_at < shipped_at`.
  - `QC-004` (Invalid Status Enum): Trạng thái nằm ngoài danh mục định nghĩa.
  - `QC-005` (Foreign Key Orphan): `carrier_id` hoặc `product_id` không tồn tại trong danh mục.

---

## 2. Mục tiêu Sprint 4 (Idempotent ETL Pipeline & Observability)
Hoàn thiện các module trong `etl/`:
1. `etl/validate.py`:
   - Kiểm tra toàn bộ 5 bảng sự kiện với bộ quy tắc QC-001 đến QC-007.
   - Phân tách triệt để: Record hợp lệ -> đưa tiếp vào luồng xử lý; Record lỗi -> ghi nhận vào `staging.data_quality_log` kèm `(run_id, source_file, row_number, rule_code, message)`. Không silent drop.
2. `etl/transform.py`:
   - Chuẩn hóa kiểu dữ liệu (Date, Timestamp, Numeric).
   - Tạo dimension tables và tính toán các surrogate keys / attributes (ví dụ `dim_date`).
   - Xây dựng 4 bảng Facts đúng Grain: `fact_orders`, `fact_shipments`, `fact_returns`, `fact_return_costs`.
3. `etl/load.py`:
   - Nạp dữ liệu vào PostgreSQL (hoặc SQLite fallback) với cơ chế Idempotent (chạy lại 2 lần không nhân đôi dòng hay lỗi primary key).
4. `etl/pipeline.py`:
   - Hàm `main()` điều phối luồng chạy end-to-end.
   - Khởi tạo và kết thúc bản ghi trong `staging.pipeline_run`: ghi `run_id`, `started_at`, `ended_at`, `status` ('SUCCESS'/'FAILED'), `rows_read`, `rows_loaded`, `rows_rejected`.
```[cite: 5]

---

