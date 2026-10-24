BÁO CÁO ĐỀ XUẤT ĐỀ TÀI PROJECT
SMART LOGISTICS ANALYTICS
& DECISION SUPPORT SYSTEM
Hệ thống phân tích dữ liệu và hỗ trợ ra quyết định trong logistics ngược



Định hướng portfolio cho sinh viên năm cuối ngành Công nghệ thông tin
Chuyên ngành Hệ thống thông tin





Phiên bản: 1.0 | Ngày lập: 19/10/2026


Mục lục nội dung
1. Tóm tắt đề tài
2. Bối cảnh và lý do chọn đề tài
3. Mục tiêu, câu hỏi và giá trị dự kiến
4. Phạm vi, giả định và giới hạn
5. Đối tượng sử dụng và kịch bản nghiệp vụ
6. Yêu cầu chức năng và phi chức năng
7. Chỉ số phân tích và quy tắc tính
8. Kiến trúc tổng thể và công nghệ
9. Thiết kế dữ liệu và mô hình kho dữ liệu
10. Thiết kế pipeline ETL/ELT
11. Phân tích nghiệp vụ: bộ tài liệu BA
12. Thiết kế dashboard và trải nghiệm người dùng
13. Phương pháp thực hiện và kế hoạch 12 tuần
14. Kiểm thử, đánh giá và tiêu chí nghiệm thu
15. Rủi ro, bảo mật và quản trị dữ liệu
16. Cấu trúc repository và quy trình Git
17. Sản phẩm bàn giao và cách trình bày portfolio
18. Hướng phát triển sau phiên bản đầu
19. Checklist bắt đầu triển khai
20. Tài liệu tham khảo công nghệ


