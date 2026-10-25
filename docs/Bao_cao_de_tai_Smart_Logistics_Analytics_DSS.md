BÁO CÁO ĐỀ XUẤT ĐỀ TÀI PROJECT SLADSS
SMART LOGISTICS ANALYTICS & DECISION SUPPORT SYSTEM
Hệ thống phân tích dữ liệu, tự động hóa chất lượng và hỗ trợ ra quyết định trong logistics ngược

Định hướng portfolio chuyên sâu cho sinh viên năm cuối ngành Công nghệ thông tin / Hệ thống thông tin
Phiên bản: 2.0 (Containerized & AI-Agent Integrated) | Ngày cập nhật: 25/10/2026
1. Tóm tắt đề tài
Tên tiếng Việt: Hệ thống phân tích dữ liệu và hỗ trợ ra quyết định trong logistics ngược.
Tên tiếng Anh: Smart Logistics Analytics & Decision Support System (SLADSS).
Định hướng chuyên môn: Xây dựng nền tảng dữ liệu doanh nghiệp kết hợp 4 nhóm năng lực: Phân tích nghiệp vụ (BA), Kỹ thuật dữ liệu (DE), Phân tích dữ liệu (DA) và Trí tuệ nhân tạo / Trợ lý quyết định (AI Engineering).
Mô hình hoạt động: Hệ thống vận hành hoàn toàn trên nền tảng Docker Compose, mô phỏng môi trường dữ liệu thương mại điện tử thực tế. Dữ liệu đơn hàng, vận chuyển và hoàn trả được sinh tự động bằng thuật toán (Synthetic Data, Zero PII) có cài đặt có kiểm soát các vi phạm logic. Pipeline Python xử lý, kiểm tra chất lượng dữ liệu và nạp vào kho Star Schema trên PostgreSQL 16 Container. Hệ thống tích hợp các AI Agent chuyên trách để tự động chẩn đoán lỗi dữ liệu, tìm nguyên nhân gốc rễ (Root Cause Analysis) và đưa ra khuyến nghị vận hành có giải thích cho nhà quản lý.
Sản phẩm bàn giao: Repository GitHub đạt chuẩn Enterprise Git Flow, hạ tầng Docker 1-lệnh (docker compose up --build), tài liệu BA, mô hình Star Schema, pipeline ETL Idempotent, hệ thống AI Agents tích hợp và Dashboard trực quan.
2. Bối cảnh và lý do chọn đề tài
Trong thương mại điện tử, chi phí logistics ngược (đơn giao thất bại, hoàn hàng, thẩm định chất lượng, lưu kho hoàn trả) chiếm từ 10–25% giá trị hàng hóa nếu không được kiểm soát. Vấn đề cốt lõi không chỉ là trực quan hóa báo cáo, mà là năng lực phát hiện sớm dữ liệu sai lệch, định lượng rủi ro hoàn trả và giải thích rõ ràng nguyên nhân phát sinh chi phí để hỗ trợ can thiệp kịp thời.
2.1. Vấn đề thực tế cần giải quyết
Dữ liệu logistics rời rạc giữa đơn vị vận chuyển (3PL), kho bãi và hệ thống OMS/CRM.
Tỷ lệ giao thất bại và hoàn trả bị trễ nhịp giám sát; báo cáo thủ công không thể cảnh báo theo thời gian thực.
Dữ liệu đầu vào thường xuyên gặp lỗi cấu trúc: trùng mã, chi phí âm, sai lệch thứ tự thời gian (ngày hoàn trước ngày giao).
Các quyết định vận hành phụ thuộc vào cảm tính cá nhân, thiếu cơ chế giải thích nguyên nhân gốc rễ bằng dữ liệu và trợ lý thông minh.
2.2. Ý tưởng giải pháp
Hạ tầng Containerized: Đóng gói toàn bộ cơ sở dữ liệu PostgreSQL, luồng ETL và ứng dụng phân tích vào Docker để đảm bảo tính nhất quán trên mọi môi trường.
Quản trị chất lượng dữ liệu (Data Observability): Bẫy lỗi chủ động theo bộ quy tắc QC-001 đến QC-007, ghi vết kiểm toán vào data_quality_log và pipeline_run (Zero Silent Drop).
Ứng dụng AI Agent & Mô hình phân tích: Kết hợp giữa mô hình Machine Learning cổ điển (dự báo rủi ro hoàn trả) và các Large Language Model (LLM) Agent (chẩn đoán lỗi, truy vấn ngôn ngữ tự nhiên Text-to-SQL và tóm tắt đề xuất hành động).
3. Mục tiêu, câu hỏi phân tích và giá trị dự kiến
3.1. Mục tiêu tổng quát
Xây dựng một nền tảng dữ liệu containerized hoàn chỉnh, ứng dụng quy trình phân tích hiện đại và hệ thống AI Agent hỗ trợ theo dõi, đo lường và tối ưu hóa chu trình logistics ngược.
3.2. Mục tiêu cụ thể
Mô hình hóa quy trình logistics ngược chuẩn BPMN (As-Is / To-Be) và bộ tài liệu BA chi tiết.
Triển khai kiến trúc Docker Compose gồm 3 services tách biệt: Database Container, Data Engine Container và Dashboard UI Container.
Thiết kế kho dữ liệu Star Schema trên PostgreSQL 16, đảm bảo tính bất biến của Grain giữa 4 bảng Fact và 5 bảng Dimension.
Xây dựng pipeline ETL Idempotent (chạy lại nhiều lần an toàn) với bộ lọc bẫy lỗi Data Quality nghiêm ngặt.
Tích hợp cụm AI Agents:
DQ Diagnosis Agent: Giải thích nguyên nhân dữ liệu bị từ chối và đề xuất cách làm sạch dữ liệu nguồn.
Root-Cause Analysis Agent: Phân tích đa chiều tìm ra lý do chi phí hoàn trả tăng đột biến.
Decision Support Copilot: Trả lời truy vấn vận hành, chuyển đổi câu hỏi tự nhiên thành SQL và tóm tắt báo cáo điều hành.
Huấn luyện mô hình Machine Learning phân loại đơn hàng có nguy cơ giao thất bại / hoàn trả cao.
3.3. Câu hỏi phân tích trọng tâm
Tỷ lệ hoàn hàng biến động như thế nào theo thời gian và ngành hàng?
Đơn vị vận chuyển (Carrier) hoặc tuyến khu vực nào có tỷ lệ giao thất bại vượt ngưỡng cảnh báo chuẩn?
Chi phí hoàn trả tập trung lớn nhất ở phân khúc sản phẩm hay lý do hoàn trả nào?
Đặc trưng đơn hàng nào (COD, khung giờ đặt, khu vực, giá trị) có xác suất hoàn hàng cao nhất?
Biện pháp can thiệp vận hành nào cần được ưu tiên triển khai theo đề xuất của AI Agent?
4. Phạm vi, giả định và giới hạn
Môi trường: 100% Docker Containerized (PostgreSQL 16, Python 3.11, Streamlit). Loại bỏ hoàn toàn SQLite/Local host đơn lẻ. Ngoài phạm vi: Triển khai cụm Kubernetes (K8s) phân tán đa cụm server.
Dữ liệu: Dữ liệu mô phỏng chân thực (Synthetic Data, 1.200+ đơn, Zero PII) có cài cắm 3–5% lỗi logic kiểm thử. Ngoài phạm vi: Tích hợp trực tiếp API production của Shopee/Lazada/TikTok Shop thật do ràng buộc bảo mật.
AI Agents: Multi-Agent xây dựng trên LangGraph / CrewAI, sử dụng API LLM (Claude 3.5 Sonnet / OpenAI GPT-4o / Ollama Llama 3) kết hợp RAG và Semantic Caching. Ngoài phạm vi: Tự huấn luyện (Pre-train) mô hình Foundation LLM từ con số 0.
Machine Learning: Tự huấn luyện mô hình phân loại mới (XGBoost / LightGBM) trên tập dữ liệu logistics để dự báo rủi ro hoàn trả. Ngoài phạm vi: Mô hình Computer Vision quét ảnh bưu kiện bị hỏng tại kho.
Giao diện: Web Dashboard tương tác bằng Streamlit/Plotly nhúng trong Docker + Báo cáo Power BI Desktop kết nối Database Container qua cổng 5432. Ngoài phạm vi: Ứng dụng di động (Mobile App) cho shipper.
5. Kiến trúc tổng thể và Chi tiết công nghệ (Docker-Centric Architecture)
5.1. Kiến trúc phân tầng Multi-Container
Hệ thống vận hành thông qua docker-compose.yml bao gồm mạng nội bộ cô lập (sladss-network) và named volume (pgdata) đảm bảo dữ liệu không bị mất khi khởi động lại:

