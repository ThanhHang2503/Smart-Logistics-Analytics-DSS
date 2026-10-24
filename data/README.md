# 📦 Dữ liệu Mẫu (Data Directory)

## Chính sách Dữ liệu (BẤT BIẾN theo Hiến pháp Dự án)

1. **100% Mock / Synthetic Data**: Toàn bộ dữ liệu trong thư mục này là dữ liệu mô phỏng được sinh ra cho mục đích kiểm thử và học tập.
2. **Không chứa thông tin cá nhân (Zero PII)**: Trường `customer_key` được mã hóa/giả lập ngẫu nhiên (UUID hoặc mã hash giả định), không chứa họ tên, số điện thoại, địa chỉ thực tế.
3. **Phân cấp thư mục**:
   - `data/sample/`: Nơi lưu các file CSV dữ liệu mẫu được phép commit lên Git phục vụ việc chạy lại pipeline.
   - `data/raw/` (đã gitignore): Thư mục chứa dữ liệu thô cục bộ (nếu có).
   - `data/processed/` (đã gitignore): Thư mục chứa dữ liệu trung gian cục bộ.

## Cách tạo mới dữ liệu mẫu

Sử dụng tiện ích tự động:
```bash
python scripts/generate_sample_data.py
```
File CSV sẽ được sinh tự động vào `data/sample/`.