1. Tóm tắt đề tài
Tên tiếng Việt: Hệ thống phân tích dữ liệu và hỗ trợ ra quyết định trong logistics ngược.
Tên tiếng Anh: Smart Logistics Analytics & Decision Support System (SLADSS).
Định hướng: xây dựng một sản phẩm portfolio kết hợp ba nhóm năng lực: phân tích nghiệp vụ (BA), phân tích dữ liệu (DA) và kỹ thuật dữ liệu (DE). Hệ thống mô phỏng bài toán doanh nghiệp thương mại điện tử cần theo dõi đơn hàng, đơn giao thất bại, hàng hoàn trả, chi phí phát sinh và hiệu quả của đơn vị vận chuyển.
Sản phẩm không chỉ hiển thị biểu đồ. Dữ liệu được nhập từ CSV hoặc API giả lập, kiểm tra và làm sạch bằng Python, lưu trong cơ sở dữ liệu, chuyển đổi sang mô hình kho dữ liệu, sau đó được phân tích bằng SQL và trình bày qua Power BI. Từ kết quả, hệ thống đưa ra các cảnh báo và khuyến nghị có giải thích.
Đối tượng thực hiện: một sinh viên hoặc nhóm nhỏ. Dữ liệu sử dụng trong phiên bản học tập là dữ liệu giả lập hoặc dữ liệu công khai đã được kiểm tra giấy phép; không dùng dữ liệu cá nhân thật.
Kết quả mong đợi: một repository có thể chạy lại, tài liệu nghiệp vụ, mô hình dữ liệu, pipeline ETL, dashboard, bộ kiểm thử, hướng dẫn cài đặt và bài thuyết trình demo.
2. Bối cảnh và lý do chọn đề tài
Trong hoạt động thương mại điện tử, đơn hàng không kết thúc ở thời điểm giao hàng. Một phần đơn có thể giao thất bại, bị từ chối nhận, đổi trả hoặc phải hoàn về kho. Những sự kiện này tạo thêm chi phí vận chuyển, kiểm tra hàng, lưu kho và xử lý hoàn tiền. Nếu dữ liệu bị phân tán giữa nhiều file hoặc hệ thống, nhà quản lý khó xác định khu vực, sản phẩm, thời điểm hay đơn vị vận chuyển nào tạo ra vấn đề.
Đề tài phù hợp với chuyên ngành Hệ thống thông tin vì kết hợp quy trình nghiệp vụ, dữ liệu, cơ sở dữ liệu, phần mềm và hỗ trợ ra quyết định. Đồng thời, đề tài có thể được trình bày theo từng vị trí tuyển dụng: BA nhấn mạnh tài liệu và quy trình; DA nhấn mạnh SQL, phân tích và dashboard; DE nhấn mạnh pipeline, kho dữ liệu và chất lượng dữ liệu.
2.1. Vấn đề cần giải quyết
Không có một góc nhìn thống nhất về số đơn, số đơn hoàn, tỷ lệ giao thất bại và chi phí hoàn.
Khó so sánh hiệu quả giữa khu vực, nhóm sản phẩm và đơn vị vận chuyển.
Dữ liệu đầu vào có thể thiếu, trùng, sai định dạng hoặc không nhất quán về trạng thái.
Báo cáo thủ công tốn thời gian và khó tái lập.
Quyết định cải thiện hoạt động thường dựa vào cảm nhận thay vì chỉ số và bằng chứng.
2.2. Ý tưởng giải pháp
Xây dựng một luồng dữ liệu có thể tái chạy: dữ liệu nguồn → kiểm tra và làm sạch → lưu vùng staging → chuyển đổi vào kho dữ liệu → truy vấn KPI → dashboard và khuyến nghị. Mỗi chỉ số phải có định nghĩa rõ ràng, mỗi khuyến nghị phải chỉ ra dữ liệu hoặc quy tắc làm căn cứ.
3. Mục tiêu, câu hỏi và giá trị dự kiến
3.1. Mục tiêu tổng quát
Thiết kế và xây dựng một hệ thống mẫu hỗ trợ theo dõi, phân tích và cải thiện hiệu quả xử lý đơn hàng hoàn trả bằng cách tích hợp phân tích nghiệp vụ, phân tích dữ liệu và kỹ thuật dữ liệu.
3.2. Mục tiêu cụ thể
Khảo sát và mô hình hóa quy trình giao hàng, giao thất bại và hoàn trả.
Xây dựng bộ yêu cầu chức năng, phi chức năng và mô hình dữ liệu.
Thiết kế cơ sở dữ liệu tác nghiệp và mô hình kho dữ liệu phục vụ phân tích.
Xây dựng pipeline xử lý dữ liệu có kiểm tra chất lượng và nhật ký lỗi.
Viết truy vấn SQL để tính KPI và phân tích theo thời gian, khu vực, sản phẩm, đơn vị vận chuyển.
Thiết kế dashboard cho người quản lý và viết báo cáo insight.
Xây dựng một số quy tắc cảnh báo/khuyến nghị có thể giải thích.
Đánh giá hệ thống bằng các ca kiểm thử và tiêu chí nghiệm thu.
3.3. Câu hỏi phân tích
1.Tỷ lệ hoàn hàng thay đổi như thế nào theo tháng?
2.Những khu vực hoặc đơn vị vận chuyển nào có tỷ lệ giao thất bại cao hơn mức tham chiếu?
3.Nhóm sản phẩm nào có chi phí hoàn trả lớn nhất?
4.Chi phí hoàn trả tập trung ở một số nguyên nhân hay phân tán?
5.Nhóm đơn nào nên được ưu tiên điều tra dựa trên tỷ lệ, số lượng và chi phí?
3.4. Giá trị dự kiến
Về học thuật và kỹ thuật: minh họa quy trình từ yêu cầu nghiệp vụ đến dữ liệu, phân tích và hệ thống hỗ trợ quyết định. Về thực tiễn mô phỏng: cung cấp góc nhìn tổng hợp giúp người quản lý xác định vấn đề cần ưu tiên. Đây là giá trị dự kiến của hệ thống mẫu; không được khẳng định đã tiết kiệm chi phí thực tế nếu chưa triển khai trong doanh nghiệp thật.
4. Phạm vi, giả định và giới hạn
Nội dung	Trong phạm vi phiên bản đầu	Ngoài phạm vi phiên bản đầu
Dữ liệu	CSV/API giả lập; đơn hàng, trạng thái, hoàn trả, chi phí, sản phẩm, khu vực, đơn vị vận chuyển	Tích hợp trực tiếp ERP/WMS/TMS doanh nghiệp thật
Phân tích	KPI, xu hướng, so sánh nhóm, phân tích nguyên nhân theo dữ liệu có sẵn	Dự báo nâng cao hoặc tối ưu vận tải quy mô lớn
Khuyến nghị	Quy tắc minh bạch, giải thích được	Tự động ra quyết định tài chính/vận hành không có người duyệt
Giao diện	Dashboard Power BI; có thể thêm giao diện web nhỏ	Ứng dụng thương mại đầy đủ, đa tenant
Bảo mật	Dữ liệu giả lập, biến môi trường, phân quyền cơ bản nếu có API	Tuân thủ toàn diện tiêu chuẩn doanh nghiệp
Triển khai	Chạy cục bộ bằng hướng dẫn hoặc Docker	Cam kết SLA production

Giả định: dữ liệu được tạo ra cho mục đích học tập; các chỉ số và khuyến nghị phụ thuộc vào chất lượng, độ đầy đủ và cách định nghĩa dữ liệu. Nếu dùng dữ liệu công khai, cần ghi rõ nguồn, giấy phép và giới hạn.
Nguyên tắc: không tạo ra kết luận kinh doanh như thể đó là kết quả của doanh nghiệp thật. Dùng nhãn “dữ liệu mô phỏng” trong dashboard và báo cáo.
5. Đối tượng sử dụng và kịch bản nghiệp vụ
Vai trò	Nhu cầu chính	Quyền/hoạt động
Quản lý vận hành	Theo dõi KPI tổng thể, phát hiện điểm bất thường	Xem dashboard, lọc theo thời gian/khu vực, đọc khuyến nghị
Chuyên viên phân tích	Truy vấn dữ liệu, kiểm tra nguyên nhân	Phân tích dữ liệu đã xử lý, xuất báo cáo
Nhân viên dữ liệu	Nạp dữ liệu, kiểm tra chất lượng	Chạy pipeline, xem log lỗi, xử lý dữ liệu lỗi
Quản trị hệ thống	Quản lý cấu hình và quyền truy cập	Cấu hình kết nối, tài khoản và nhật ký