postgres_db (PostgreSQL 16-alpine): Cổng 5432
etl_service (Python 3.11-slim): Pipeline & Agents
web_dashboard (Streamlit + Plotly): Cổng 8501
5.2. Định nghĩa chi tiết các Container Services
Service postgres_db:
Image: postgres:16-alpine.
Nhiệm vụ: Lưu trữ toàn bộ 3 tầng dữ liệu (staging, warehouse, marts) cùng các bảng audit logs (pipeline_run, data_quality_log).
Cấu hình: Port forwarding 5432:5432 cho phép Power BI Desktop, DBeaver kết nối trực tiếp từ máy host. Thiết lập healthcheck: pg_isready để đảm bảo cơ sở dữ liệu đã sẵn sàng trước khi các service khác kích hoạt.
Service etl_service:
Build: Tự động build từ Dockerfile dựa trên python:3.11-slim.
Nhiệm vụ: Chạy script sinh dữ liệu, thực hiện xác thực chất lượng (DQ Validation), chuẩn hóa dữ liệu, nạp vào Star Schema và kích hoạt các pipeline chạy batch hoặc huấn luyện mô hình ML.
Service web_dashboard:
Build: Chạy ứng dụng Streamlit trên cổng 8501, đọc trực tiếp từ schema marts và tích hợp khung chat AI Decision Copilot.
6. Thiết kế chi tiết hệ thống AI: AI Agents & Machine Learning Models
6.1. Ma trận lựa chọn công nghệ: Tự Train mô hình vs Dùng LLM có sẵn
Bài toán / Tính năng
Hướng giải quyết
Thư viện / Công cụ
Yêu cầu huấn luyện
Dự báo rủi ro hoàn hàng (Return Risk Prediction)
Custom Supervised Machine Learning (Phân loại nhị phân)
scikit-learn, xgboost, lightgbm, imbalanced-learn (SMOTE)
BẮT BUỘC TRAIN MỚI trên tập dữ liệu lịch sử đơn hàng. Mô hình học trực tiếp các trọng số tương quan giữa order_value, cod_flag, region_id, carrier_id để xuất ra điểm rủi ro $P(\text{return})$.
Data Quality Diagnosis Agent
Agentic Workflow sử dụng mô hình ngôn ngữ lớn kết hợp Prompt Engineering & Rule-based Validation
langchain, langgraph (hoặc crewai), OpenAI API (gpt-4o-mini) hoặc mô hình Local mã nguồn mở qua ollama (llama3.1:8b)
KHÔNG TRAIN MỚI. Tận dụng khả năng suy luận logic có sẵn của LLM. Sử dụng kỹ thuật Few-shot Prompting kèm theo Data Quality Log làm ngữ cảnh đầu vào.
Root Cause Analysis (RCA) Agent
Retrieval-Augmented Reasoning Agent truy vấn Data Marts và phân tích bất thường
langgraph, duckdb, plotly export JSON
KHÔNG TRAIN MỚI. Sử dụng cơ chế Function Calling / Tool Calling để Agent tự động thực thi các câu SQL điều tra sâu vào kho dữ liệu.
Decision Support Copilot (Text-to-SQL & Recommender)
Semantic Routing & Tool-Using Agent
langchain-community, sqlalchemy, Pydantic để validate schema đầu ra
KHÔNG TRAIN MỚI. Sử dụng kỹ thuật In-Context Learning với sơ đồ DDL Star Schema được nạp trực tiếp vào System Prompt để sinh SQL chính xác.

