# ==============================================================================
# Dockerfile - SLADSS Data Engineering Platform
# Base: Python 3.11 Slim (Debian based)
# ==============================================================================

FROM python:3.11-slim

# Thiết lập biến môi trường cho Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Cài đặt các gói phụ thuộc hệ thống cần thiết (build tools, libpq cho psycopg2, curl cho healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Sao chép file requirements.txt và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn dự án vào container
COPY . .

# Tạo các thư mục logs và data nếu chưa có
RUN mkdir -p logs data/sample

# Lệnh mặc định: Chạy kiểm thử xác thực môi trường
CMD ["python", "-m", "pytest", "-v"]