5.1. Kịch bản chính
6.Người quản lý mở dashboard và chọn khoảng thời gian cần xem.
7.Hệ thống hiển thị tổng số đơn, số đơn hoàn, tỷ lệ hoàn và chi phí hoàn.
8.Người quản lý lọc theo khu vực hoặc đơn vị vận chuyển để tìm nhóm có chỉ số bất thường.
9.Người phân tích mở bảng chi tiết, kiểm tra các nguyên nhân và so sánh với giai đoạn trước.
10.Pipeline dữ liệu chạy theo lịch hoặc được kích hoạt thủ công; bản ghi lỗi được ghi log và không âm thầm biến mất.
11.Hệ thống tạo danh sách nhóm cần điều tra theo quy tắc đã định nghĩa, kèm số liệu giải thích.
6. Yêu cầu chức năng và phi chức năng
6.1. Yêu cầu chức năng
Mã	Yêu cầu	Mức ưu tiên	Tiêu chí hoàn thành
FR-01	Nạp dữ liệu từ CSV theo mẫu quy định	Must	Đọc được file hợp lệ, báo số dòng đọc thành công/lỗi
FR-02	Kiểm tra trường bắt buộc, kiểu dữ liệu, khóa và giá trị hợp lệ	Must	Dòng sai được đánh dấu và có lý do
FR-03	Lưu dữ liệu nguồn và dữ liệu đã chuẩn hóa	Must	Có thể truy vết nguồn và thời điểm nạp
FR-04	Tính KPI đơn hàng, giao thất bại, hoàn hàng và chi phí	Must	Kết quả khớp bộ dữ liệu kiểm thử đã biết
FR-05	Lọc dashboard theo thời gian, khu vực, sản phẩm, đơn vị vận chuyển	Must	Các biểu đồ thay đổi theo bộ lọc
FR-06	Xem chi tiết nhóm có tỷ lệ hoàn cao	Should	Có số lượng, mẫu số, tỷ lệ và chi phí
FR-07	Tạo cảnh báo theo ngưỡng hoặc mức tham chiếu	Should	Cảnh báo nêu rõ điều kiện kích hoạt
FR-08	Ghi nhật ký mỗi lần chạy pipeline	Must	Có thời điểm, số dòng, trạng thái, lỗi
FR-09	Xuất báo cáo dữ liệu tổng hợp	Could	Xuất CSV/XLSX hoặc ảnh/PDF dashboard
FR-10	Có tài liệu cài đặt và chạy lại	Must	Người khác làm theo README có thể chạy phiên bản demo

6.2. Yêu cầu phi chức năng
Mã	Yêu cầu	Cách kiểm tra
NFR-01	Tính đúng đắn	Đối chiếu KPI với dữ liệu nhỏ có kết quả tính tay
NFR-02	Khả năng tái lập	Chạy lại pipeline không tạo bản ghi trùng ngoài ý muốn
NFR-03	Khả năng bảo trì	Tách cấu hình, xử lý dữ liệu, SQL và dashboard
NFR-04	Khả năng quan sát	Có log, số dòng hợp lệ/lỗi và thông báo thất bại
NFR-05	Bảo mật cơ bản	Không commit mật khẩu/API key; dùng biến môi trường
NFR-06	Hiệu năng phù hợp demo	Đặt mục tiêu thời gian chạy trên bộ dữ liệu mẫu và ghi rõ môi trường
NFR-07	Dễ sử dụng	Tên KPI, đơn vị, bộ lọc và định nghĩa được mô tả rõ
NFR-08	Tính minh bạch	Mỗi cảnh báo/khuyến nghị có quy tắc và dữ liệu làm căn cứ

7. Chỉ số phân tích và quy tắc tính
Cần thống nhất định nghĩa KPI trước khi viết SQL. Ví dụ dưới đây là đề xuất; cần giữ cùng một định nghĩa xuyên suốt dữ liệu, truy vấn và dashboard.
KPI	Định nghĩa gợi ý	Lưu ý
Tổng đơn hàng	Số order_id duy nhất trong phạm vi thời gian	Chốt rõ theo ngày tạo đơn hay ngày hoàn tất
Số đơn giao thất bại	Số đơn có trạng thái giao thất bại theo quy tắc nghiệp vụ	Một đơn có thể có nhiều lần giao; cần chọn cấp đơn hay cấp lần giao
Tỷ lệ giao thất bại	Số đơn giao thất bại / số đơn đã có kết quả giao × 100%	Không dùng toàn bộ đơn chưa giao làm mẫu số
Số đơn hoàn	Số order_id duy nhất có sự kiện hoàn hợp lệ	Phân biệt hoàn hàng, hủy đơn và đổi hàng
Tỷ lệ hoàn	Số đơn hoàn / số đơn đủ điều kiện tính hoàn × 100%	Ghi rõ mẫu số và thời gian ghi nhận
Chi phí hoàn	Tổng chi phí hoàn trả của các bản ghi hợp lệ	Xác định có bao gồm phí vận chuyển hai chiều, kiểm tra và xử lý hay không
Chi phí hoàn trung bình	Tổng chi phí hoàn / số đơn hoàn	Nếu số đơn hoàn bằng 0, trả về NULL/không áp dụng
Thời gian xử lý hoàn	Thời điểm đóng quy trình hoàn − thời điểm bắt đầu hoàn	Chuẩn hóa múi giờ và xử lý bản ghi thiếu ngày

