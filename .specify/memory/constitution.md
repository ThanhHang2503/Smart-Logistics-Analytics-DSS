# 📜 SLADSS Project Constitution
<!-- Smart Logistics Analytics & Decision Support System -->
<!-- Hiến pháp Dự án — Tài liệu Bất biến — Mọi thay đổi phải được phê duyệt và tăng version -->

> **Tài liệu này có quyền ưu tiên cao nhất trong toàn bộ dự án.**
> Mọi quyết định kỹ thuật, thiết kế dữ liệu, và quy trình phát triển phải tuân thủ các nguyên tắc được ghi trong đây.
> Bất kỳ ngoại lệ nào cũng phải được ghi chú rõ ràng với lý do kỹ thuật xác đáng.

---

**Version**: `2.0.0` | **Ratified**: `2026-10-24` | **Last Amended**: `2026-10-24`  
**Source Document**: `docs/Bao_cao_de_tai_Smart_Logistics_Analytics_DSS.md` (v1.0, 19/10/2026)

---

## Mục lục

1. [Tổng quan Dự án](#1-tổng-quan-dự-án)
2. [Tech Stack & Ràng buộc Công nghệ](#2-tech-stack--ràng-buộc-công-nghệ)
3. [Cấu trúc Repository Chuẩn](#3-cấu-trúc-repository-chuẩn)
4. [Nguyên tắc Thiết kế Dữ liệu & Star Schema](#4-nguyên-tắc-thiết-kế-dữ-liệu--star-schema)
5. [Quy tắc Chất lượng & Xử lý Pipeline](#5-quy-tắc-chất-lượng--xử-lý-pipeline)
6. [Bảo mật & Quản trị Dữ liệu](#6-bảo-mật--quản-trị-dữ-liệu)
7. [Tính Minh bạch của Cảnh báo & Khuyến nghị](#7-tính-minh-bạch-của-cảnh-báo--khuyến-nghị)
8. [Quy trình Phát triển & Git Workflow](#8-quy-trình-phát-triển--git-workflow)
9. [Tiêu chí Nghiệm thu Tối thiểu](#9-tiêu-chí-nghiệm-thu-tối-thiểu)
10. [Governance & Amendments](#10-governance--amendments)

---

## 1. Tổng quan Dự án

### 1.1. Danh tính Dự án

| Thuộc tính | Giá trị |
|---|---|
| **Tên tiếng Anh** | Smart Logistics Analytics & Decision Support System |
| **Viết tắt** | **SLADSS** |
| **Tên tiếng Việt** | Hệ thống phân tích dữ liệu và hỗ trợ ra quyết định trong logistics ngược |
| **Phiên bản tài liệu gốc** | 1.0 — 19/10/2026 |
| **Định hướng** | Portfolio kết hợp BA + DA + DE |

### 1.2. Mục tiêu & Phạm vi

SLADSS mô phỏng bài toán doanh nghiệp thương mại điện tử cần theo dõi và phân tích **logistics ngược**, gồm:

- Đơn giao thất bại và tỷ lệ giao thất bại theo khu vực / đơn vị vận chuyển.
- Hàng hoàn trả và tỷ lệ hoàn theo thời gian / nhóm sản phẩm.
- Chi phí hoàn trả và phân tích nguyên nhân phát sinh chi phí.
- Hiệu quả hoạt động của từng đơn vị vận chuyển (carrier).

Hệ thống **không chỉ hiển thị biểu đồ** — dữ liệu đi qua pipeline Python đầy đủ:  
`ingest → validate → transform → load → dashboard → khuyến nghị có giải thích`

### 1.3. Các Câu hỏi Phân tích Cốt lõi

> Mọi KPI và tính năng phát triển phải trả lời được ít nhất một câu hỏi dưới đây *(§3.3 tài liệu gốc)*.

1. Tỷ lệ hoàn hàng thay đổi như thế nào theo tháng?
2. Khu vực hoặc đơn vị vận chuyển nào có tỷ lệ giao thất bại cao hơn mức tham chiếu?
3. Nhóm sản phẩm nào có chi phí hoàn trả lớn nhất?
4. Chi phí hoàn trả tập trung ở một số nguyên nhân hay phân tán?
5. Nhóm đơn nào nên được ưu tiên điều tra dựa trên tỷ lệ, số lượng và chi phí?

### 1.4. ⚠️ Chính sách Dữ liệu — BẤT BIẾN

> **TUYỆT ĐỐI**: Toàn bộ dữ liệu sử dụng trong dự án phải là dữ liệu **mô phỏng (Synthetic / Mock Data)**.

- `customer_key` phải là **mã giả lập** (hash / UUID tổng hợp), **không** chứa tên, số điện thoại, địa chỉ hoặc bất kỳ PII thật nào.
- Mọi bộ dữ liệu phải được đánh nhãn **"dữ liệu mô phỏng"** trong dashboard và báo cáo.
- Nếu dùng dữ liệu công khai, phải ghi rõ nguồn và giấy phép.
- **Không** tạo ra kết luận kinh doanh như thể đó là kết quả của doanh nghiệp thật.

---

## 2. Tech Stack & Ràng buộc Công nghệ

> **Nguồn**: §8 và §8.2 tài liệu gốc.  
> Không thêm công nghệ mới vào `requirements.txt` mà không cập nhật lý do vào `docs/`.

### 2.1. Stack Được Phê duyệt

| Lớp | Công nghệ | Ghi chú |
|---|---|---|
| **Data Ingestion & Validation** | Python 3.x, Pandas, python-dotenv | Entry point của mọi dữ liệu vào hệ thống |
| **ORM / DB Connector** | SQLAlchemy, psycopg2-binary | Không hard-code connection string |
| **Storage — Production** | PostgreSQL | Database duy nhất cho môi trường staging/production |
| **Storage — Local Test** | SQLite | Chỉ dùng cho unit test; không thay thế PostgreSQL ở production |
| **Transformation & Modeling** | SQL DDL/DML | Viết trong `sql/` với phân cấp thư mục chuẩn |
| **BI & Visualization** | Power BI Desktop (PBIX) | File PBIX được commit, **không** commit credentials |
| **Báo cáo thay thế** | Markdown / CSV export | Dùng khi không có Power BI |
| **Testing** | Pytest + SQL Validation queries | Bắt buộc cho mọi KPI và pipeline step |
| **Orchestration (Phase 1)** | Python script thủ công | Airflow chỉ thêm ở phase mở rộng |
| **Containerization** | Docker (tùy chọn) | Thêm sau khi pipeline chạy ổn định |
| **Version Control** | Git + GitHub | Commit message theo Conventional Commits |
| **Cấu hình môi trường** | `.env` + `python-dotenv` | `.env` KHÔNG được commit lên Git |

### 2.2. Quyết định Công nghệ Cứng (Hard Decisions)

- **Chọn MỘT database chính**: PostgreSQL cho mọi môi trường non-test. Không vừa dùng MySQL vừa PostgreSQL.
- **Không dùng Jupyter Notebook cho pipeline logic**: Notebook chỉ dùng cho EDA. Logic pipeline nằm trong Python module có thể `import` và `pytest`.
- **FastAPI / React là phần mở rộng tùy chọn**: Không bắt buộc để hoàn thành phiên bản phân tích dữ liệu cốt lõi.

---

## 3. Cấu trúc Repository Chuẩn

> **Nguồn**: §16 tài liệu gốc. Bắt buộc tuân thủ — không được đặt file sai thư mục.

```
smart-logistics-analytics-dss/
│
├── docs/                          # Tài liệu BA, data dictionary, kiến trúc
│   ├── project-charter.md
│   ├── requirements/
│   ├── process/                   # BPMN As-Is / To-Be
│   ├── data-dictionary.md         # CẬP NHẬT mỗi khi thêm/đổi schema
│   ├── kpi-definitions.md         # ĐỊNH NGHĨA KPI trước khi viết SQL
│   └── architecture/
│
├── data/
│   ├── sample/                    # CHỈ chứa CSV mô phỏng — KHÔNG dữ liệu nhạy cảm
│   └── README.md                  # Mô tả nguồn gốc và cách tái tạo dữ liệu mẫu
│
├── etl/                           # Python ETL modules — có thể import và test
│   ├── extract.py
│   ├── validate.py
│   ├── transform.py
│   └── load.py
│
├── sql/                           # Toàn bộ DDL/DML — phân cấp rõ ràng
│   ├── ddl/                       # init_schema.sql — source of truth cho schema
│   ├── staging/                   # Staging table queries
│   ├── warehouse/                 # Star Schema: fact + dim tables
│   ├── marts/                     # Data Mart views phục vụ dashboard
│   └── tests/                     # SQL validation queries
│
├── notebooks/                     # CHỈ dùng cho EDA — KHÔNG chứa pipeline logic
│   └── exploratory_analysis.ipynb
│
├── dashboard/                     # File PBIX và hướng dẫn
│   └── README.md                  # Hướng dẫn mở và kết nối dashboard
│
├── tests/                         # Pytest test suites
│   ├── unit/                      # Test KPI logic
│   ├── data/                      # Test data quality
│   └── integration/               # Test end-to-end pipeline
│
├── scripts/                       # Script tiện ích
│   ├── generate_mock_data.py      # Sinh dữ liệu mô phỏng
│   └── setup_db.py                # Khởi tạo database
│
├── .env.example                   # CHỈ chứa key names + giá trị mẫu an toàn
├── .gitignore                     # Phải bao gồm .env, *.db, data/raw/
├── requirements.txt               # Pinned versions
└── README.md                      # Hướng dẫn cài đặt, cấu hình, chạy, cấu trúc, giới hạn
```

### 3.1. Quy tắc Đặt File

| Quy tắc | Lý do |
|---|---|
| Schema thay đổi → cập nhật `sql/ddl/init_schema.sql` VÀ `docs/data-dictionary.md` | Đồng bộ tài liệu và code |
| KPI mới → định nghĩa trong `docs/kpi-definitions.md` TRƯỚC khi viết SQL | Tránh SQL và dashboard không nhất quán |
| Logic pipeline → `etl/*.py` hoặc `scripts/`, KHÔNG trong `notebooks/` | Đảm bảo có thể test và tái chạy |
| Dữ liệu mẫu → `data/sample/` kèm README ghi rõ đây là mock data | Minh bạch, không nhầm với dữ liệu thật |

---

## 4. Nguyên tắc Thiết kế Dữ liệu & Star Schema

> **Nguồn**: §9 và §9.2 tài liệu gốc.  
> Đây là các nguyên tắc **BẤT BIẾN** — vi phạm sẽ gây sai lệch KPI nghiêm trọng.

### 4.1. Các Thực thể Nghiệp vụ Nguồn (Operational Tables)

| Thực thể | Trường chính | Ý nghĩa |
|---|---|---|
| `orders` | `order_id`, `order_date`, `customer_key` (mã giả), `product_id`, `region_id`, `carrier_id`, `order_value` | Đơn hàng |
| `shipments` | `shipment_id`, `order_id`, `carrier_id`, `shipped_at`, `delivered_at`, `delivery_status` | Thông tin mỗi lần giao |
| `returns` | `return_id`, `order_id`, `return_date`, `return_reason`, `return_status` | Sự kiện hoàn trả |
| `return_costs` | `cost_id`, `return_id`, `cost_type`, `amount`, `currency` | Chi phí phát sinh từ hoàn |
| `products` | `product_id`, `category`, `product_name` | Danh mục sản phẩm |
| `regions` | `region_id`, `region_name`, `province_or_area` | Khu vực địa lý |
| `carriers` | `carrier_id`, `carrier_name` | Đơn vị vận chuyển |
| `data_quality_log` | `run_id`, `source_file`, `row_number`, `rule_code`, `message` | Lỗi dữ liệu — KHÔNG bỏ qua |
| `pipeline_run` | `run_id`, `started_at`, `ended_at`, `status`, `rows_read`, `rows_loaded` | Lịch sử mỗi lần chạy pipeline |

### 4.2. Star Schema — Grain Definitions (BẤT BIẾN)

> **⚠️ NGUYÊN TẮC GRAIN — KHÔNG ĐƯỢC VI PHẠM**

| Bảng Fact | Grain (Mức chi tiết) | Khóa chính nghiệp vụ |
|---|---|---|
| `fact_orders` | **1 dòng = 1 đơn hàng** | `order_key` |
| `fact_shipments` | **1 dòng = 1 lần giao hàng** | `shipment_key` |
| `fact_returns` | **1 dòng = 1 sự kiện hoàn trả** | `return_key` |
| `fact_return_costs` | **1 dòng = 1 khoản chi phí phát sinh** | `cost_key` |

| Bảng Dimension | Nội dung |
|---|---|
| `dim_date` | Một ngày (date_key, date, day, month, quarter, year) |
| `dim_product` | Một sản phẩm / phiên bản lịch sử (SCD nếu cần) |
| `dim_region` | Một khu vực địa lý |
| `dim_carrier` | Một đơn vị vận chuyển |
| `dim_return_reason` | Một lý do hoàn chuẩn hóa |

### 4.3. ⛔ Quy tắc Cấm JOIN Làm Nhân Số liệu — BẤT BIẾN

**TUYỆT ĐỐI KHÔNG** JOIN trực tiếp các bảng Fact có Grain khác nhau trong một phép tính tổng hợp (`SUM`, `COUNT`, ...) mà không tổng hợp từng bảng về cùng grain trước.

**Lý do**: Một đơn hàng có thể có nhiều lần giao (`shipments`) VÀ nhiều khoản chi phí (`return_costs`). JOIN trực tiếp tạo tích Cartesian, làm tổng doanh thu hoặc chi phí bị **nhân lên sai**.

```sql
-- ✅ ĐÚNG: Tổng hợp về grain đơn hàng TRƯỚC KHI kết hợp
WITH order_costs AS (
    -- Grain: 1 dòng / 1 đơn hàng (GROUP BY về grain fact_orders)
    SELECT fr.order_key, SUM(frc.cost_amount) AS total_cost
    FROM fact_return_costs frc
    JOIN fact_returns fr USING (return_key)
    GROUP BY fr.order_key
),
order_shipments AS (
    -- Grain: 1 dòng / 1 đơn hàng
    SELECT order_key, COUNT(*) AS shipment_count
    FROM fact_shipments
    GROUP BY order_key
)
SELECT fo.order_key, fo.order_value, oc.total_cost, os.shipment_count
FROM fact_orders fo
LEFT JOIN order_costs oc     USING (order_key)
LEFT JOIN order_shipments os USING (order_key);

-- ❌ SAI: JOIN trực tiếp sẽ nhân số liệu (fanout)
SELECT fo.order_key, SUM(fo.order_value), SUM(frc.cost_amount)
FROM fact_orders fo
JOIN fact_shipments fs    ON fo.order_key = fs.order_key   -- fanout!
JOIN fact_return_costs frc ON fs.order_key = frc.return_key -- fanout nhân đôi!
GROUP BY fo.order_key;
```

> **Mọi query tổng hợp chéo bảng fact PHẢI có comment giải thích grain và cảnh báo fanout.**

---

## 5. Quy tắc Chất lượng & Xử lý Pipeline

> **Nguồn**: §9.3 và §10 tài liệu gốc.

### 5.1. ⚠️ Tính Idempotent — BẤT BIẾN

> Pipeline chạy lại nhiều lần trên cùng một tập dữ liệu **KHÔNG ĐƯỢC** sinh bản ghi trùng ngoài ý muốn.

**Cách thực thi**:
- Xác định **business key** rõ ràng cho mỗi bảng (ví dụ: `order_id` cho `orders`).
- Dùng chiến lược **UPSERT** (`INSERT ... ON CONFLICT DO UPDATE`) hoặc nạp theo **batch có kiểm soát**.
- Bảng staging phải có cơ chế **deduplication** trước khi load vào warehouse.
- Staging table phải được truncate hoặc có logic idempotent trước khi tái nạp.

### 5.2. ⚠️ Xử lý Dữ liệu Lỗi — BẤT BIẾN

> **TUYỆT ĐỐI KHÔNG** âm thầm loại bỏ bản ghi lỗi mà không ghi log.

Dòng dữ liệu vi phạm bất kỳ quy tắc nào dưới đây phải được chuyển vào bảng `data_quality_log`:

| Quy tắc | Mã lỗi | Ví dụ vi phạm |
|---|---|---|
| Khóa chính không được rỗng hoặc trùng | `QC-001` | `order_id IS NULL` hoặc trùng lặp |
| Ngày phải parse được đúng định dạng | `QC-002` | `order_date = '2026-13-45'` |
| Ngày hoàn không sớm hơn ngày tạo đơn | `QC-003` | `return_date < order_date` |
| Chi phí không âm | `QC-004` | `amount = -500` |
| Tiền tệ thống nhất theo danh sách cho phép | `QC-005` | `currency = 'XYZ'` |
| Trạng thái phải thuộc danh mục định nghĩa | `QC-006` | `delivery_status = 'unknown_status'` |
| Khóa ngoại phải tham chiếu thực thể tồn tại | `QC-007` | `carrier_id` không tồn tại trong `carriers` |

**Schema `data_quality_log`**:

```sql
CREATE TABLE data_quality_log (
    log_id      SERIAL      PRIMARY KEY,
    run_id      UUID        NOT NULL REFERENCES pipeline_run(run_id),
    source_file TEXT        NOT NULL,
    row_number  INTEGER,
    rule_code   VARCHAR(10) NOT NULL,   -- e.g. 'QC-003'
    message     TEXT        NOT NULL,   -- mô tả lỗi cụ thể
    raw_value   TEXT,                   -- giá trị gốc gây lỗi
    logged_at   TIMESTAMPTZ DEFAULT NOW()
);
```

### 5.3. Ghi nhận Pipeline Run — BẮT BUỘC

> Mọi lần thực thi pipeline PHẢI được ghi nhận vào `pipeline_run`.

**Schema `pipeline_run`**:

```sql
CREATE TABLE pipeline_run (
    run_id        UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file   TEXT,
    started_at    TIMESTAMPTZ NOT NULL,
    ended_at      TIMESTAMPTZ,
    status        VARCHAR(20) CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED')),
    rows_read     INTEGER,
    rows_valid    INTEGER,
    rows_rejected INTEGER,
    rows_loaded   INTEGER,
    error_detail  TEXT        -- NULL nếu SUCCESS
);
```

**Quy tắc**: Pipeline chỉ được đánh dấu `SUCCESS` khi **tất cả** các bước hoàn tất hợp lệ. Bất kỳ bước nào thất bại phải ghi `FAILED` và điền `error_detail`.

### 5.4. Pseudocode Pipeline Chuẩn

```python
def run_pipeline(source_file: str) -> None:
    run_id = create_run_record(source_file, status="RUNNING")
    try:
        raw_records         = extract(source_file, run_id)
        valid, rejected     = validate_and_normalize(raw_records)
        write_rejected_rows(rejected, run_id)       # -> data_quality_log
        load_staging(valid, idempotent=True)
        transform_warehouse()                       # SQL DDL/DML
        run_data_quality_tests()
        publish_dashboard_dataset()
        finish_run_record(run_id, status="SUCCESS", ...)
    except Exception as e:
        finish_run_record(run_id, status="FAILED", error_detail=str(e))
        raise
```

### 5.5. Kiểm tra Chất lượng Sau Load (Post-Load Validation)

Sau khi load vào warehouse, bắt buộc chạy SQL validation:

- **Uniqueness**: Grain của mỗi fact table không bị vi phạm.
- **Referential integrity**: Mọi foreign key trong fact phải tồn tại trong dim tương ứng.
- **KPI reconciliation**: Tổng số đơn trong `fact_orders` khớp với staging source.
- **No zero-denominator**: Mọi tỷ lệ phải trả về `NULL` khi mẫu số = 0.

---

## 6. Bảo mật & Quản trị Dữ liệu

> **Nguồn**: §15 và §16.1 tài liệu gốc.

### 6.1. ⛔ Quy tắc Bảo mật — BẤT BIẾN

| Hành động | Trạng thái |
|---|---|
| Commit file `.env` lên Git | **⛔ TUYỆT ĐỐI CẤM** |
| Commit mật khẩu database dưới bất kỳ dạng nào | **⛔ TUYỆT ĐỐI CẤM** |
| Commit connection string có thông tin xác thực | **⛔ TUYỆT ĐỐI CẤM** |
| Commit API key / secret token | **⛔ TUYỆT ĐỐI CẤM** |
| Commit dữ liệu cá nhân thật (tên, SĐT, địa chỉ) | **⛔ TUYỆT ĐỐI CẤM** |
| Commit file dữ liệu lớn không cần thiết | **❌ TRÁNH** |
| Dùng `customer_key` dạng hash/UUID giả lập | **✅ BẮT BUỘC** |
| Duy trì `.env.example` với key names + giá trị mẫu an toàn | **✅ BẮT BUỘC** |
| Dùng biến môi trường cho mọi cấu hình kết nối | **✅ BẮT BUỘC** |

### 6.2. Xử lý Sự cố Lộ Secret

> Nếu vô tình commit secret, **chỉ xóa khỏi file hiện tại là CHƯA ĐỦ**.  
> Phải: **thu hồi / đổi secret ngay lập tức** + xử lý lịch sử Git (BFG Repo Cleaner hoặc `git filter-branch`).

### 6.3. Template `.env.example`

```dotenv
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sladss_db
DB_USER=your_db_user
DB_PASSWORD=your_secure_password_here

# Pipeline Configuration
PIPELINE_BATCH_SIZE=1000
LOG_LEVEL=INFO

# Optional: Power BI
POWERBI_WORKSPACE_ID=your_workspace_id
```

### 6.4. `.gitignore` Bắt buộc Bao gồm

```gitignore
# Secrets & environment
.env
*.env.local

# Database files
*.db
*.sqlite

# Raw/sensitive data
data/raw/
data/private/

# Python artifacts
__pycache__/
*.pyc
.pytest_cache/
venv/
.venv/

# OS artifacts
.DS_Store
Thumbs.db
```

---

## 7. Tính Minh bạch của Cảnh báo & Khuyến nghị

> **Nguồn**: §6.2 NFR-08 và §7.1 tài liệu gốc.  
> Áp dụng cho mọi alert, KPI card, và recommendation trong dashboard.

### 7.1. ⚠️ Yêu cầu Minh bạch — BẮT BUỘC

Mọi cảnh báo KPI và khuyến nghị điều tra phải **đồng thời** cung cấp:

| Yếu tố | Mô tả | Ví dụ |
|---|---|---|
| **Công thức** | Cách tính KPI / điều kiện kích hoạt cảnh báo | `tỷ lệ hoàn = số đơn hoàn / số đơn đủ điều kiện × 100%` |
| **Mẫu số** | Giá trị mẫu số; nếu = 0 → trả `NULL`/`N/A` | `mẫu số = 234 đơn` |
| **Sample Size** | Số lượng quan sát tối thiểu để kết luận có ý nghĩa | `Chỉ cảnh báo khi N ≥ 30 đơn` |
| **Kỳ dữ liệu** | Khoảng thời gian và thời điểm cập nhật gần nhất | `Tháng 9/2026, cập nhật 2026-10-01` |
| **Nhóm liên quan** | Đơn vị vận chuyển / khu vực / sản phẩm cụ thể | `Carrier: ViettelPost, Khu vực: HCM` |

### 7.2. ⛔ Quy tắc Diễn giải — BẤT BIẾN

> **TUYỆT ĐỐI KHÔNG** quy kết nguyên nhân nhân quả khi chỉ có dữ liệu tương quan.

| ❌ KHÔNG dùng | ✅ THAY BẰNG |
|---|---|
| "ViettelPost **gây ra** tỷ lệ hoàn cao" | "ViettelPost **có liên quan** đến tỷ lệ hoàn cao" |
| "Sản phẩm X **làm tăng** chi phí hoàn" | "Sản phẩm X **có chi phí hoàn cao hơn mức tham chiếu**; cần điều tra thêm" |
| "Do vấn đề chất lượng nên..." | "Quan sát cho thấy...; có thể do... (cần xác nhận thêm)" |

### 7.3. Alert Rule Template

```python
# Mọi quy tắc cảnh báo phải có đủ các trường sau:
alert_rule = {
    "condition":       "delivery_failure_rate > threshold",
    "threshold":       "configurable (default: 15%)",
    "min_sample_size": 30,       # Không cảnh báo nếu N < 30
    "denominator_guard": True,   # Trả NULL nếu mẫu số = 0
    "display_evidence":  True,   # Hiển thị số đơn và kỳ dữ liệu
    "causal_claim":      False   # Không tuyên bố nhân quả
}
```

---

## 8. Quy trình Phát triển & Git Workflow

> **Nguồn**: §16.1 tài liệu gốc.

### 8.1. Commit Message Convention (Conventional Commits)

```
<type>(<scope>): <mô tả ngắn>

Types : feat | fix | docs | refactor | test | chore | style
Scopes: etl | sql | dashboard | data | tests | docs | ci

Ví dụ:
  feat(sql): add return-cost KPI view in marts/
  fix(etl): handle NULL carrier_id in validate.py
  docs(data-dictionary): update fact_returns grain definition
  test(pipeline): add idempotency test for load_staging()
```

### 8.2. Checklist Trước Khi Push

```bash
git status           # Kiểm tra file thay đổi
git diff --staged    # Xem nội dung sắp commit
# Đảm bảo KHÔNG có: .env | *.db | data/raw/ | credentials
git push origin <branch>
```

### 8.3. Thứ tự Phát triển Khuyến nghị

| Bước | Nội dung | Đầu ra kiểm chứng |
|---|---|---|
| 1 | Tài liệu BA (problem statement, KPI definition, ERD) | `docs/` hoàn chỉnh |
| 2 | Mock data với trường hợp bình thường và lỗi | `data/sample/*.csv` |
| 3 | DDL và khởi tạo database | `sql/ddl/init_schema.sql` |
| 4 | ETL pipeline với validate + log | `etl/*.py` chạy được |
| 5 | SQL KPI và đối chiếu test cases | `sql/marts/`, `tests/` |
| 6 | Star Schema và kiểm tra grain | `sql/warehouse/` |
| 7 | Power BI dashboard | Dashboard 3 trang |
| 8 | Pytest tests và SQL validation | Test report |
| — | *(Tùy chọn)* Docker, FastAPI, Airflow | Phase mở rộng |

---

## 9. Tiêu chí Nghiệm thu Tối thiểu

> **Nguồn**: §14.2 tài liệu gốc.  
> Dự án chỉ được coi là **hoàn thành** khi đáp ứng đủ 8 tiêu chí sau.

| # | Tiêu chí | Cách kiểm tra |
|---|---|---|
| 1 | Có ít nhất một bộ dữ liệu mẫu được ghi rõ là **dữ liệu mô phỏng** | Nhãn trong README và dashboard |
| 2 | Có tài liệu định nghĩa **KPI và mẫu số** đầy đủ | `docs/kpi-definitions.md` |
| 3 | Có thể chạy **pipeline end-to-end** từ CSV đến dashboard | `README.md` hướng dẫn, chạy thực tế được |
| 4 | Có **kiểm tra chất lượng dữ liệu** và nhật ký cho mỗi lần chạy | `data_quality_log` + `pipeline_run` |
| 5 | Có ít nhất **3 trang/nhóm phân tích** hoặc dashboard tương đương | Power BI hoặc báo cáo Markdown |
| 6 | Có ít nhất **5 insight** theo cấu trúc: quan sát → bằng chứng → diễn giải → đề xuất | Báo cáo phân tích |
| 7 | Có **test cases** cho KPI chính và trường hợp dữ liệu lỗi | `tests/` với Pytest |
| 8 | **README** nêu đủ: môi trường, cấu hình, cách chạy, cấu trúc thư mục, giới hạn | `README.md` |

---

## 10. Governance & Amendments

### 10.1. Quyền ưu tiên Tài liệu

```
constitution.md  >  docs/kpi-definitions.md  >  docs/data-dictionary.md  >  Code
```

Khi có mâu thuẫn giữa tài liệu và code, **tài liệu thắng** — code phải được cập nhật để khớp.

### 10.2. Quy trình Thay đổi Constitution

1. Mở issue mô tả lý do thay đổi và tác động.
2. Cập nhật phần liên quan với comment giải thích.
3. **Tăng version** theo Semantic Versioning:
   - **PATCH** (`x.x.+1`): Làm rõ ngôn ngữ, sửa typo.
   - **MINOR** (`x.+1.0`): Thêm nguyên tắc mới không phá vỡ nguyên tắc cũ.
   - **MAJOR** (`+1.0.0`): Thay đổi nguyên tắc bất biến hiện có.
4. Cập nhật trường `Last Amended` ở đầu file.

### 10.3. Dependency Management

- Không thêm dependency mới vào `requirements.txt` mà không ghi lý do vào `docs/`.
- Pin phiên bản cụ thể trong `requirements.txt` (không dùng `>=` không có upper bound).
- Xem xét tác động bảo mật trước khi thêm thư viện mới.

---

*"Thước đo thành công không phải số lượng công nghệ, mà là khả năng giải thích bài toán, định nghĩa dữ liệu và KPI chính xác, chứng minh pipeline hoạt động, diễn giải insight có căn cứ và giúp người khác chạy lại được project."*

— Tài liệu đề tài SLADSS, §Kết luận
