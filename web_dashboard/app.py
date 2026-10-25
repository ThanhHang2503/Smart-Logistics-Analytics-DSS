"""
SLADSS Web Dashboard Entrypoint
===============================
Streamlit interactive dashboard for Reverse Logistics Analytics & AI Decision Copilot.
Runs in web_dashboard container on port 8501.
"""

import streamlit as st

st.set_page_config(
    page_title="SLADSS | Smart Logistics Analytics & DSS",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📦 Smart Logistics Analytics & Decision Support System (SLADSS)")
st.caption("Phiên bản 2.0 (Containerized & AI-Agent Integrated) | Dữ liệu mô phỏng (Synthetic Data)")

st.info(
    "Chào mừng đến với hệ thống SLADSS. Vui lòng chọn trang phân tích từ menu thanh bên (Sidebar) "
    "hoặc sử dụng khung chat AI Decision Copilot để bắt đầu truy vấn."
)

with st.sidebar:
    st.header("⚙️ Cấu hình Hệ thống")
    st.write("**Database:** PostgreSQL 16 Alpine Container (Port 5432)")
    st.write("**Analytics Engine:** Data Marts Schema")
    st.write("**AI Model:** Multi-Agent (LangGraph) + Return Risk ML")
