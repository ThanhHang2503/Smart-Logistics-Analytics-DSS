# SLADSS Engineering Specification & Execution Plan
> System: Smart Logistics Analytics & Decision Support System (SLADSS)  
> Standard: Enterprise Spec-Driven Development (SDD) & Containerized Data Platform  
> Governing Constitution: `.specify/memory/constitution.md`

---

## 1. Hệ thống Mục tiêu & Ràng buộc Bất biến (Hard Constraints)
1. **Grain Integrity (Bảo toàn mức chi tiết Fact/Dim)**:
   - `fact_orders`: 1 dòng / 1 order.
   - `fact_shipments`: 1 dòng / 1 shipment.
   - `fact_returns`: 1 dòng / 1 return event.
   - `fact_return_costs`: 1 dòng / 1 cost item.
   - *Strict Rule*: Không bao giờ JOIN trực tiếp các Fact table có Grain khác nhau trong phép tính SUM/Aggregate để tránh nhân đôi/nhân bản dòng dữ liệu (anti-fanout). Phải tổng hợp riêng trước khi kết hợp.
2. **Data Quality & Traceability**:
   - Không được âm thầm loại bỏ bản ghi lỗi (zero silent drop).
   - Bản ghi lỗi vi phạm kiểm tra logic (QC-001 -> QC-007) phải chuyển vào bảng `data_quality_log` kèm mã lỗi, nguyên nhân, số dòng và file nguồn.
   - Mọi chu trình thực thi pipeline phải được ghi nhận vào `pipeline_run`.
3. **Idempotency (Tính tái lập)**:
   - Chạy pipeline nhiều lần trên cùng một tập dữ liệu không làm tăng số dòng ngoài ý muốn. Sử dụng cơ chế TRUNCATE & RELOAD cho Staging hoặc UPSERT theo khóa nghiệp vụ.
4. **Environment Isolation**:
   - Toàn bộ cơ sở dữ liệu và script chạy khép kín qua Docker Compose. Không hardcode credentials trong source code.

---

## 2. Kế hoạch Triển khai theo 4 Sprint (Execution Workflows)

### SPRINT 1: Hạ tầng Docker & Containerization (Infrastructure First)
- **Mục tiêu**: Xây dựng môi trường chạy cô lập, sẵn sàng mở port cho Power BI kết nối.
- **Tasks**:
  - [x] Tạo `Dockerfile` dựa trên `python:3.11-slim`, cài đặt build tools và thư viện từ `requirements.txt`.
  - [x] Tạo `docker-compose.yml` gồm 2 services:
    * `postgres_db`: image `postgres:16-alpine`, port `5432:5432`, volume `pgdata`, healthcheck `pg_isready`.
    * `etl_service`: build từ Dockerfile, mount `data/` và `logs/`, depends_on `postgres_db` (condition: service_healthy).
  - [x] Cập nhật `.env.example` và `.env` tương ứng.

### SPRINT 2: Mô hình DDL Cơ sở dữ liệu & Data Quality Log (Storage Layer)
- **Mục tiêu**: Tạo toàn bộ cấu trúc bảng từ Staging đến Warehouse Star Schema và Marts.
- **Tasks**:
  - [ ] Tạo file `sql/ddl/01_staging_and_logs.sql`:
    * Bảng logging: `pipeline_run`, `data_quality_log`.
    * Bảng Staging tác nghiệp: `orders`, `shipments`, `returns`, `return_costs`, `products`, `regions`, `carriers`.
  - [ ] Tạo file `sql/ddl/02_star_schema.sql`:
    * Dimension tables: `dim_date`, `dim_product`, `dim_region`, `dim_carrier`, `dim_return_reason`.
    * Fact tables: `fact_orders`, `fact_shipments`, `fact_returns`, `fact_return_costs`.
  - [ ] Tạo file `sql/marts/logistics_kpi_views.sql`:
    * View tính các KPI chính: Tỷ lệ giao thất bại, Tỷ lệ hoàn, Chi phí hoàn trung bình, Thời gian xử lý hoàn.
    * Đảm bảo xử lý lỗi chia cho 0 bằng `NULLIF(denominator, 0)`.

### SPRINT 3: Bộ sinh Dữ liệu Mô phỏng Thực tế (Synthetic Data Generator)
- **Mục tiêu**: Tạo dữ liệu mẫu 1.000+ orders sát thực tế nghiệp vụ, có cài sẵn dữ liệu lỗi để kiểm thử.
- **Tasks**:
  - [ ] Viết script `scripts/generate_sample_data.py`:
    * Sinh các file CSV vào `data/sample/`: `orders.csv`, `shipments.csv`, `returns.csv`, `return_costs.csv`, `products.csv`, `regions.csv`, `carriers.csv`.
    * Dữ liệu mô phỏng: customer_key mã hóa (CUST_XXXX), không dùng thông tin thật.
    * Tỉ lệ giao thất bại ~8-12%, tỉ lệ hoàn ~5-8%.
    * **Edge Cases bắt buộc**: Cố tình chèn 3-5% bản ghi vi phạm (chi phí âm, ngày hoàn trước ngày tạo đơn, thiếu order_id, mã carrier không tồn tại) để kiểm thử bộ lọc chất lượng.

### SPRINT 4: Xây dựng Module ETL Pipeline Hoàn chỉnh (Data Engineering)
- **Mục tiêu**: Đóng gói luồng ETL chạy độc lập, idempotent, có log đầy đủ.
- **Tasks**:
  - [ ] `etl/config.py`: Đọc cấu hình từ biến môi trường qua `pydantic` hoặc `os.getenv`.
  - [ ] `etl/extract.py`: Đọc các file CSV từ `data/sample/`.
  - [ ] `etl/validate.py`: Kiểm tra 7 mã lỗi (QC-001 -> QC-007), tách records hợp lệ và ghi records lỗi vào `data_quality_log`.
  - [ ] `etl/transform.py`: Chuẩn hóa kiểu dữ liệu, định dạng ngày tháng và ánh xạ sang Star Schema.
  - [ ] `etl/load.py`: Tải dữ liệu vào bảng Staging và Fact/Dimension đảm bảo không bị trùng dòng.
  - [ ] `etl/pipeline.py`: Hàm `main()` điều phối chu trình, cập nhật bảng `pipeline_run` (thời gian bắt đầu, kết thúc, số dòng đọc, số dòng nạp thành công, số dòng lỗi).
  - [ ] Viết unit tests trong `tests/` để kiểm tra validation và tính đúng đắn của KPI.
```[cite: 5]


