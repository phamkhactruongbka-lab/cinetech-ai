# Vận hành liên tục có bằng chứng

GitHub Pages phục vụ website tĩnh liên tục theo dịch vụ GitHub. Trang phòng ban
đọc số liệu công khai khi tải lại và kiểm tra kết quả Actions qua API công khai.
Nó không có máy chủ ứng dụng, CRM hay kết nối ngân hàng, vì vậy không được gọi
là bảng điều khiển tiền mặt thời gian thực.

Workflow `Monitor public site` kiểm tra trang chủ và `published.json` mỗi 15
phút, lệch khỏi đầu giờ để giảm khả năng bị dồn lịch. Một lần chạy `success`
chỉ xác nhận hai endpoint ở thời điểm đó; không chứng minh uptime giữa các lần
kiểm tra. Nếu workflow bị chậm hoặc không chạy, trang phải hiện trạng thái
không xác minh thay vì hiển thị màu xanh.

Chỉ số tiền, đơn hàng và phản hồi khách được cập nhật sau bằng chứng thật trong
thư mục kinh doanh riêng. Không đưa tên lead, email, bản nháp chào hàng hoặc
chi tiết giao dịch lên repository public.