7.1. Quy tắc cảnh báo gợi ý
Cảnh báo nhóm vận chuyển khi tỷ lệ giao thất bại vượt ngưỡng cấu hình và có ít nhất N đơn quan sát.
Cảnh báo nhóm sản phẩm khi tỷ lệ hoàn vượt mức tham chiếu toàn hệ thống một khoảng nhất định.
Ưu tiên điều tra nhóm có chi phí hoàn cao; hiển thị đồng thời số đơn và tỷ lệ để tránh hiểu sai nhóm có ít đơn.
Không gắn nhãn nguyên nhân nhân quả nếu dữ liệu chỉ cho thấy mối liên hệ. Dùng cách diễn đạt “có liên quan” hoặc “cần điều tra thêm”.
8. Kiến trúc tổng thể và công nghệ
Kiến trúc đề xuất gồm bốn lớp: nguồn dữ liệu, xử lý/kiểm tra, lưu trữ và phân tích/hiển thị. Phiên bản đầu nên ưu tiên pipeline có thể chạy lại và KPI đúng trước khi xây thêm web frontend.
Lớp	Thành phần	Trách nhiệm
Nguồn	CSV/JSON hoặc API giả lập	Mô phỏng dữ liệu đơn hàng, vận chuyển, hoàn trả và chi phí
Ingestion & quality	Python, Pandas	Đọc dữ liệu, chuẩn hóa kiểu, kiểm tra quy tắc, ghi lỗi
Storage	PostgreSQL (hoặc MySQL)	Lưu staging, bảng chuẩn hóa và kho dữ liệu
Transformation	SQL và Python	Tạo bảng dimension/fact và dữ liệu tổng hợp
Orchestration	Script chạy thủ công trước; Airflow tùy chọn	Điều phối các bước theo thứ tự
BI	Power BI	Dashboard, KPI, bộ lọc và drill-down
API/UI tùy chọn	FastAPI; React nếu cần	Cung cấp dữ liệu cho giao diện quản lý
Delivery	GitHub, Docker, README	Quản lý phiên bản, chạy lại và trình diễn

8.1. Luồng xử lý
CSV/API → raw/staging → kiểm tra chất lượng → chuẩn hóa → data warehouse → SQL KPI/view → Power BI/dashboard → insight và khuyến nghị.
8.2. Quyết định công nghệ
Chọn một hệ quản trị cơ sở dữ liệu chính, không cần vừa dùng MySQL vừa PostgreSQL trong bản đầu.
Power BI là lựa chọn thực dụng cho portfolio DA; cần kiểm tra điều kiện cấp phép khi chia sẻ báo cáo trực tuyến.
FastAPI chỉ nên thêm khi cần chứng minh khả năng xây API hoặc muốn làm giao diện web; không bắt buộc để hoàn thành bản phân tích dữ liệu.
Airflow là phần mở rộng. Trước tiên cần có pipeline Python chạy được, có log và có thể chạy lại.
Docker giúp đóng gói môi trường; nên thêm sau khi các bước riêng lẻ hoạt động ổn định.
9. Thiết kế dữ liệu và mô hình kho dữ liệu
9.1. Các thực thể nghiệp vụ gợi ý
Thực thể	Trường tiêu biểu	Ý nghĩa
orders	order_id, order_date, customer_key giả lập, product_id, region_id, carrier_id, order_value	Đơn hàng
shipments	shipment_id, order_id, carrier_id, shipped_at, delivered_at, delivery_status	Thông tin giao hàng/lần giao
returns	return_id, order_id, return_date, return_reason, return_status	Sự kiện hoàn trả
return_costs	cost_id, return_id, cost_type, amount, currency	Chi phí liên quan đến hoàn
products	product_id, category, product_name	Danh mục sản phẩm
regions	region_id, region_name, province_or_area	Khu vực
carriers	carrier_id, carrier_name	Đơn vị vận chuyển
data_quality_log	run_id, source_file, row_number, rule_code, message	Lỗi dữ liệu
pipeline_run	run_id, started_at, ended_at, status, rows_read, rows_loaded	Lịch sử pipeline

Các trường định danh khách hàng trong dữ liệu demo phải là mã giả, không cần tên, số điện thoại hoặc địa chỉ thật.
9.2. Mô hình kho dữ liệu dạng Star Schema
Bảng fact lưu sự kiện hoặc số liệu đo lường; bảng dimension cung cấp ngữ cảnh để lọc và nhóm.
Bảng	Grain (mức chi tiết)	Trường chính gợi ý
fact_orders	Một dòng cho một đơn hàng	order_key, order_date_key, product_key, region_key, carrier_key, order_count, order_value
fact_shipments	Một dòng cho một lần giao	shipment_key, order_key, shipped_date_key, delivery_status_key, delivery_duration
fact_returns	Một dòng cho một sự kiện hoàn	return_key, order_key, return_date_key, reason_key, return_count
fact_return_costs	Một dòng cho một khoản chi phí	cost_key, return_key, cost_type_key, cost_amount
dim_date	Một ngày	date_key, date, day, month, quarter, year
dim_product	Một sản phẩm/phiên bản lịch sử nếu cần	product_key, product_id, category
dim_region	Một khu vực	region_key, region_id, region_name
dim_carrier	Một đơn vị vận chuyển	carrier_key, carrier_id, carrier_name
dim_return_reason	Một lý do hoàn chuẩn hóa	reason_key, reason_code, reason_name

