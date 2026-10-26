# CODEX HANDOFF — CINETECH AI

## Vai trò
Bạn là kỹ sư trưởng của CineTech AI. Tiếp tục từ code thực tế trong repository, không giả định các tính năng chưa kiểm tra đã hoạt động. Giao tiếp và tài liệu hướng dẫn bằng tiếng Việt.

## Mục tiêu kinh doanh
Công ty một người vận hành bằng các tác vụ/AI Agent; chi phí bổ sung mục tiêu 0 VND (người dùng có ChatGPT Plus, không bao gồm API credits). Website tiếng Việt về tin phim và thiết bị xem phim tại nhà; doanh thu kỳ vọng từ Affiliate và quảng cáo trong tương lai. Không cam kết thu nhập. Thiết bị của chủ dự án: Windows/laptop, có thể dành trên 3 giờ/ngày.

## Hiện trạng xác minh từ bản ZIP
Mã nguồn gồm: `agent/research.py`, `agent/editor.py`, `agent/validate.py`, `docs/index.html`, `docs/style.css`, `docs/app.js`, `docs/chooser.js`, `docs/data/research.json`, `data/research.json`, `data/drafts.json`, `.github/workflows/research.yml`, `tests/`, `README.md`.
- Website tĩnh responsive, hiển thị tiêu đề tin có nguồn; công cụ chọn thiết bị theo luật.
- Research Agent Python thu thập RSS Google News, lọc trùng và ghi JSON; chưa xác minh RSS trực tuyến trong môi trường triển khai.
- Editor tạo bản nháp theo quy tắc, KHÔNG phải LLM và KHÔNG tự đăng.
- GitHub Actions có cấu hình, chưa xác minh chạy trong repository người dùng.
- Chưa có domain/website công khai, AI API, tài khoản/link Affiliate được duyệt, doanh thu hay analytics thật.
- Bản trước báo cáo 5/5 kiểm thử cục bộ thành công; hãy tự chạy lại test và kiểm tra thực tế trước khi khẳng định.

## Nhiệm vụ Codex, theo thứ tự
1. Mở dự án, đọc README và toàn bộ mã nguồn, chạy `python -m unittest discover -s tests -v`, ghi nhận lỗi nếu có.
2. Kiểm tra website cục bộ: `python -m http.server 8000`, truy cập `http://localhost:8000/docs/`; xác minh giao diện desktop/mobile, XSS-safe DOM, liên kết nguồn.
3. Chạy `python agent/research.py`, `python agent/validate.py`, `python agent/editor.py`; kiểm tra dữ liệu và hành vi khi RSS lỗi, trùng, trống; không bịa nội dung review.
4. Sửa lỗi và tăng chất lượng: logging, timeout, xử lý lỗi, tests, accessibility, SEO cơ bản, sitemap, robots.txt, trang chính sách Affiliate, liên hệ/quyền riêng tư (không bịa thông tin liên hệ).
5. Thêm catalog sản phẩm bằng JSON có schema rõ ràng (tên, nguồn, thời điểm xác minh, URL affiliate tùy chọn). Không tự tạo link affiliate giả, không tự bịa giá/đánh giá.
6. Thiết kế cơ chế human approval cho bài viết; chỉ đăng nội dung được phê duyệt. Nếu thêm LLM, dùng cấu hình tùy chọn, không yêu cầu trả phí và không nhúng API key vào repo.
7. Xác minh GitHub Actions: quyền tối thiểu, workflow theo lịch, cập nhật dữ liệu và commit an toàn. Hướng dẫn triển khai GitHub Pages; nếu có quyền GitHub được kết nối thì đề nghị người dùng xác nhận repository và thao tác cần thiết trước khi thay đổi tài nguyên từ xa.
8. Viết hướng dẫn Windows dạng copy-paste, kèm troubleshooting và bảng phân biệt tính năng đã kiểm thử/chưa kiểm thử.

## Quy tắc bắt buộc
- Không giả vờ đã xem phim, thử sản phẩm hoặc có dữ liệu doanh thu.
- Không tải/cắt phim trái phép, không đăng hàng loạt nội dung rác, tôn trọng điều khoản nguồn RSS/API.
- Không tự chi tiền, kích hoạt dịch vụ trả phí hoặc công bố thông tin nhạy cảm.
- Không yêu cầu người dùng dán mật khẩu/token vào chat; dùng secrets của GitHub khi cần.
- Khi không có quyền truy cập tài khoản GitHub, hoàn thiện mọi phần cục bộ có thể, rồi nêu đúng bước kết nối còn thiếu.

## Tiêu chí bàn giao
- Tests pass; hướng dẫn chạy local Windows rõ ràng; website render đúng; RSS có fallback; nội dung không tự đăng; CI cấu hình hợp lệ; file ZIP/repo sẵn sàng triển khai.
- Báo cáo cụ thể những gì đã thực sự chạy, những gì chỉ được cấu hình và các việc phụ thuộc tài khoản bên ngoài.

## Bắt đầu ngay
Hãy audit dự án hiện có, chạy test, sửa lỗi ưu tiên cao và tiếp tục xây MVP có thể triển khai. Không chỉ đưa kế hoạch; hãy trực tiếp chỉnh sửa code trong workspace.
