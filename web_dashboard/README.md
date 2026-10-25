# 🌐 SLADSS Web Dashboard (Streamlit + Plotly)

Giao diện Web tương tác trực quan và Trợ lý AI Copilot của dự án SLADSS, phục vụ nhà quản lý vận hành logistics.

---

## Tính năng chính

1. **Giám sát KPI Logistics Ngược**:
   - Tỷ lệ giao thất bại (Delivery Failure Rate).
   - Tỷ lệ hoàn đơn (Return Rate) và Chi phí phát sinh (Return Cost).
   - Phân tích đa chiều theo Carrier, Region, Category và Return Reason.
2. **Khung Chat AI Decision Support Copilot**:
   - Truy vấn ngôn ngữ tự nhiên (Text-to-SQL) kết nối an toàn với schema `marts`.
   - Đề xuất giải pháp can thiệp vận hành dựa trên bằng chứng dữ liệu.
   - Hiển thị cảnh báo trực quan khi KPI vượt ngưỡng baseline ($\mu \pm 2\sigma$).

---

## Cấu trúc Thư mục

```
web_dashboard/
├── README.md
├── app.py                     # Entry point chính của ứng dụng Streamlit
├── components/                # UI components (KPI cards, charts, chat UI)
│   ├── chat_copilot.py
│   ├── kpi_cards.py
│   └── visual_charts.py
└── pages/                     # Multi-page dashboard
    ├── 1_Overview.py
    ├── 2_Carrier_Performance.py
    ├── 3_Cost_Analysis.py
    └── 4_Quality_Observability.py
```

---

## Khởi chạy qua Docker

Ứng dụng được đóng gói thành container `web_dashboard` chạy trên cổng 8501:

```bash
docker compose up --build web_dashboard
```

Truy cập tại: `http://localhost:8501`