Không cộng trực tiếp các fact có grain khác nhau trong một phép JOIN mà không kiểm tra nguy cơ nhân bản dòng. Ví dụ, một đơn có nhiều lần giao và nhiều khoản chi phí có thể làm tổng doanh thu hoặc chi phí bị nhân lên. Cần tổng hợp từng fact về cùng grain trước khi kết hợp.
9.3. Quy tắc chất lượng dữ liệu
Khóa chính không được rỗng hoặc trùng ngoài trường hợp được cho phép.
Ngày tháng phải parse được; ngày hoàn không được sớm hơn ngày tạo đơn nếu nghiệp vụ không cho phép.
Chi phí không âm, tiền tệ thống nhất.
Trạng thái phải thuộc danh mục được định nghĩa.
Khóa ngoại phải tham chiếu tới thực thể tồn tại hoặc được đưa vào bảng lỗi.
Mỗi bản ghi lỗi có mã quy tắc và lý do cụ thể; không tự ý xóa mà không ghi nhận.
10. Thiết kế pipeline ETL/ELT
10.1. Các bước pipeline
Bước	Đầu vào	Xử lý	Đầu ra
1. Extract	CSV/JSON	Đọc file, gắn run_id và nguồn	Raw records
2. Validate	Raw records	Kiểm tra cột, kiểu, null, phạm vi, khóa	Valid records + rejected records
3. Normalize	Valid records	Chuẩn hóa ngày, trạng thái, tên khu vực, tiền tệ	Staging tables
4. Load	Staging	Upsert hoặc nạp theo batch; chống nạp trùng	Operational/staging database
5. Transform	Staging	SQL tạo dimensions/facts và aggregate	Data warehouse
6. Test	Warehouse	Kiểm tra uniqueness, referential integrity, tổng số và KPI	Test results
7. Publish	Warehouse/views	Cập nhật dataset cho dashboard	Dashboard-ready data
8. Log	Tất cả bước	Ghi trạng thái, số dòng, thời gian, lỗi	pipeline_run + data_quality_log

10.2. Yêu cầu kỹ thuật
Pipeline phải có cấu hình kết nối qua biến môi trường, không ghi mật khẩu trực tiếp trong source code.
Chạy lại cùng một file không được tạo bản ghi trùng không kiểm soát; xác định khóa nghiệp vụ và chiến lược upsert.
Nếu bước chuyển đổi thất bại, ghi rõ bước lỗi và không đánh dấu toàn bộ pipeline thành công.
Lưu lại số dòng đầu vào, hợp lệ, bị loại và nạp thành công để dễ đối chiếu.
Tách logic xử lý khỏi notebook; notebook dùng cho khám phá dữ liệu, code pipeline nằm trong module có thể kiểm thử.
10.3. Pseudocode
run_pipeline(source_file):
    run_id = create_run_record(source_file)
    raw = extract(source_file)
    valid, rejected = validate_and_normalize(raw)
    write_rejected_rows(rejected, run_id)
    load_staging(valid, idempotent=True)
    transform_warehouse()
    run_data_quality_tests()
    publish_dashboard_dataset()
    finish_run_record(run_id, status="SUCCESS")