6.2. Thiết kế chi tiết các AI Agents
Data Quality Diagnosis Agent (Giám sát & Bẫy lỗi dữ liệu):
Mục tiêu: Khi pipeline ghi nhận các bản ghi vi phạm vào staging.data_quality_log (QC-001: Null PK, QC-002: Negative values, QC-003: Date chronology violation, QC-004: Invalid enum, QC-005: Orphan FK), Agent sẽ phân tích nguyên nhân gốc của nguồn dữ liệu và sinh tài liệu đề xuất giải pháp cho đội Data Engineer.
Thư viện triển khai: LangChain / Pydantic.
Cơ chế hoạt động: Quét định kỳ các dòng có cờ lỗi mới trong bảng staging.data_quality_log; gom nhóm mã lỗi theo đối tác vận chuyển hoặc file nguồn; áp dụng template cấu trúc để giải thích: Vấn đề phát hiện $\rightarrow$ Tác động đến báo cáo $\rightarrow$ Hướng xử lý tự động (Data Imputation / Auto-rejection).
Root Cause Analysis (RCA) Agent (Phân tích nguyên nhân biến động KPI):
Mục tiêu: Tự động trả lời câu hỏi phân tích sâu nguyên nhân biến động chỉ số vận hành.
Thư viện triển khai: LangGraph (xây dựng đồ thị có trạng thái - StateGraph).
Quy trình suy luận: Node 1 (Anomaly Detection: phát hiện khi KPI vượt ngưỡng baseline 2 độ lệch chuẩn) $\rightarrow$ Node 2 (Data Mart Drill-down: thực thi SQL bóc tách theo dim_carrier, dim_region, dim_return_reason) $\rightarrow$ Node 3 (Synthesis & Recommendation: tổng hợp bằng chứng định lượng và đề xuất hành động vận hành).
Decision Support Copilot (Trợ lý điều hành & Text-to-SQL):
Mục tiêu: Cho phép cấp quản lý đặt câu hỏi bằng ngôn ngữ tự nhiên trên giao diện Web Dashboard, hệ thống tự động sinh SQL, thực thi an toàn và trả về câu trả lời kèm biểu đồ.
Thư viện triển khai: LangChain SQL Database Toolkit + Ollama / OpenAI.
Cơ chế bảo vệ: Chỉ cấp quyền READ ONLY trên schema marts; luôn sử dụng hàm NULLIF(denominator, 0) trong các view KPI để loại trừ lỗi chia cho 0.
6.3. Thiết kế mô hình Machine Learning: Dự báo nguy cơ hoàn đơn (Return Risk Predictor)
Bản chất kỹ thuật: Mô hình học máy phân loại nhị phân (Binary Classification) được huấn luyện mới từ dữ liệu lịch sử đơn hàng của kho dữ liệu.
Biến mục tiêu: is_returned $\in {0, 1}$.
Đặc trưng đầu vào: Thuộc tính đơn hàng (order_value, cod_flag, thời điểm đặt hàng), thuộc tính sản phẩm (danh mục ngành hàng), tỷ lệ hoàn lịch sử (region_historical_return_rate, carrier_delivery_failure_rate).
Quy trình huấn luyện: Tiền xử lý dữ liệu và cân bằng lớp bằng SMOTE; huấn luyện với XGBoost và LightGBM; đánh giá bằng PR-AUC, F1-Score, ROC-AUC; giải thích mô hình qua SHAP values.
7. Thiết kế dữ liệu và Mô hình kho dữ liệu (Star Schema trên PostgreSQL 16)
Mô hình kho dữ liệu gồm:

