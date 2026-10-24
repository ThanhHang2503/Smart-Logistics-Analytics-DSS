# Smart Logistics Analytics & Decision Support System (SLADSS)

> **Hệ thống phân tích dữ liệu và hỗ trợ ra quyết định trong logistics ngược**  
> Dự án portfolio tích hợp ba mảng năng lực: **Business Analysis (BA)**, **Data Analysis (DA)**, và **Data Engineering (DE)**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20SQLite-informational.svg)](https://www.postgresql.org/)
[![BI](https://img.shields.io/badge/BI-Power%20BI-yellow.svg)](https://powerbi.microsoft.com/)
[![Testing](https://img.shields.io/badge/Testing-Pytest-green.svg)](https://docs.pytest.org/)
[![Governance](https://img.shields.io/badge/Constitution-v2.0.0-purple.svg)](.specify/memory/constitution.md)

---

## 1. 📌 Tổng quan Dự án

Trong thương mại điện tử, chi phí logistics ngược (đơn giao thất bại, hàng hoàn trả, lưu kho, xử lý khiếu nại) thường chiếm từ 10–25% giá trị hàng hóa nếu không được kiểm soát. **SLADSS** giải quyết bài toán quản lý và tối ưu hóa vận hành logistics ngược thông qua:

- **Pipeline kỹ thuật dữ liệu (DE)**: Thu thập, kiểm tra chất lượng (Data Quality), chuẩn hóa và nạp dữ liệu vào Data Warehouse Star Schema.
- **Phân tích dữ liệu & Trực quan hóa (DA)**: Xây dựng các Data Marts, tính toán KPI (tỷ lệ hoàn, tỷ lệ giao thất bại, chi phí hoàn) và thiết kế Dashboard quản trị trên Power BI.
- **Hỗ trợ ra quyết định & Nghiệp vụ (BA)**: Tài liệu hóa quy trình (BPMN As-Is / To-Be), phân tích nguyên nhân gốc rễ (Root Cause), và cung cấp cảnh báo/khuyến nghị có căn cứ minh bạch.

> ⚠️ **Chính sách dữ liệu**: Toàn bộ dữ liệu trong repository này là **dữ liệu mô phỏng (Synthetic Mock Data)** 100%, không chứa thông tin định danh cá nhân (Zero PII) và được đánh nhãn rõ ràng theo [Hiến pháp Dự án](.specify/memory/constitution.md).

---

## 2. 🏗️ Kiến trúc & Cấu trúc Thư mục

### Luồng Dữ liệu (Data Flow)
```
[data/sample/*.csv] 
       ↓ (extract.py)
[Pandas Ingestion] 
       ↓ (validate.py -> data_quality_log)
[Cleaned Data] 
       ↓ (transform.py)
[Star Schema: Facts & Dims] 
       ↓ (load.py)
[PostgreSQL / SQLite Warehouse] 
       ↓ (sql/marts/ Views)
[Power BI Dashboard / Insights]
```

### Cấu trúc Mã nguồn
```
Smart-Logistics-Analytics-DSS/
├── data/
│   ├── sample/                     # Dữ liệu mô phỏng (CSV) không chứa PII
│   └── README.md                   # Chính sách dữ liệu & hướng dẫn sinh data
├── etl/                            # Các module pipeline Python
│   ├── __init__.py
│   ├── extract.py                  # Trích xuất dữ liệu từ nguồn
│   ├── validate.py                 # Kiểm tra chất lượng dữ liệu & ghi log lỗi
│   ├── transform.py                # Chuẩn hóa & ánh xạ vào Star Schema
│   └── load.py                     # Nạp dữ liệu idempotent vào Database
├── sql/                            # Toàn bộ mã SQL có phân cấp
│   ├── ddl/
│   │   └── init_schema.sql         # Khởi tạo schema Staging & Warehouse
│   ├── staging/                    # Các script xử lý tầng staging
│   ├── warehouse/                  # Star Schema transformations
│   ├── marts/
│   │   └── v_kpi_return_rates.sql  # Views tổng hợp KPI chống fanout
│   └── tests/
│       └── test_data_integrity.sql # Kiểm thử tính toàn vẹn dữ liệu
├── notebooks/                      # CHỈ dùng cho EDA phân tích khám phá
│   └── README.md
├── dashboard/                      # Power BI Desktop & hướng dẫn trực quan hóa
│   └── README.md
├── tests/                          # Bộ kiểm thử tự động với Pytest
│   ├── conftest.py
│   ├── unit/                       # Unit tests (công thức KPI, anti-fanout)
│   ├── data/                       # Data quality tests (DQ-001 -> DQ-005)
│   └── integration/                # Pipeline integration tests
├── scripts/                        # Tiện ích tự động hóa
│   ├── generate_sample_data.py     # Script sinh dữ liệu mock ngẫu nhiên
│   └── setup_db.py                 # Script thiết lập database & chạy DDL
├── docs/                           # Bộ tài liệu dự án, BA & spec
│   ├── Bao_cao_de_tai_Smart_Logistics_Analytics_DSS.md
│   └── roadmap_spec.md
├── .specify/memory/constitution.md # Hiến pháp kỹ thuật dự án (v2.0.0)
├── .env.example                    # Biến môi trường mẫu không chứa secret
├── .gitignore                      # Cấu hình loại trừ Git chuẩn
├── requirements.txt                # Thư viện phụ thuộc cốt lõi
└── README.md                       # Tài liệu hướng dẫn chính
```

---

## 3. 🚀 Hướng dẫn Thiết lập & Chạy Dự án

### Bước 1: Khởi tạo môi trường ảo Python
```bash
# Clone repository (nếu chưa có)
git clone https://github.com/ThanhHang2503/Smart-Logistics-Analytics-DSS.git
cd Smart-Logistics-Analytics-DSS

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment:
# Trên Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Trên Linux/macOS:
source venv/bin/activate
```

### Bước 2: Cài đặt các thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình biến môi trường
Sao chép `.env.example` thành `.env` và tùy chỉnh thông số kết nối:
```bash
cp .env.example .env
```
*(Nếu muốn chạy kiểm thử nhanh bằng SQLite mà không cần cài PostgreSQL, đặt `USE_SQLITE_FALLBACK=true` trong file `.env`)*.

### Bước 4: Sinh dữ liệu mẫu & Thiết lập Database
```bash
# 1. Sinh dữ liệu mô phỏng vào data/sample/
python scripts/generate_sample_data.py

# 2. Khởi tạo cấu trúc bảng trong cơ sở dữ liệu
python scripts/setup_db.py
```

### Bước 5: Chạy Pipeline ETL
```bash
python -c "from etl import extract_data, validate_data, transform_data, load_data; raw = extract_data(); clean, logs = validate_data(raw); star = transform_data(clean); load_data(star);"
```

---

## 4. 🧪 Chạy Kiểm thử (Testing)

Dự án áp dụng Pytest cho cả unit test, data quality test và integration test:
```bash
pytest -v
```

Kiểm tra tính toàn vẹn dữ liệu trong Data Warehouse:
```bash
# Thực thi các query kiểm thử trong sql/tests/test_data_integrity.sql
```

---

## 5. 📊 Khám phá Dashboard

1. Mở **Power BI Desktop**.
2. Chọn file báo cáo trong thư mục [dashboard/](dashboard/README.md).
3. Đổi kết nối dữ liệu đến cơ sở dữ liệu đã nạp ở Bước 4.
4. Xem hướng dẫn chi tiết tại [dashboard/README.md](dashboard/README.md).

---

## 6. 📜 Quy ước Đóng góp (Git Workflow)

- Dự án tuân thủ định dạng **Conventional Commits**:
  - `feat: add return-cost KPI view in marts/`
  - `fix: handle NULL carrier_id in validate.py`
  - `docs: update star schema grain definitions`
- Trước khi commit và push, luôn chạy checklist:
  ```bash
  git status
  pytest
  ```
  *(Đảm bảo tuyệt đối không commit file `.env`, file `.db`, hoặc dữ liệu nhạy cảm)*.
