# 📓 Thư mục Notebooks (Exploratory Data Analysis)

## Nguyên tắc Kỹ thuật (Hiến pháp Dự án - Mục 2.2 & 3.1)

1. **CHỈ DÙNG CHO EDA**: Thư mục này chỉ phục vụ phân tích khám phá dữ liệu ban đầu, vẽ biểu đồ thử nghiệm hoặc kiểm tra phân phối dữ liệu.
2. **KHÔNG CHỨA LOGIC PIPELINE**: Toàn bộ logic trích xuất, kiểm tra chất lượng, biến đổi và nạp dữ liệu (ETL) bắt buộc phải được module hóa trong gói `etl/` để đảm bảo khả năng chạy lại tự động (reproducibility) và kiểm thử (testing).
3. **KHÔNG COMMIT KẾT QUẢ CÓ PII**: Mọi dữ liệu phân tích trong notebook phải là dữ liệu mô phỏng từ `data/sample/`.
