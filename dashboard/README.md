# 📊 Dashboard & Báo cáo Hỗ trợ Ra Quyết định (SLADSS)

## Tổng quan Dashboard Power BI

Dashboard phục vụ người quản lý vận hành (Operations Manager) và chuyên viên phân tích (Data Analyst) nhằm theo dõi các chỉ số logistics ngược.

### Cấu trúc các trang báo cáo chính:
1. **Overview / Executive Summary**:
   - Tổng số đơn, số đơn hoàn, tỷ lệ hoàn trả (%) và tổng chi phí hoàn.
   - Xu hướng tỷ lệ hoàn theo tháng/quý.
2. **Carrier Performance Analysis**:
   - So sánh tỷ lệ giao thất bại và tỷ lệ hoàn theo từng đơn vị vận chuyển (`carrier_id`).
   - Cảnh báo các đơn vị vượt ngưỡng tham chiếu KPI (benchmark).
3. **Product & Cost Breakdown**:
   - Phân loại chi phí hoàn theo nhóm sản phẩm và lý do hoàn.
   - Ma trận ưu tiên xử lý (Impact vs. Cost).

---

## Hướng dẫn Mở và Kết nối File Power BI (.pbix)

1. Cài đặt **Power BI Desktop** (phiên bản mới nhất).
2. Mở file `.pbix` trong thư mục này (nếu có).
3. Cấu hình kết nối cơ sở dữ liệu:
   - Vào `Transform Data` -> `Data source settings`.
   - Cập nhật host/port/database theo cấu hình trong `.env` (PostgreSQL `sladss_db`).
4. Bấm `Refresh` để cập nhật dữ liệu mới nhất từ schema `warehouse` và `marts`.

> ⚠️ **LƯU Ý QUAN TRỌNG**:
> - Dashboard phải hiển thị rõ nhãn **"Dữ liệu mô phỏng / Synthetic Data"**.
> - Không commit credentials trong file `.pbix`.
