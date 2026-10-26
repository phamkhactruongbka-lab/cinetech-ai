> Cập nhật 26/10/2026: báo cáo bên dưới ghi lại lần kiểm tra cục bộ ban đầu. GitHub Pages, CI và Research sau đó đã triển khai thành công; xem DEPLOYMENT_REPORT.md để biết trạng thái mới nhất.

# Kết quả xác minh — 26/10/2026

Đã đọc README, toàn bộ Python/HTML/CSS/JS/JSON, tests và workflow trong bản đầu; thực hiện thay đổi trực tiếp tại workspace. Không tạo hoặc sửa tài nguyên từ xa.

| Hạng mục | Kết quả thực tế |
| --- | --- |
| Test bản đầu | 3/5 đạt; lỗi encoding cp1252 và HTTP loopback bị sandbox chặn. |
| Python sau sửa | **20/20 đạt**, bao gồm HTTP, RSS timeout/XML lỗi/trùng/trống/quá lớn, fallback giữ nguyên file, URL, catalog, duyệt/gỡ bài và tạo sitemap qua CLI. |
| JavaScript | `node --check` cho app/chooser đạt; bộ kiểm thử DOM đạt: nội dung HTML được giữ dưới dạng text, URL nguy hiểm bị loại, chỉ bài approved hiển thị, disclosure affiliate và trạng thái trống/lỗi. DOM mock không thay thế browser security audit đầy đủ. |
| RSS trực tuyến | Chạy thành công, 30 tiêu đề từ Google News, 10 bản nháp; không có bài được tự đăng. Dữ liệu ghi trong `data/`. Không xác minh tính đúng đắn của từng bài báo hoặc mọi redirect nguồn. |
| Website | HTTP 200, đã mở trong trình duyệt cục bộ; trạng thái chưa có bài/sản phẩm đúng. Quan sát khung desktop 1280×900 và mobile 390×844 bằng iframe QA; tương tác đổi ngân sách/mục đích trong trình duyệt hoạt động. Không phải kiểm thử trên điện thoại vật lý. |
| Accessibility | Label điều khiển, heading, skip link, focus rõ, aria-live và reduced-motion đã có; chưa audit WCAG toàn diện/screen reader thực. |
| Catalog | JSON/schema và validator đã thêm, catalog thật còn rỗng; không tạo sản phẩm, giá, rating hoặc affiliate giả. |
| Duyệt bài | CLI và snapshot đã test với fixture trong thư mục tạm; dữ liệu xuất bản thật vẫn rỗng. Người có quyền sửa repo vẫn có thể sửa JSON, nên cần review/branch protection phù hợp. |
| SEO/chính sách | Có title/description, ngôn ngữ, sitemap generator, robots, Affiliate, quyền riêng tư và liên hệ. Sitemap hiện rỗng vì chưa có URL triển khai. Kênh liên hệ thật chưa được cung cấp. |
| Workflow | Hai YAML đã parse bằng PyYAML 6.0.3; kiểm tra quyền job, lịch, concurrency, timeout, danh sách file commit và không force push. Chưa có lần chạy Actions trên tài khoản người dùng; chưa xác minh branch protection/permission thực. |
| GitHub Pages | Có hướng dẫn đối chiếu tài liệu GitHub, chưa triển khai; workspace là thư mục nguồn chưa có `.git`/remote. Không có connector GitHub sẵn dùng trong phiên. |
| Chi phí/LLM/doanh thu | Không gọi API trả phí, không thêm LLM, không có analytics, doanh thu hoặc Affiliate được phê duyệt. |

## Thay đổi chính

- Research không ghi vào thư mục public; bỏ `docs/data/research.json` cũ. Timeout 20 giây, giới hạn RSS 2 MB, dedup theo tiêu đề và URL, ghi JSON nguyên tử, fallback giữ dữ liệu cũ.
- Không dùng assert làm validation production; kiểm tra rõ ràng kể cả khi Python chạy tối ưu.
- Lệnh publish yêu cầu ID, người duyệt và xác nhận đã kiểm tra; có gỡ bài; workflow chỉ cập nhật nghiên cứu và bản nháp.
- Frontend chỉ đọc published.json và dùng textContent, giới hạn HTTPS, noopener/noreferrer, sponsored với affiliate.
- Sửa navigation/chooser màn hình nhỏ; thêm các trang chính sách và tài liệu Windows tiếng Việt.

## Bằng chứng

- `evidence/python-tests.txt`, `evidence/dom-tests.txt`, `evidence/validation.txt`.
- `evidence/responsive.png`, `evidence/preview.html` (trang QA nằm ngoài `/docs`).
- Dữ liệu RSS đã thu thập: `data/research.json`; bản nháp: `data/drafts.json`.

## Việc chủ dự án cần hoàn tất

Xác nhận URL repository và quyền kết nối trước khi Codex thay đổi GitHub; cung cấp kênh liên hệ công khai; đọc và duyệt nội dung; bổ sung nguồn sản phẩm thật nếu cần. Sau triển khai, chạy configure_site với URL thật và kiểm tra Pages/Actions. Những phần này chưa thể xác minh bằng test cục bộ.

Preview server phục vụ QA đã được dừng khi bàn giao. Khởi động lại theo README để xem website.