11. Phân tích nghiệp vụ: bộ tài liệu BA
Ngay cả khi ứng tuyển DA hoặc DE, phần tài liệu BA giúp chứng minh bạn hiểu lý do dữ liệu được thu thập và KPI được sử dụng như thế nào.
11.1. Problem statement
Người quản lý vận hành chưa có góc nhìn thống nhất về đơn giao thất bại, hàng hoàn và chi phí hoàn trả. Dữ liệu rời rạc khiến việc so sánh giữa khu vực, sản phẩm và đơn vị vận chuyển tốn thời gian. Hệ thống cần chuẩn hóa dữ liệu và cung cấp chỉ số có thể kiểm tra để hỗ trợ xác định nhóm cần điều tra.
11.2. User stories mẫu
Là quản lý vận hành, tôi muốn xem tỷ lệ hoàn theo tháng để nhận biết xu hướng tăng hoặc giảm.
Là quản lý vận hành, tôi muốn lọc theo khu vực và đơn vị vận chuyển để tìm nhóm có tỷ lệ giao thất bại cao.
Là chuyên viên phân tích, tôi muốn xem định nghĩa và mẫu số của mỗi KPI để diễn giải đúng.
Là kỹ sư dữ liệu, tôi muốn xem số dòng lỗi và lý do lỗi sau mỗi lần chạy để sửa nguồn dữ liệu.
Là người dùng dashboard, tôi muốn biết dữ liệu được cập nhật vào thời điểm nào để đánh giá độ mới.
11.3. Acceptance criteria mẫu
Khi người dùng chọn khoảng thời gian hợp lệ, các KPI chỉ tính những bản ghi thuộc khoảng thời gian và quy tắc ngày đã công bố.
Khi bộ lọc khu vực được thay đổi, toàn bộ biểu đồ liên quan phải cập nhật nhất quán.
Khi mẫu số bằng 0, tỷ lệ phải hiển thị “N/A” hoặc giá trị rỗng, không hiển thị lỗi chia cho 0.
Khi pipeline gặp bản ghi không hợp lệ, hệ thống phải ghi nhận số dòng và lý do, không âm thầm loại bỏ.
Mỗi cảnh báo phải hiển thị điều kiện kích hoạt, nhóm liên quan, số lượng quan sát và thời điểm dữ liệu.
11.4. Danh mục tài liệu BA nên bàn giao
Project charter / đề cương dự án.
Stakeholder map và mô tả persona.
Business requirements và functional requirements.
BPMN quy trình hiện tại (As-Is) và quy trình đề xuất (To-Be).
Use Case Diagram và mô tả các use case quan trọng.
SRS hoặc backlog User Stories + Acceptance Criteria.
ERD và data dictionary.
Wireframe dashboard hoặc prototype Figma.
Test scenarios / UAT checklist.
12. Thiết kế dashboard và trải nghiệm người dùng
12.1. Trang 1 — Tổng quan điều hành
Thẻ KPI: tổng đơn, số đơn hoàn, tỷ lệ hoàn, tỷ lệ giao thất bại, tổng chi phí hoàn.
Biểu đồ đường: xu hướng số đơn và tỷ lệ hoàn theo tháng.
Biểu đồ thanh: chi phí hoàn theo khu vực hoặc đơn vị vận chuyển.
Phân bố lý do hoàn hàng.
Bộ lọc: thời gian, khu vực, danh mục sản phẩm, đơn vị vận chuyển.
12.2. Trang 2 — Phân tích giao hàng
Tỷ lệ giao thành công/thất bại theo đơn vị vận chuyển.
Thời gian giao trung bình và phân phối thời gian giao.
Xem chi tiết theo khu vực và tháng.
Chỉ hiển thị so sánh khi số lượng quan sát đạt ngưỡng tối thiểu đã đặt.
12.3. Trang 3 — Phân tích hoàn trả và chi phí
Tỷ lệ hoàn theo danh mục sản phẩm và khu vực.
Top lý do hoàn theo số lượng và chi phí.
Chi phí hoàn trung bình trên mỗi đơn hoàn.
Bảng chi tiết có số lượng, tỷ lệ, chi phí và cảnh báo.
12.4. Quy tắc thiết kế
Đặt định nghĩa KPI trong trang thông tin hoặc tooltip.
Không dùng màu sắc làm tín hiệu duy nhất; thêm nhãn văn bản.
Luôn hiển thị kỳ dữ liệu và thời điểm cập nhật gần nhất.
Tránh chỉ trình bày Top N mà không cho biết quy mô mẫu.
Không tuyên bố nguyên nhân nếu chỉ có tương quan.
13. Phương pháp thực hiện và kế hoạch 12 tuần
Tuần	Công việc	Đầu ra kiểm chứng được
1	Chốt bài toán, mục tiêu, phạm vi, vai trò người dùng	Project charter, problem statement, scope
2	Yêu cầu nghiệp vụ, KPI, BPMN, Use Case	BRD/SRS bản đầu, sơ đồ quy trình
3	Thiết kế ERD, data dictionary, dữ liệu mẫu	ERD, schema nguồn, bộ CSV mẫu
4	SQL cơ bản và staging	DDL, truy vấn kiểm tra, nạp dữ liệu
5	Làm sạch dữ liệu và kiểm tra chất lượng bằng Python	Module validation, log lỗi
6	Viết SQL KPI và đối chiếu kết quả	SQL views, bộ kiểm thử KPI
7	Thiết kế Star Schema	Dimensions, facts, tài liệu grain
8	Xây dựng ETL/ELT và khả năng chạy lại	Pipeline chạy end-to-end
9	Xây dựng dashboard Power BI	Dashboard 3 trang và định nghĩa KPI
10	Viết quy tắc cảnh báo, phân tích insight	Danh sách cảnh báo và báo cáo phân tích
11	Kiểm thử, sửa lỗi, hoàn thiện README/Docker nếu đủ thời gian	Test report, hướng dẫn chạy
12	Demo, viết case study, chuẩn bị CV/phỏng vấn	Repository hoàn chỉnh, video/demo, portfolio