4 Fact Tables: fact_orders (Grain: 1 dòng/order), fact_shipments (Grain: 1 dòng/delivery attempt), fact_returns (Grain: 1 dòng/return event), fact_return_costs (Grain: 1 dòng/cost item).
5 Dimension Tables: dim_date, dim_product, dim_region, dim_carrier, dim_return_reason.
Nguyên tắc chống lỗi nhân dòng (Anti-Fanout Rule): Tuyệt đối KHÔNG JOIN trực tiếp giữa fact_orders, fact_shipments và fact_returns/fact_return_costs trong một câu truy vấn tính tổng khi chưa được tổng hợp độc lập về cùng cấp độ Grain.
8. Thiết kế Pipeline ETL và Quy chuẩn Chất lượng dữ liệu
8.1. Các bước trong Pipeline thực thi trên Docker
Extract (etl/extract.py): Đọc CSV nguồn với UTF-8.
Validate (etl/validate.py): Bẫy lỗi QC-001 đến QC-007, ghi log chi tiết vào staging.data_quality_log (Zero Silent Drop).
Transform (etl/transform.py): Ánh xạ sang Star Schema bảo toàn Grain.
Load (etl/load.py): Nạp dữ liệu vào PostgreSQL với cơ chế Idempotent.
Audit (etl/pipeline.py): Quản lý vòng đời và cập nhật staging.pipeline_run.
8.2. Danh mục 7 mã lỗi kiểm thử chất lượng (QC Rules)
QC-001: Khóa chính rỗng hoặc null.
QC-002: Số tiền hoặc chi phí hoàn có giá trị âm.
QC-003: Lỗi thứ tự thời gian logic (ngày hoàn trước ngày đặt).
QC-004: Trạng thái không hợp lệ ngoài enum.
QC-005: Khóa ngoại không tồn tại trong danh mục.
QC-006: Trùng lặp khóa nghiệp vụ.
QC-007: Sai lệch định dạng hoặc tiền tệ.
9. Cấu trúc Repository chuẩn Enterprise Git Flow
Cấu trúc Monorepo gồm:
data/sample/, docker-compose.yml, Dockerfile, docs/, etl/, ai_agents/, sql/, web_dashboard/, dashboard/, tests/, scripts/, .env.example, .gitignore, requirements.txt, README.md.
10. Kế hoạch triển khai 12 tuần
Tuần 1: Khởi tạo & Hiến pháp dự án (constitution.md)
Tuần 2: Phân tích nghiệp vụ BA (BRD, SRS, BPMN, Use Case)
Tuần 3: Hạ tầng Docker & DDL Database (PostgreSQL 16)
Tuần 4: Sinh dữ liệu mẫu (1.200+ đơn kèm 3-5% lỗi QC)
Tuần 5: Xây dựng pipeline ETL & Quản trị chất lượng dữ liệu
Tuần 6: Xây dựng Star Schema & SQL Data Mart Views
Tuần 7: Huấn luyện Custom ML Model (XGBoost/LightGBM) dự báo rủi ro hoàn
Tuần 8: Xây dựng AI Multi-Agent (LangGraph: DQ Agent, RCA Agent, Copilot)
Tuần 9: Phát triển Web Dashboard Streamlit tích hợp AI Chat
Tuần 10: Tích hợp báo cáo Power BI Desktop qua cổng 5432
Tuần 11: Kiểm thử toàn diện Pytest (100% Passed) & tối ưu hóa
Tuần 12: Đóng gói Portfolio, quay video demo và hoàn thiện CV
11. Hướng dẫn cài đặt và Khởi chạy thực tế (Docker Quickstart)
Clone repository từ GitHub và chuyển vào thư mục dự án.
Sao chép file cấu hình: cp .env.example .env
Khởi chạy toàn bộ hệ thống bằng 1 lệnh: docker compose up --build

Sau khi khởi chạy: PostgreSQL mở tại cổng 5432, Web Dashboard & AI Copilot truy cập tại http://localhost:8501, kiểm thử tự động qua lệnh pytest trong container etl_service.
12. Tài liệu tham khảo công nghệ chính thức
Docker & Docker Compose
PostgreSQL 16 Documentation
LangChain & LangGraph Framework
XGBoost & LightGBM Machine Learning
Streamlit Web Framework
Microsoft Learn — Power BI
GitHub Spec Kit


Kết luận
Bản báo cáo đề xuất đề tài SLADSS phiên bản 2.0 đã giải quyết triệt để sự thiếu hụt về mặt hạ tầng triển khai và ứng dụng trí tuệ nhân tạo. Bằng việc đưa Docker trở thành hạ tầng cốt lõi, loại bỏ hoàn toàn SQLite, tích hợp mô hình Machine Learning tùy chỉnh cùng hệ thống AI Multi-Agent chuyên trách, đề tài mang lại giá trị thực tiễn cao cho cả đào tạo và ứng dụng thực tế.
