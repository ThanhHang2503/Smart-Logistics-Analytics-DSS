# 🤖 AI Agents & Machine Learning Models (SLADSS v2.0)

Hệ thống Trí tuệ Nhân tạo hỗ trợ phân tích và ra quyết định trong Logistics ngược, tuân thủ nguyên tắc phân định công nghệ tại Mục 6 của Báo cáo đề tài v2.0:

---

## 1. Ma trận Phân định Công nghệ (Architecture Matrix)

| Phân hệ / Tác tử | Hướng giải quyết | Thư viện & Công cụ | Yêu cầu Huấn luyện |
|---|---|---|---|
| **Dự báo rủi ro hoàn đơn** *(Return Risk Predictor)* | Custom Supervised Machine Learning (Phân loại nhị phân) | `scikit-learn`, `xgboost`, `lightgbm`, `imbalanced-learn` (SMOTE), `shap` | **BẮT BUỘC TRAIN MỚI** từ dữ liệu lịch sử Data Warehouse để trích xuất xác suất $P(\text{return})$. |
| **Data Quality Diagnosis Agent** | Agentic Workflow + Structured Output | `langchain`, `pydantic`, OpenAI (`gpt-4o-mini`) / Ollama (`llama3.1:8b`) | **KHÔNG TRAIN MỚI**. Dùng LLM có sẵn + Few-shot Prompting với ngữ cảnh `staging.data_quality_log`. |
| **Root Cause Analysis (RCA) Agent** | Multi-step Reasoning Graph (StateGraph) | `langgraph`, `duckdb` / SQL tool calling, `plotly` export | **KHÔNG TRAIN MỚI**. Xây dựng đồ thị trạng thái bóc tách đa chiều khi KPI lệch $\mu \pm 2\sigma$. |
| **Decision Support Copilot** | Text-to-SQL & Operational Recommender | `langchain-community`, `sqlalchemy`, `pydantic` | **KHÔNG TRAIN MỚI**. In-context learning với DDL Schema, chỉ đọc `marts`, chống chia cho 0. |

---

## 2. Cấu trúc Module Dự kiến

```
ai_agents/
├── __init__.py
├── README.md
├── custom_ml/
│   ├── __init__.py
│   ├── train_risk_model.py     # Huấn luyện XGBoost/LightGBM + SMOTE
│   ├── predict_risk.py         # Inference module xuất xác suất P(return)
│   └── explainability.py       # Phân tích SHAP values
├── agents/
│   ├── __init__.py
│   ├── dq_diagnosis_agent.py   # Chẩn đoán lỗi QC-001 -> QC-007
│   ├── rca_agent.py            # LangGraph StateGraph điều tra nguyên nhân gốc
│   └── copilot_agent.py        # Text-to-SQL và tư vấn ra quyết định
└── prompts/
    ├── dq_diagnosis_prompt.py
    ├── rca_prompts.py
    └── text_to_sql_prompts.py
```

---

## 3. Quy chuẩn An toàn & Vận hành

1. **Text-to-SQL Guardrail**: Toàn bộ truy vấn SQL tự động chỉ được cấp quyền `SELECT` trên schema `marts`. Cấm mọi thao tác DDL hoặc DML (`INSERT`, `UPDATE`, `DELETE`, `DROP`).
2. **Division-by-Zero Protection**: Mọi phép tính tỷ lệ đều phải sử dụng `NULLIF(denominator, 0)`.
3. **Correlation vs. Causation**: Không đưa ra kết luận nhân quả tuyệt đối nếu chỉ dựa vào tương quan; mọi khuyến nghị đều phải có bằng chứng định lượng đi kèm.