Nếu thời gian chỉ có 4–8 tuần, hãy giữ lại các phần cốt lõi: dữ liệu mẫu, SQL KPI, pipeline Python, dashboard và README. Có thể giảm số bảng, số trang dashboard và bỏ Airflow/React/Docker nâng cao.
14. Kiểm thử, đánh giá và tiêu chí nghiệm thu
14.1. Các nhóm kiểm thử
Nhóm	Ví dụ	Kết quả mong đợi
Kiểm thử dữ liệu	Thiếu order_id, ngày sai định dạng, chi phí âm	Bản ghi bị đánh dấu và có lý do
Kiểm thử pipeline	Chạy cùng file hai lần	Không nhân đôi dữ liệu ngoài quy tắc
Kiểm thử SQL	Bộ dữ liệu nhỏ với kết quả tính tay	KPI khớp kết quả kỳ vọng
Kiểm thử mô hình	Một đơn có nhiều shipment và nhiều cost	Không bị nhân tổng do JOIN
Kiểm thử dashboard	Chọn lọc thời gian/khu vực	KPI và biểu đồ cập nhật đúng
Kiểm thử lỗi	Database không kết nối được	Pipeline báo lỗi, ghi log, không báo thành công
Kiểm thử tài liệu	Người khác làm theo README	Có thể chạy demo mà không cần hỏi tác giả

14.2. Tiêu chí nghiệm thu tối thiểu
Có ít nhất một bộ dữ liệu mẫu được ghi rõ là dữ liệu mô phỏng.
Có tài liệu định nghĩa KPI và mẫu số.
Có thể chạy pipeline từ dữ liệu nguồn đến bảng phục vụ dashboard.
Có kiểm tra dữ liệu và nhật ký cho mỗi lần chạy.
Có ít nhất ba trang/nhóm phân tích hoặc một dashboard tương đương.
Có ít nhất năm insight được viết theo cấu trúc: quan sát → bằng chứng → diễn giải → hành động đề xuất.
Có test cho các KPI chính và trường hợp dữ liệu lỗi.
README nêu yêu cầu môi trường, cách cấu hình, cách chạy, cấu trúc thư mục và giới hạn.
15. Rủi ro, bảo mật và quản trị dữ liệu
Rủi ro	Tác động	Cách giảm thiểu
Dữ liệu giả lập quá đơn giản	Insight không có ý nghĩa	Tạo phân bố và trường hợp đa dạng; ghi rõ đây là dữ liệu demo
Định nghĩa KPI không thống nhất	Dashboard và SQL khác nhau	Dùng một data dictionary và bộ kiểm thử KPI
JOIN làm nhân số liệu	Tổng doanh thu/chi phí sai	Xác định grain, tổng hợp fact riêng trước khi JOIN
Phạm vi quá rộng	Không hoàn thành project	Chốt MVP, ưu tiên pipeline và dashboard trước
Lộ thông tin bí mật	Rủi ro tài khoản và dữ liệu	Dùng .env, .gitignore, secret scanning; không commit thông tin thật
Không tái lập được môi trường	Người tuyển dụng không chạy được	requirements.txt/pyproject, SQL setup, README; Docker nếu khả thi
Kết luận quá mức từ dữ liệu	Khuyến nghị sai lệch	Phân biệt tương quan với nguyên nhân; ghi giới hạn dữ liệu

Không đưa dữ liệu khách hàng thật, số điện thoại, địa chỉ, token, mật khẩu hoặc chuỗi kết nối có thông tin xác thực lên GitHub. Nếu vô tình commit secret, chỉ xóa khỏi file hiện tại là chưa đủ; cần thu hồi/đổi secret và xử lý lịch sử Git phù hợp.
16. Cấu trúc repository và quy trình Git
Có thể dùng một repository cho toàn bộ portfolio để người xem dễ hiểu luồng từ nghiệp vụ đến dữ liệu. Nếu muốn thể hiện FE/BE tách riêng, chỉ tách repo khi có API/frontend thực sự cần duy trì.
smart-logistics-analytics-dss/
├── docs/
│   ├── project-charter.md
│   ├── requirements/
│   ├── process/
│   ├── data-dictionary.md
│   └── architecture/
├── data/
│   ├── sample/              # chỉ dữ liệu demo, không chứa dữ liệu nhạy cảm
│   └── README.md
├── etl/
│   ├── extract.py
│   ├── validate.py
│   ├── transform.py
│   └── load.py
├── sql/
│   ├── ddl/
│   ├── staging/
│   ├── warehouse/
│   ├── marts/
│   └── tests/
├── notebooks/
│   └── exploratory_analysis.ipynb
├── dashboard/
│   └── README.md             # hướng dẫn mở file Power BI nếu có
├── tests/
├── scripts/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

16.1. Quy tắc làm việc với Git
Commit theo thay đổi nhỏ, có thông điệp rõ nghĩa, ví dụ: feat: add return-cost KPI.
Không commit .env, mật khẩu, token, file dữ liệu cá nhân hoặc file lớn không cần thiết.
Giữ file .env.example chỉ có tên biến và giá trị mẫu không bí mật.
README phải có hướng dẫn tạo database, nạp dữ liệu, chạy pipeline và xem dashboard.
Trước khi push, kiểm tra git status, git diff và các file chuẩn bị commit.
17. Sản phẩm bàn giao và cách trình bày portfolio
Sản phẩm	Nội dung tối thiểu
Repository	Source code, SQL, cấu hình mẫu, hướng dẫn cài đặt
Tài liệu BA	Problem statement, scope, BPMN, use case, requirements, acceptance criteria
Tài liệu dữ liệu	ERD, data dictionary, Star Schema, định nghĩa KPI
Pipeline	Mã chạy được, log, kiểm tra chất lượng, khả năng chạy lại
Dashboard	Ảnh chụp/ file PBIX nếu phù hợp, mô tả trang và KPI
Phân tích	Báo cáo insight và đề xuất dựa trên dữ liệu
Kiểm thử	Test cases, kết quả chạy, giới hạn còn tồn tại
Demo	Video 3–5 phút hoặc hướng dẫn thao tác từng bước

