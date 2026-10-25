# 📜 SLADSS Project Constitution
<!-- Smart Logistics Analytics & Decision Support System -->
<!-- Hiến pháp Dự án — Tài liệu Bất biến — Mọi thay đổi phải được phê duyệt và tăng version -->

> **Tài liệu này có quyền ưu tiên cao nhất trong toàn bộ dự án.**
> Mọi quyết định kỹ thuật, thiết kế dữ liệu, kiến trúc hạ tầng và quy trình phát triển phải tuân thủ nghiêm ngặt các nguyên tắc được ghi trong đây.
> Bất kỳ ngoại lệ nào cũng phải được ghi chú rõ ràng với lý do kỹ thuật xác đáng.

---

**Version**: `2.1.0` | **Ratified**: `2026-10-24` | **Last Amended**: `2026-10-25`  
**Source Document**: `docs/Bao_cao_de_tai_Smart_Logistics_Analytics_DSS.md` (Phiên bản 2.0 Containerized & AI-Agent Integrated, 25/10/2026)

---

## Mục lục

1. [Tổng quan Dự án](#1-tổng-quan-dự-án)
2. [Hạ tầng Kỹ thuật & Ràng buộc Công nghệ (Docker-Centric Architecture)](#2-hạ-tầng-kỹ-thuật--ràng-buộc-công-nghệ-docker-centric-architecture)
3. [Cấu trúc Monorepo Chuẩn](#3-cấu-trúc-monorepo-chuẩn)
4. [Nguyên tắc Thiết kế Dữ liệu & Star Schema](#4-nguyên-tắc-thiết-kế-dữ-liệu--star-schema)
5. [Quy tắc Chất lượng & Xử lý Pipeline (Zero Silent Drop)](#5-quy-tắc-chất-lượng--xử-lý-pipeline-zero-silent-drop)
6. [Đặc tả Hệ thống Trí tuệ Nhân tạo: Custom ML & Multi-Agent](#6-đặc-tả-hệ-thống-trí-tuệ-nhân-tạo-custom-ml--multi-agent)
7. [Bảo mật & Quản trị Dữ liệu](#7-bảo-mật--quản-trị-dữ-liệu)
8. [Tính Minh bạch của Cảnh báo & Khuyến nghị](#8-tính-minh-bạch-của-cảnh-báo--khuyến-nghị)
9. [Quy trình Phát triển & Enterprise Git Flow](#9-quy-trình-phát-triển--enterprise-git-flow)
10. [Tiêu chí Nghiệm thu Tối thiểu (v2.0)](#10-tiêu-chí-nghiệm-thu-tối-thiểu-v20)
11. [Governance & Amendments](#11-governance--amendments)

---

## 1. Tổng quan Dự án

### 1.1. Danh tính Dự án

| Thuộc tính | Giá trị |
|---|---|
| **Tên tiếng Anh** | Smart Logistics Analytics & Decision Support System |
| **Viết tắt** | **SLADSS** |
| **Tên tiếng Việt** | Hệ thống phân tích dữ liệu, tự động hóa chất lượng và hỗ trợ ra quyết định trong logistics ngược |
| **Phiên bản báo cáo gốc** | 2.0 (Containerized & AI-Agent Integrated) — 25/10/2026 |
| **Định hướng chuyên môn** | Kết hợp 4 nhóm năng lực: BA (Phân tích nghiệp vụ) + DE (Kỹ thuật dữ liệu) + DA (Phân tích dữ liệu) + AI Engineering (Học máy & Multi-Agent) |

### 1.2. Mục tiêu & Phạm vi

SLADSS mô phỏng bài toán doanh nghiệp thương mại điện tử cần theo dõi, đo lường, dự báo và tối ưu hóa chu trình **logistics ngược (reverse logistics)**, bao gồm:

- Đơn giao thất bại và tỷ lệ giao thất bại theo khu vực / đơn vị vận chuyển (carrier).
- Hàng hoàn trả và tỷ lệ hoàn theo thời gian / nhóm sản phẩm / lý do hoàn.
- Chi phí hoàn trả và phân tích cấu trúc chi phí (phí vận chuyển, lưu kho, thẩm định chất lượng).
- Dự báo sớm rủi ro hoàn đơn đối với đơn hàng mới bằng học máy có giám sát.
- Chẩn đoán tự động lỗi chất lượng dữ liệu, bóc tách nguyên nhân gốc rễ (Root Cause Analysis) và trợ lý tương tác ngôn ngữ tự nhiên (Decision Copilot).

Hệ thống vận hành end-to-end trên nền tảng Docker:  
`ingest → validate & audit → transform → star schema load → ML inference & Agent reasoning → web dashboard & BI reporting`

### 1.3. Các Câu hỏi Phân tích Cốt lõi

> Mọi KPI, mô hình ML và tác tử AI phải phục vụ trả lời ít nhất một câu hỏi dưới đây *(§3.3 tài liệu gốc)*.

1. Tỷ lệ hoàn hàng biến động như thế nào theo thời gian và ngành hàng?
2. Đơn vị vận chuyển (Carrier) hoặc tuyến khu vực nào có tỷ lệ giao thất bại vượt ngưỡng cảnh báo chuẩn?
3. Chi phí hoàn trả tập trung lớn nhất ở phân khúc sản phẩm hay lý do hoàn trả nào?
4. Đặc trưng đơn hàng nào (COD, khung giờ đặt, khu vực, giá trị) có xác suất hoàn hàng cao nhất?
5. Biện pháp can thiệp vận hành nào cần được ưu tiên triển khai theo đề xuất của AI Agent?

### 1.4. ⚠️ Chính sách Dữ liệu — BẤT BIẾN

> **TUYỆT ĐỐI**: Toàn bộ dữ liệu sử dụng trong dự án phải là **dữ liệu mô phỏng (Synthetic / Mock Data, Zero PII)** có cài đặt có kiểm soát 3–5% lỗi vi phạm logic nhằm kiểm thử chất lượng.

- `customer_key` phải là **mã giả lập** (hash / UUID tổng hợp), **không** chứa tên, số điện thoại, địa chỉ hoặc bất kỳ PII thật nào.
- Mọi bộ dữ liệu, giao diện dashboard và báo cáo phải được đánh nhãn **"Dữ liệu mô phỏng / Synthetic Data"**.
- Không giả mạo kết luận kinh doanh như thể đó là số liệu nội bộ của một doanh nghiệp thật ngoài đời.

---

## 2. Hạ tầng Kỹ thuật & Ràng buộc Công nghệ (Docker-Centric Architecture)

> **Nguồn**: §4, §5 và §5.2 tài liệu gốc v2.0.  
> Không tự ý bổ sung công nghệ ngoài danh mục phê duyệt dưới đây.

### 2.1. Kiến trúc Cụm 3-Service Docker Compose (BẮT BUỘC)

Hệ thống chuẩn hóa 100% trên cụm Docker Compose (`docker-compose.yml`), gồm 3 services biệt lập kết nối qua mạng nội bộ (`sladss_network`) và named volume (`pgdata`):

| Service | Container Image / Base | Cổng / Port | Vai trò & Trách nhiệm |
|---|---|---|---|
| `postgres_db` | `postgres:16-alpine` | `5432:5432` | **Data Warehouse duy nhất**: Lưu trữ 3 tầng schemas (`staging`, `warehouse`, `marts`) cùng các bảng audit logs (`pipeline_run`, `data_quality_log`). Mở cổng 5432 ra host để Power BI Desktop và DBeaver kết nối trực tiếp. Cấu hình healthcheck `pg_isready`. |
| `etl_service` | `python:3.11-slim` (Dockerfile) | N/A (Internal) | **Data Engine & ML Worker**: Chạy script sinh dữ liệu, thực hiện xác thực chất lượng (DQ Validation), chuẩn hóa dữ liệu, nạp vào Star Schema với tính idempotent, kích hoạt batch pipeline và chạy test suite Pytest. |
| `web_dashboard` | `python:3.11-slim` (Streamlit + Plotly) | `8501:8501` | **Interactive UI & AI Chat**: Giao diện trực quan hóa dữ liệu đọc từ schema `marts`, tích hợp khung chat trợ lý AI Decision Support Copilot phục vụ người quản lý vận hành. |

### 2.2. ⛔ Loại bỏ Hoàn toàn SQLite — BẤT BIẾN

> **NGUYÊN TẮC CỨNG**: **TUYỆT ĐỐI CẤM** sử dụng SQLite fallback hoặc lưu trữ dữ liệu trên file `.db` / `.sqlite` cục bộ dưới mọi hình thức.
> 
> - Mọi môi trường (kể cả Local Dev, Unit Tests, Integration Tests và Production) bắt buộc kết nối trực tiếp đến PostgreSQL 16 Container (`postgres_db`).
> - Bộ test suite Pytest phải kết nối và kiểm thử trực tiếp trên cơ sở dữ liệu PostgreSQL thực tế để kiểm chứng DDL, kiểu dữ liệu, ràng buộc Foreign Key và hàm SQL chuyên biệt.

### 2.3. Bảng Công nghệ Được Phê duyệt (Approved Tech Stack)

| Lớp kiến trúc | Công nghệ phê duyệt | Ghi chú & Ràng buộc |
|---|---|---|
| **Container Engine** | Docker & Docker Compose | Khởi chạy toàn bộ hệ thống bằng 1 lệnh `docker compose up --build` |
| **Storage & Warehouse** | PostgreSQL 16 Alpine | Phân tách rõ 3 schemas: `staging`, `warehouse`, `marts` |
| **ETL & Data Validation** | Python 3.11, Pandas, SQLAlchemy, psycopg2-binary | Chạy trong container `etl_service`, xử lý UTF-8 |
| **Custom Supervised ML** | `scikit-learn`, `xgboost`, `lightgbm`, `imbalanced-learn` (SMOTE), `shap` | Bắt buộc train mô hình mới phân loại nguy cơ hoàn đơn |
| **Multi-Agent Framework** | `langchain`, `langgraph` (StateGraph), `pydantic` | Điều phối 3 tác tử chuyên trách; KHÔNG train mới LLM |
| **LLM Inference Provider** | OpenAI API (`gpt-4o-mini`) hoặc Local LLM qua Ollama (`llama3.1:8b`) | Tích hợp Few-shot Prompting, RAG và Structured Output |
| **Web Dashboard** | Streamlit, Plotly | Web application tương tác đa chiều nhúng khung chat AI |
| **Enterprise BI** | Power BI Desktop (.pbix) | Kết nối PostgreSQL container qua cổng 5432 |
| **Quality Testing** | Pytest, SQL Assertions | Chạy tự động trong container `etl_service` |
| **Configuration** | `.env` + `python-dotenv` | `.env` được bảo mật nghiêm ngặt, cấm commit lên Git |

---

## 3. Cấu trúc Monorepo Chuẩn

> **Nguồn**: §9 tài liệu gốc v2.0. Bắt buộc tuân thủ — không đặt file sai vị trí.

```
smart-logistics-analytics-dss/
│
├── docker-compose.yml             # Cấu hình cụm 3 services: postgres_db, etl_service, web_dashboard
├── Dockerfile                     # Base image Python 3.11 cho etl_service và web_dashboard
├── requirements.txt               # Thư viện Python cố định phiên bản
├── .env.example                   # Biến môi trường mẫu an toàn (không chứa secret)
├── .gitignore                     # Bỏ qua .env, *.db, pycache, raw data
├── README.md                      # Hướng dẫn khởi chạy, kiến trúc, giới hạn đề tài
│
├── docs/                          # Tài liệu BA, kiến trúc, data dictionary, KPI definitions
│   ├── Bao_cao_de_tai_Smart_Logistics_Analytics_DSS.md  # Báo cáo đề tài gốc v2.0
│   ├── data-dictionary.md         # Data dictionary chi tiết 3 schemas
│   ├── kpi-definitions.md         # Định nghĩa công thức và điều kiện biên KPI
│   └── architecture/              # Sơ đồ kiến trúc Docker và Agent Workflow
│
├── data/
│   ├── sample/                    # File CSV dữ liệu mô phỏng (Synthetic Data, Zero PII)
│   └── README.md                  # Hướng dẫn sinh và nguồn gốc dữ liệu
│
├── etl/                           # Python ETL modules (Idempotent Pipeline)
│   ├── extract.py                 # Đọc CSV với encoding UTF-8
│   ├── validate.py                # Bẫy lỗi QC-001 -> QC-007, ghi log audit
│   ├── transform.py               # Chuẩn hóa và mapping sang Star Schema
│   ├── load.py                    # Nạp PostgreSQL với cơ chế Upsert/Idempotent
│   └── pipeline.py                # Quản lý vòng đời chạy và cập nhật pipeline_run
│
├── sql/                           # Toàn bộ SQL Scripts theo phân tầng
│   ├── ddl/                       # init_schema.sql (Tạo schemas staging, warehouse, marts, logs)
│   ├── staging/                   # DDL và logic bảng staging
│   ├── warehouse/                 # DDL Star Schema: 4 Fact + 5 Dimension tables
│   ├── marts/                     # SQL Views phục vụ Dashboard & AI Text-to-SQL
│   └── tests/                     # SQL validation queries (Grain, FK integrity, Anti-fanout)
│
├── ai_agents/                     # Hệ thống AI: Custom ML & LLM Multi-Agent
│   ├── README.md                  # Kiến trúc và nguyên tắc vận hành AI
│   ├── custom_ml/                 # Mô hình Machine Learning tự huấn luyện (XGBoost/LightGBM)
│   │   ├── train_risk_model.py    # Huấn luyện mô hình dự báo rủi ro hoàn đơn + SMOTE
│   │   ├── predict_risk.py        # Xuất xác suất P(return) cho đơn hàng mới
│   │   └── explainability.py      # Trích xuất và giải thích đặc trưng bằng SHAP
│   ├── agents/                    # 3 Tác tử chuyên trách (LangGraph / LangChain)
│   │   ├── dq_diagnosis_agent.py  # Chẩn đoán lỗi dữ liệu QC-001 -> QC-007
│   │   ├── rca_agent.py           # Phân tích nguyên nhân gốc rễ bất thường KPI (StateGraph)
│   │   └── copilot_agent.py       # Trợ lý Text-to-SQL và tư vấn ra quyết định
│   └── prompts/                   # System prompts, few-shot examples, JSON schemas
│
├── web_dashboard/                 # Ứng dụng Web tương tác Streamlit (Port 8501)
│   ├── README.md                  # Hướng dẫn sử dụng giao diện web
│   ├── app.py                     # Entry point chính của Streamlit
│   ├── components/                # UI components (KPI cards, charts, chat box)
│   └── pages/                     # Các trang nghiệp vụ chuyên sâu
│
├── dashboard/                     # Báo cáo Power BI Desktop
│   └── README.md                  # Hướng dẫn kết nối cổng 5432 container
│
├── notebooks/                     # Jupyter Notebooks CHỈ dùng cho EDA và thử nghiệm mô hình
│   └── exploratory_analysis.ipynb
│
├── tests/                         # Pytest test suites (chạy trên PostgreSQL Container)
│   ├── unit/                      # Test KPI logic và hàm tính toán
│   ├── data/                      # Test bộ quy tắc chất lượng dữ liệu QC
│   └── integration/               # Test luồng pipeline end-to-end
│
└── scripts/                       # Scripts tiện ích
    ├── generate_mock_data.py      # Sinh dữ liệu mô phỏng có kiểm soát lỗi
    └── setup_db.py                # Khởi tạo schemas và phân quyền database
```

---

## 4. Nguyên tắc Thiết kế Dữ liệu & Star Schema

> **Nguồn**: §7 tài liệu gốc v2.0.  
> Các nguyên tắc dưới đây là **BẤT BIẾN** để bảo đảm tính toàn vẹn số liệu tài chính và vận hành.

### 4.1. Cấu trúc Star Schema trên PostgreSQL 16

Mô hình kho dữ liệu phân tách rõ ràng 4 Fact Tables và 5 Dimension Tables:

| Bảng Fact | Grain (Mức chi tiết bất biến) | Khóa chính nghiệp vụ | Khóa ngoại chính |
|---|---|---|---|
| `fact_orders` | **1 dòng = 1 đơn hàng** | `order_key` | `date_key`, `product_key`, `region_key`, `carrier_key` |
| `fact_shipments` | **1 dòng = 1 lần giao hàng** | `shipment_key` | `order_key`, `carrier_key`, `shipped_date_key` |
| `fact_returns` | **1 dòng = 1 sự kiện hoàn trả** | `return_key` | `order_key`, `return_date_key`, `reason_key` |
| `fact_return_costs`| **1 dòng = 1 khoản chi phí phát sinh** | `cost_key` | `return_key`, `order_key`, `cost_date_key` |

| Bảng Dimension | Vai trò & Nội dung |
|---|---|
| `dim_date` | Chi tiết thời gian (date_key, full_date, day, month, quarter, year, is_weekend) |
| `dim_product` | Danh mục sản phẩm (product_key, product_id, product_name, category) |
| `dim_region` | Khu vực địa lý (region_key, region_id, region_name, province_or_area) |
| `dim_carrier` | Đơn vị vận chuyển (carrier_key, carrier_id, carrier_name) |
| `dim_return_reason` | Lý do hoàn hàng chuẩn hóa (reason_key, reason_code, reason_description, category) |

### 4.2. ⛔ Nguyên tắc Chống Lỗi Nhân Dòng (Anti-Fanout Rule) — BẤT BIẾN

**TUYỆT ĐỐI KHÔNG** JOIN trực tiếp giữa các bảng Fact có Grain khác nhau (`fact_orders`, `fact_shipments`, `fact_returns`, `fact_return_costs`) trong cùng một câu truy vấn tính tổng (`SUM`, `COUNT`) khi chưa được tổng hợp độc lập về cùng cấp độ Grain.

**Lý do**: Một đơn hàng có thể có nhiều lần giao hàng và phát sinh nhiều khoản chi phí hoàn. Phép JOIN trực tiếp sẽ nhân bản số dòng (Cartesian fanout), khiến tổng doanh thu hoặc chi phí bị **phóng đại sai lệch nghiêm trọng**.

```sql
-- ✅ ĐÚNG: Tổng hợp chi phí độc lập về grain order_key TRƯỚC KHI kết hợp
WITH aggregated_costs AS (
    SELECT order_key, SUM(cost_amount) AS total_return_cost
    FROM fact_return_costs
    GROUP BY order_key
),
aggregated_shipments AS (
    SELECT order_key, COUNT(*) AS total_shipment_attempts
    FROM fact_shipments
    GROUP BY order_key
)
SELECT 
    fo.order_key,
    fo.order_value,
    COALESCE(ac.total_return_cost, 0) AS total_return_cost,
    COALESCE(ash.total_shipment_attempts, 0) AS total_shipment_attempts
FROM fact_orders fo
LEFT JOIN aggregated_costs ac       ON fo.order_key = ac.order_key
LEFT JOIN aggregated_shipments ash  ON fo.order_key = ash.order_key;
```

---

## 5. Quy tắc Chất lượng & Xử lý Pipeline (Zero Silent Drop)

> **Nguồn**: §5.2 và §8.2 tài liệu gốc v2.0.

### 5.1. ⚠️ Tính Idempotent (BẤT BIẾN)

Pipeline ETL khi chạy lại nhiều lần trên cùng một tập dữ liệu nguồn **KHÔNG ĐƯỢC PHÉP** sinh ra các bản ghi trùng lặp:
- Sử dụng cơ chế **UPSERT** (`INSERT ... ON CONFLICT DO UPDATE`) dựa trên business key.
- Bảng staging phải được quản lý theo `run_id` và làm sạch trước mỗi đợt nạp batch.

### 5.2. ⚠️ Bộ 7 Quy tắc Chất lượng Dữ liệu (QC-001 đến QC-007)

Mọi bản ghi dữ liệu vi phạm bất kỳ quy tắc nào dưới đây **KHÔNG ĐƯỢC ÂM THẦM BỎ QUA (Zero Silent Drop)** mà phải lập tức chuyển vào bảng audit `staging.data_quality_log`:

| Mã lỗi | Tên quy tắc | Tiêu chí vi phạm | Hành động xử lý |
|---|---|---|---|
| `QC-001` | **Null Primary Key** | Khóa chính nghiệp vụ rỗng (`order_id IS NULL`, `shipment_id IS NULL`) | Từ chối nạp vào Fact; ghi log |
| `QC-002` | **Negative Financial Value** | Doanh thu hoặc chi phí có giá trị âm (`order_value < 0`, `cost_amount < 0`) | Cách ly bản ghi; ghi log |
| `QC-003` | **Date Chronology Violation** | Trình tự thời gian phi logic (`return_date < order_date` hoặc `delivered_at < shipped_at`) | Cách ly bản ghi; ghi log |
| `QC-004` | **Invalid Status Enum** | Trạng thái giao hàng/hoàn hàng nằm ngoài danh mục chuẩn | Đánh dấu lỗi enum; ghi log |
| `QC-005` | **Orphan Foreign Key** | Khóa ngoại tham chiếu đến bản ghi không tồn tại trong Dimension tương ứng | Chuyển vào staging; ghi log |
| `QC-006` | **Duplicate Business Key** | Trùng lặp khóa nghiệp vụ trong cùng một batch nạp | Khử trùng lặp; ghi log bản ghi trùng |
| `QC-007` | **Format / Currency Anomaly** | Sai định dạng ngày giờ hoặc đơn vị tiền tệ không được hỗ trợ | Từ chối hoặc chuẩn hóa có kiểm toán |

### 5.3. Audit Tables: `pipeline_run` & `data_quality_log`

Mọi phiên thực thi pipeline phải được ghi nhận vào `staging.pipeline_run`:
- `run_id` (UUID), `started_at`, `ended_at`, `status` (`RUNNING`, `SUCCESS`, `FAILED`).
- `rows_read`, `rows_valid`, `rows_rejected`, `rows_loaded`, `error_detail`.

Bảng `staging.data_quality_log` lưu vết chi tiết từng dòng lỗi:
- `log_id`, `run_id`, `source_file`, `row_number`, `rule_code` (`QC-001`..`QC-007`), `message`, `raw_value`, `logged_at`.

---

## 6. Đặc tả Hệ thống Trí tuệ Nhân tạo: Custom ML & Multi-Agent

> **Nguồn**: §6.1, §6.2 và §6.3 tài liệu gốc v2.0.  
> Đây là định chế cốt lõi phân định ranh giới giữa Machine Learning tự huấn luyện và Agentic AI.

### 6.1. Ma trận Lựa chọn Công nghệ (BẤT BIẾN)

```
┌───────────────────────────────────────────────────────────────────────────┐
│                      SLADSS AI ARCHITECTURE MATRIX                         │
├─────────────────────────────────────┬─────────────────────────────────────┤
│ 1. CUSTOM TRAIN MACHINE LEARNING    │ 2. MULTI-AGENT SYSTEM               │
│    (Supervised Predictive Model)    │    (Pretrained LLM + Agentic Graph) │
├─────────────────────────────────────┼─────────────────────────────────────┤
│ • Bài toán: Return Risk Prediction  │ • 3 Agents: DQ, RCA, Copilot        │
│ • BẮT BUỘC TRAIN MÔ HÌNH MỚI        │ • TUYỆT ĐỐI KHÔNG TRAIN MỚI LLM    │
│ • Stack: scikit-learn, xgboost,     │ • Stack: LangChain, LangGraph,      │
│   lightgbm, imbalanced-learn, shap  │   Pydantic, OpenAI / Ollama         │
│ • Output: Xác suất P(return)        │ • Output: Reasoning, Tool Call, SQL │
└─────────────────────────────────────┴─────────────────────────────────────┘
```

### 6.2. Mô hình Tự Huấn Luyện Mới (Custom Train ML): Return Risk Predictor

1. **Bản chất kỹ thuật**: Mô hình học máy có giám sát phân loại nhị phân (Binary Classification) được huấn luyện từ dữ liệu lịch sử trong Data Warehouse.
2. **Biến mục tiêu**: `is_returned ∈ {0, 1}` (1: Đơn bị hoàn trả; 0: Đơn thành công).
3. **Bộ đặc trưng đầu vào (Features)**:
   - Thuộc tính đơn hàng: `order_value`, `cod_flag` (thanh toán khi nhận hàng), khung giờ đặt hàng.
   - Thuộc tính danh mục: `product_category_id`.
   - Tỷ lệ lịch sử: `carrier_failure_rate_30d`, `region_return_rate_30d`.
4. **Quy trình Huấn luyện & Đánh giá**:
   - **Xử lý mất cân bằng lớp (Class Imbalance)**: Áp dụng thuật toán **SMOTE** (Synthetic Minority Over-sampling Technique) từ thư viện `imbalanced-learn`.
   - **Mô hình triển khai**: So sánh hiệu năng giữa `XGBoostClassifier` và `LGBMClassifier`.
   - **Chỉ số đánh giá**: Đánh giá dựa trên `PR-AUC` (Precision-Recall AUC), `F1-Score` của lớp thiểu số, và `ROC-AUC`.
   - **Khả năng giải thích (XAI)**: Sử dụng thư viện `shap` để tính toán TreeSHAP values, trực quan hóa đóng góp của từng đặc trưng vào xác suất rủi ro $P(\text{return})$.

### 6.3. Hệ thống Multi-Agent (Pretrained LLM + Agentic Framework)

> **RÀNG BUỘC CỨNG**: Không tự huấn luyện (pre-train) hay fine-tune mô hình ngôn ngữ lớn từ đầu. Tận dụng LLM có sẵn (OpenAI `gpt-4o-mini` hoặc Local LLM `llama3.1:8b` qua Ollama) kết hợp cùng Framework điều phối `LangGraph` và `LangChain`.

Hệ thống bao gồm 3 tác tử chuyên trách:

#### 1. Data Quality Diagnosis Agent (Giám sát & Bẫy lỗi dữ liệu)
- **Mục tiêu**: Tự động quét và diễn giải các bản ghi bị từ chối từ `staging.data_quality_log` (QC-001 đến QC-007).
- **Cơ chế**: Gom nhóm lỗi theo file nguồn hoặc đối tác vận chuyển; áp dụng Pydantic Structured Output để xuất báo cáo chẩn đoán gồm 3 thành phần:
  1. *Vấn đề phát hiện* (Defect Summary).
  2. *Tác động đến báo cáo & mô hình* (Downstream Impact).
  3. *Hướng xử lý đề xuất* (Remediation: Data Imputation / Source System Fix).

#### 2. Root Cause Analysis (RCA) Agent (Phân tích nguyên nhân biến động KPI)
- **Mục tiêu**: Chẩn đoán và tìm nguyên nhân gốc rễ khi chỉ số vận hành bị lệch bất thường.
- **Cơ chế**: Xây dựng đồ thị có trạng thái (**StateGraph** qua `LangGraph`) gồm 3 nodes:
  - **Node 1 (Anomaly Detection)**: Phát hiện chỉ số KPI (tỷ lệ hoàn, chi phí hoàn, tỷ lệ giao thất bại) vượt ngưỡng baseline 2 độ lệch chuẩn ($\mu \pm 2\sigma$).
  - **Node 2 (Data Mart Drill-down Tool)**: Kích hoạt Function Calling sinh SQL bóc tách đa chiều qua schema `marts` theo `dim_carrier`, `dim_region`, `dim_return_reason`.
  - **Node 3 (Synthesis & Recommendation)**: Tổng hợp bằng chứng định lượng, xác định nhóm nguyên nhân chi phối và đề xuất giải pháp vận hành.

#### 3. Decision Support Copilot (Trợ lý điều hành & Text-to-SQL)
- **Mục tiêu**: Cho phép nhà quản lý đặt câu hỏi bằng ngôn ngữ tự nhiên trên Web Dashboard Streamlit và nhận câu trả lời kèm bảng biểu/số liệu tin cậy.
- **Cơ chế an toàn (Guardrails BẮT BUỘC)**:
  - **Chỉ đọc (Read-Only)**: Agent chỉ được cấp quyền `SELECT` duy nhất trên schema `marts`. Cấm tuyệt đối quyền can thiệp vào `staging` hay `warehouse`.
  - **Phòng vệ chia cho 0**: Mọi câu SQL sinh ra có phép chia tỷ lệ bắt buộc sử dụng `NULLIF(denominator, 0)`.
  - **Phân định Tương quan vs Nhân quả**: Không đưa ra khẳng định nhân quả tuyệt đối nếu dữ liệu chỉ mang tính tương quan.

---

## 7. Bảo mật & Quản trị Dữ liệu

> **Nguồn**: §15 và §16.1 tài liệu gốc.

### 7.1. ⛔ Danh mục Cấm Tuyệt đối (Security Guardrails)

| Hành động | Mức độ | Biện pháp cưỡng chế |
|---|---|---|
| Commit file `.env` chứa credential thật | **⛔ CẤM TUYỆT ĐỐI** | Khai báo trong `.gitignore`; kiểm tra trước mỗi commit |
| Hard-code API Key (OpenAI) hoặc mật khẩu DB | **⛔ CẤM TUYỆT ĐỐI** | Chỉ đọc từ biến môi trường qua `os.getenv` |
| Sử dụng dữ liệu định danh cá nhân thật (PII) | **⛔ CẤM TUYỆT ĐỐI** | 100% dữ liệu là Synthetic Mock Data |
| Cấp quyền DDL/DML cho Text-to-SQL Copilot | **⛔ CẤM TUYỆT ĐỐI** | Phân quyền DB user riêng biệt với quyền `SELECT` trên `marts` |

### 7.2. Cấu hình `.env.example` Chuẩn

```dotenv
# Database Configuration (PostgreSQL 16 Container)
DB_HOST=postgres_db
DB_PORT=5432
DB_NAME=sladss_db
DB_USER=sladss_user
DB_PASSWORD=your_secure_password_here

# Pipeline Settings
PIPELINE_BATCH_SIZE=1000
LOG_LEVEL=INFO

# AI & LLM Configuration
LLM_PROVIDER=openai                    # openai | ollama
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-4o-mini
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=llama3.1:8b

# Web Dashboard
STREAMLIT_SERVER_PORT=8501
```

---

## 8. Tính Minh bạch của Cảnh báo & Khuyến nghị

> **Nguồn**: §6.2 và §7.1 tài liệu gốc.  
> Áp dụng cho toàn bộ thông báo, KPI card và đề xuất từ hệ thống AI Copilot.

Mọi cảnh báo và khuyến nghị phải đồng thời cung cấp đủ 5 yếu tố minh bạch:
1. **Công thức tính toán**: Hiển thị rõ công thức và định nghĩa mẫu số.
2. **Giá trị mẫu số**: Luôn kiểm tra `denominator > 0`; trả về `N/A` nếu mẫu số bằng 0.
3. **Kích thước mẫu tối thiểu (Sample Size Guardrail)**: Không đưa ra cảnh báo hoặc kết luận nếu số lượng quan sát $N < 30$.
4. **Khoảng thời gian & Thời điểm cập nhật**: Xác định rõ kỳ dữ liệu đang phân tích.
5. **Bằng chứng định lượng**: Nêu rõ nhóm thực thể liên quan (Carrier, Region, Category) và số liệu bằng chứng trước khi đưa ra đề xuất.

---

## 9. Quy trình Phát triển & Enterprise Git Flow

### 9.1. Chuẩn mực Commit (Conventional Commits)

```
<type>(<scope>): <mô tả ngắn bằng tiếng Anh hoặc tiếng Việt>

Types : feat | fix | docs | refactor | test | chore | style
Scopes: etl | sql | ml | agent | dashboard | tests | docker | docs

Ví dụ:
  feat(agent): implement LangGraph state graph for RCA agent
  feat(ml): train return risk classifier using LightGBM and SMOTE
  fix(etl): enforce QC-003 date chronology validation in validate.py
  feat(dashboard): add chat UI component for Decision Copilot
```

### 9.2. Kế hoạch Triển khai Chuẩn 12 Tuần

- **Tuần 1**: Khởi tạo Repository, Hiến pháp dự án (`constitution.md`) & Hạ tầng Docker ban đầu.
- **Tuần 2**: Phân tích nghiệp vụ BA (BRD, BPMN As-Is/To-Be, Use Cases).
- **Tuần 3**: Hoàn thiện Docker Compose & DDL Database (PostgreSQL 16 schemas).
- **Tuần 4**: Bộ sinh dữ liệu mô phỏng (Synthetic Data Generator 1.200+ đơn, 3-5% lỗi QC).
- **Tuần 5**: Pipeline ETL Idempotent & Quản trị chất lượng dữ liệu (QC-001 -> QC-007).
- **Tuần 6**: Kho dữ liệu Star Schema & Các SQL Data Mart Views.
- **Tuần 7**: Huấn luyện Custom ML Model (XGBoost/LightGBM) dự báo rủi ro hoàn đơn + SHAP.
- **Tuần 8**: Xây dựng cụm AI Multi-Agent (LangGraph: DQ Agent, RCA Agent, Text-to-SQL Copilot).
- **Tuần 9**: Phát triển Web Dashboard tương tác bằng Streamlit tích hợp khung chat Copilot.
- **Tuần 10**: Thiết kế Báo cáo Power BI Desktop kết nối PostgreSQL container qua cổng 5432.
- **Tuần 11**: Kiểm thử toàn diện Pytest (100% Passed trên container) & Tối ưu hóa hiệu năng.
- **Tuần 12**: Đóng gói dự án, ghi hình video demo, tài liệu bàn giao portfolio.

---

## 10. Tiêu chí Nghiệm thu Tối thiểu (v2.0)

Dự án chỉ được coi là **hoàn thành đạt chuẩn nghiệm thu** khi thỏa mãn đầy đủ 9 tiêu chí sau:

1. **Khởi chạy 1 lệnh (Docker-Centric)**: Toàn bộ hệ thống chạy thành công bằng `docker compose up --build`, sẵn sàng 3 services (`postgres_db`, `etl_service`, `web_dashboard`).
2. **Không tồn tại SQLite**: 100% truy vấn dữ liệu và kiểm thử thực hiện trên PostgreSQL 16 Alpine.
3. **Bộ dữ liệu mô phỏng minh bạch**: Có ít nhất 1.200+ đơn hàng synthetic, đánh nhãn rõ ràng, không chứa PII.
4. **Star Schema chuẩn Grain & Anti-Fanout**: 4 Fact Tables và 5 Dimension Tables; không xảy ra lỗi nhân dòng trong các views.
5. **Pipeline ETL Idempotent & Audit đầy đủ**: Ghi nhận chính xác vào `pipeline_run` và bẫy đủ các lỗi QC-001 -> QC-007 vào `data_quality_log`.
6. **Custom ML Model được huấn luyện**: Huấn luyện thành công mô hình XGBoost/LightGBM dự báo xác suất hoàn đơn, có cân bằng SMOTE và giải thích SHAP.
7. **Hệ thống Multi-Agent hoạt động**: Triển khai đủ 3 tác tử: DQ Diagnosis Agent, RCA Agent (LangGraph), Decision Support Copilot (Text-to-SQL an toàn).
8. **Web Dashboard & Power BI**: Web Streamlit (cổng 8501) hoạt động mượt mà kèm chat Copilot; file Power BI kết nối thành công cổng 5432.
9. **Test Suite Đạt 100%**: Bộ kiểm thử Pytest chạy tự động trong container kiểm chứng toàn bộ tính năng và bẫy lỗi.

---

## 11. Governance & Amendments

### 11.1. Thứ bậc Hiệu lực Tài liệu

```
constitution.md  >  docs/kpi-definitions.md  >  docs/data-dictionary.md  >  Source Code
```

Khi có bất kỳ sự khác biệt hoặc mâu thuẫn nào giữa tài liệu và mã nguồn, **Hiến pháp dự án (`constitution.md`) luôn giữ quyền ưu tiên cao nhất**.

### 11.2. Quy trình Tu chỉnh Hiến pháp

Mọi điều chỉnh Hiến pháp phải tuân thủ Semantic Versioning:
- **PATCH** (`x.x.+1`): Sửa lỗi chính tả, làm rõ ngôn từ diễn đạt.
- **MINOR** (`x.+1.0`): Bổ sung thêm nguyên tắc, module hoặc công nghệ mới mà không phá vỡ nguyên tắc cũ.
- **MAJOR** (`+1.0.0`): Thay đổi cấu trúc cốt lõi, thay đổi hạ tầng cơ sở hoặc định chế bất biến.
Mọi tu chỉnh phải cập nhật trường `Last Amended` và ghi nhận tóm tắt vào lịch sử tài liệu.
