# Harness vận hành CineTech AI

## Vai trò và đầu ra

- Agent điều phối (Codex): đọc handoff và trạng thái thực, giao việc có phạm vi file riêng, review kết quả, chạy test, báo cáo.
- Agent biên tập: mở nguồn, viết tóm tắt ngắn có quy thuộc nguồn và ngày bài gốc; lưu data/review_queue.json cùng EDITORIAL_REVIEW.md. Không tự phê duyệt.
- Agent catalog: chỉ ghi tên sản phẩm, nguồn chính thức, thời điểm kiểm tra; không tạo giá/rating/affiliate giả.
- Agent pipeline: duy trì validate → draft → kiểm tra public/catalog, giữ nguyên nội dung sửa và ghi lỗi có timestamp.

Đây là cách dùng harness và các subagent của phiên Codex. Công cụ Python bên dưới chỉ điều phối tác vụ xác định, không chứa mô hình AI, không gọi API trả phí. Skill Sites dùng cho website; OpenAI Docs dùng để kiểm tra cơ chế tác vụ theo lịch. Không cần cài framework hoặc dịch vụ mới.

## Chạy lặp lại

Từ gốc dự án, chạy `py -3.14 -X utf8 agent/harness.py`. Báo cáo JSON nằm ở evidence/harness-latest.json, có started_at, finished_at, stages, status và publication_performed=false. Chạy thêm --collect nếu muốn thu thập RSS mới. Khi --collect không lấy được tin, harness báo failed và giữ file nghiên cứu cũ; lệnh research.py độc lập vẫn hỗ trợ fallback không lỗi như trước.

Hàng chờ draft được giữ theo ID, tối đa 200 mục; khi đầy, bản mới được hoãn, không xóa bản cũ. Người vận hành cần lưu trữ thủ công các mục không còn dùng. File hỏng sẽ bị từ chối trước khi ghi.

## Cổng phê duyệt

Research, Editor và harness không được sửa docs/data/published.json. Bài được đưa lên website chỉ bằng lệnh publish có --id, --reviewer và --confirm-reviewed sau khi con người đọc bản cụ thể. Hỗ trợ --drafts data/review_queue.json để đọc hàng chờ đã biên tập. Không coi yêu cầu triển khai website là duyệt tất cả bài.

## Điều kiện bàn giao mỗi vòng

Chạy Python unittest và Node DOM tests; kiểm tra harness report; kiểm tra nguồn và trạng thái needs_human_review; xác minh Git diff không chứa bí mật; báo rõ đã push/deploy hay chỉ hoàn tất local. Lỗi mạng không được coi là workflow lỗi, và lịch có cấu hình không có nghĩa đã chạy.

## Vận hành thử

Theo dõi website và Actions mỗi ngày lúc 09:00 giờ Asia/Bangkok (theo cấu hình automation kiểm tra ngày 27/10) trong một tuần. Ghi event thực tế, trạng thái, thời gian, lỗi mới và khoảng trống quan sát vào evidence/operations-log.md. Chỉ thông báo thay đổi đáng chú ý, lỗi mới, phục hồi hoặc yêu cầu hành động. Không tự đăng bài. Kết thúc tuần phải báo số lần đã quan sát, không suy đoán uptime từ số ít lần kiểm tra.

Tham khảo chính thức về tác vụ theo lịch: https://learn.chatgpt.com/docs/automations?surface=app .