17.1. Cách viết project trong CV
Mẫu mô tả sau chỉ nên dùng sau khi bạn thực sự hoàn thành các phần tương ứng:
Smart Logistics Analytics & Decision Support System | Personal Project
- Designed business requirements, process flows, data dictionary and KPI definitions for reverse-logistics analysis.
- Built a Python ETL pipeline to validate, normalize and load sample order/return data into a relational database and analytical warehouse.
- Developed SQL metrics and a Power BI dashboard to analyze return rate, delivery failure and return cost by time, region, product and carrier.
- Added data-quality checks, pipeline logging and reproducible setup documentation.
Không tự ghi phần trăm cải thiện hiệu quả hoặc quy mô dữ liệu nếu chưa đo lường thật. Nếu dùng dữ liệu giả lập, ghi rõ “synthetic/sample data” khi trình bày.
18. Hướng phát triển sau phiên bản đầu
Thêm lịch chạy pipeline và thông báo thất bại bằng công cụ điều phối như Airflow.
Thêm kiểm thử dữ liệu tự động sâu hơn và báo cáo chất lượng theo ngày.
Thêm API bằng FastAPI nếu cần cung cấp dữ liệu cho giao diện web.
Thêm frontend React cho màn hình vận hành nếu mục tiêu portfolio cần thể hiện full-stack.
Thử mô hình dự báo tỷ lệ hoàn, nhưng phải tách dữ liệu train/test theo thời gian và so sánh với baseline.
Thử tối ưu hoặc xếp hạng ưu tiên xử lý; phải giải thích tiêu chí, kiểm tra thiên lệch và giữ người dùng ở bước quyết định cuối.
Không cần làm hết các hướng mở rộng để project có giá trị. Một phiên bản nhỏ, có kiểm thử và chạy lại được thường thuyết phục hơn một hệ thống lớn nhưng nhiều phần chỉ là giao diện mẫu.
19. Checklist bắt đầu triển khai
☐ Chốt tên đề tài, mục tiêu và phạm vi MVP.
☐ Viết problem statement và xác định người dùng chính.
☐ Chốt định nghĩa KPI trước khi tạo dashboard.
☐ Chọn PostgreSQL hoặc MySQL.
☐ Tạo dữ liệu mô phỏng có các trường hợp bình thường và lỗi.
☐ Thiết kế ERD và data dictionary.
☐ Khởi tạo repository, .gitignore và .env.example.
☐ Tạo staging schema và viết script nạp dữ liệu đầu tiên.
☐ Viết kiểm tra chất lượng dữ liệu.
☐ Viết truy vấn SQL cho KPI cốt lõi.
☐ Thiết kế Star Schema và kiểm tra grain.
☐ Xây dựng pipeline end-to-end có log và chạy lại an toàn.
☐ Tạo dashboard và kiểm tra bộ lọc.
☐ Viết ít nhất năm insight có bằng chứng và đề xuất.
☐ Viết test cases và đối chiếu KPI.
☐ Hoàn thiện README, ảnh demo và phần mô tả CV.
20. Tài liệu tham khảo công nghệ
Các liên kết dưới đây là tài liệu chính thức nên dùng khi triển khai. Hãy kiểm tra phiên bản hiện hành và yêu cầu cấp phép tại thời điểm sử dụng.
Python documentation: https://docs.python.org/3/
pandas documentation: https://pandas.pydata.org/docs/
PostgreSQL documentation: https://www.postgresql.org/docs/
MySQL documentation: https://dev.mysql.com/doc/
Microsoft Learn — Power BI: https://learn.microsoft.com/power-bi/
FastAPI documentation: https://fastapi.tiangolo.com/
Apache Airflow documentation: https://airflow.apache.org/docs/
Docker documentation: https://docs.docker.com/
Git documentation: https://git-scm.com/doc
Kết luận
Smart Logistics Analytics & Decision Support System là đề tài có thể mở rộng theo nhiều hướng nghề nghiệp nhưng vẫn có một bài toán thống nhất. Để hoàn thành tốt trong thời gian sinh viên năm cuối, nên tập trung vào phiên bản tối thiểu gồm tài liệu nghiệp vụ, dữ liệu mô phỏng, SQL, pipeline Python, kho dữ liệu cơ bản, dashboard Power BI và kiểm thử. Sau khi bản này chạy ổn định, mới cân nhắc API, frontend, Airflow hoặc mô hình dự báo.
Thước đo thành công không phải số lượng công nghệ, mà là khả năng giải thích bài toán, định nghĩa dữ liệu và KPI chính xác, chứng minh pipeline hoạt động, diễn giải insight có căn cứ và giúp người khác chạy lại được project.