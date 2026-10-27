# CineTech AI — MVP tiếng Việt

Website: https://phamkhactruongbka-lab.github.io/cinetech-ai/

Repository: https://github.com/phamkhactruongbka-lab/cinetech-ai

Pages, CI và Research chạy thủ công đã thành công ngày 26/10/2026. Xem `DEPLOYMENT_REPORT.md` để biết bằng chứng và phần còn lại.

Website tĩnh về tin phim và thiết bị xem phim. Python chỉ dùng thư viện chuẩn; không cần API, không có dịch vụ trả phí, không cam kết doanh thu. Editor tạo bản nháp theo quy tắc, không phải LLM. Catalog có ba sản phẩm được đối chiếu nguồn nhà sản xuất; không có giá, đánh giá trải nghiệm hoặc affiliate.

## Chạy trên Windows (PowerShell)

Cài Python 3.12+ từ https://www.python.org/downloads/windows/ nếu chưa có. Mở PowerShell trong thư mục chứa README này:

```powershell
Set-Location 'D:\Codex\cinetech-ai-for-codex\cinetech-ai'
$env:PYTHONUTF8 = '1'
py -3 --version
py -3 -m unittest discover -s tests -v
py -3 agent/research.py
py -3 agent/validate.py
py -3 agent/editor.py
py -3 -m http.server 8000 --bind 127.0.0.1
```

Mở http://localhost:8000/docs/ . Dừng server bằng Ctrl+C. Nếu dùng thư mục khác, đổi dòng Set-Location. Có thể thay `py -3` bằng `python` khi Python trên PATH chạy được.

Trong phiên Codex này, đã chạy bằng runtime có sẵn tại:
`C:\Users\DRT\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`.
Nếu launcher chưa hoạt động, có thể dùng `& 'đường-dẫn-python.exe'` thay cho `py -3`. Runtime này thuộc Codex và đường dẫn có thể đổi khi cập nhật.

Kiểm tra JavaScript bổ sung nếu có Node.js:

```powershell
node --check docs/app.js
node --check docs/chooser.js
node tests/test_dom.cjs
```

## Duyệt và gỡ bài

Luồng: RSS → `data/research.json` → `data/drafts.json` → người đọc nguồn và sửa bản nháp → lệnh duyệt → `docs/data/published.json` → commit/deploy.

1. Mở `data/drafts.json`, chọn bản nháp, đọc `source_url`, đối chiếu tiêu đề, nội dung và quyền sử dụng. Có thể sửa `headline` và `draft` trong file này. Không sao chép toàn bài, không nhận là review đã trải nghiệm.
2. Chạy đoạn sau, nhập đúng ID và tên hiển thị người duyệt. Tên này lưu trong JSON công khai; dùng tên biên tập công khai nếu cần.

```powershell
$articleId = Read-Host 'ID bản nháp đã đọc và kiểm tra'
$reviewer = Read-Host 'Tên biên tập công khai'
py -3 agent/publish.py --id $articleId --reviewer $reviewer --confirm-reviewed
py -3 agent/validate.py
```

3. Tải lại trang để xem kết quả; khi có GitHub, kiểm tra diff rồi commit/push file `docs/data/published.json` bằng tài khoản của chủ dự án.
4. Gỡ bài cục bộ bằng `py -3 agent/publish.py --id $articleId --withdraw`, sau đó commit/push bản cập nhật.

Lệnh duyệt lưu bản chụp nội dung, thời điểm và người duyệt; sửa bản nháp không sửa bài đã đăng. Editor giữ nguyên bản nháp và phần sửa theo ID; giới hạn hàng chờ là 200 bản, bản mới được hoãn khi đầy. Hàng chờ biên tập có nguồn được lưu riêng trong data/review_queue.json. Workflow không gọi lệnh duyệt. Đây là kiểm soát vận hành cho một người, không phải hệ thống xác thực chống người có quyền sửa repository; cần bảo vệ branch và kiểm tra diff khi làm việc nhóm.

`data/` không được phục vụ bởi GitHub Pages khi chọn `/docs`, nhưng vẫn có thể đọc trong repository public. Không lưu dữ liệu nhạy cảm tại đây. HTTP server chạy từ gốc dự án chỉ dành cho loopback trên máy cá nhân.

## Catalog sản phẩm

File `docs/data/products.json`, schema `docs/data/products.schema.json` (JSON Schema 2020-12). Mỗi sản phẩm có `id` duy nhất, `name`, `category`, `source_name`, `source_url` HTTPS và `verified_at` ISO 8601 có múi giờ. `affiliate_url` có thể bỏ qua hoặc để null; chỉ thêm URL thật được chương trình chấp thuận. Không có trường giá/rating tự sinh. `py -3 agent/validate.py` kiểm tra các điều kiện quan trọng bằng thư viện chuẩn.

Chỉ điền catalog sau khi tự kiểm tra nguồn chính thức. Cập nhật tuyên bố trạng thái Affiliate ở trang chủ và trang chính sách khi có chương trình thật. Link affiliate được gắn `sponsored noopener noreferrer` và công bố hoa hồng cạnh link.

## Triển khai GitHub Pages

Chủ dự án đã xác nhận repository công khai `phamkhactruongbka-lab/cinetech-ai`, nhánh `main`, thư mục `/docs`. Xem `DEPLOYMENT_REPORT.md` để biết trạng thái triển khai thực tế.

1. Tạo repository public thuộc tài khoản của bạn để dùng GitHub Pages trên gói Free. Đưa **nội dung bên trong thư mục này** lên gốc repo, bao gồm `.github`, `agent`, `tests`, `data`, `docs`.
2. Trong Settings → Pages → Source chọn **Deploy from a branch**, chọn branch mặc định (thường `main`) và thư mục **/docs**, rồi Save.
3. Kênh liên hệ đã chọn là GitHub Issues của dự án; không gửi thông tin nhạy cảm vì đây là kênh công khai.
4. Khi có URL triển khai thật, tạo sitemap, không sử dụng domain ví dụ:

```powershell
$siteUrl = Read-Host 'URL HTTPS thật của GitHub Pages, gồm cả tên repository nếu có'
py -3 agent/configure_site.py --url $siteUrl
```

Commit/push `docs/sitemap.xml` và `docs/robots.txt`. Sitemap đã được cấu hình cho `https://phamkhactruongbka-lab.github.io/cinetech-ai/`; Pages đã triển khai thành công; kiểm tra lại sitemap nếu thay đổi tên repository hoặc domain. Với Pages dạng project, robots.txt nằm dưới đường dẫn project; crawler chỉ đọc robots.txt tại gốc origin. Muốn áp dụng quy tắc toàn host cần cấu hình tại site gốc hoặc domain riêng; có thể gửi sitemap thật trực tiếp cho công cụ tìm kiếm.

5. Mở Actions → Research phim moi → Run workflow trên branch mặc định. Kiểm tra log và diff hai file `data/`; website không có tin mới cho đến khi duyệt.
6. Lịch `15 2 * * *` là 09:15 giờ Việt Nam/Asia-Bangkok mỗi ngày; lịch có thể trễ hoặc bị vô hiệu khi repo public không hoạt động lâu. Xem trạng thái Actions thực tế.

Workflow mặc định `contents: read`; chỉ job cập nhật bản nháp có `contents: write`. CI cho PR chỉ đọc, không giữ credential checkout. Không cần dán PAT hoặc API key; dùng GITHUB_TOKEN tự cấp của Actions. Workflow commit đúng hai file dữ liệu, không force push; nếu có commit cạnh tranh hoặc branch protection chặn thì push thất bại an toàn, chạy lại sau khi đồng bộ hoặc dùng quy trình PR được quản trị viên chấp thuận. Không tự nới branch protection.

Tài liệu đã đối chiếu: [Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [schedule](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), [quyền GITHUB_TOKEN](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).

## Troubleshooting

| Hiện tượng | Cách xử lý |
| --- | --- |
| `python.exe` Windows Store không chạy | Cài Python chính thức, mở lại terminal, thử `py -3`; hoặc dùng runtime Codex đã nêu. |
| Lỗi ký tự tiếng Việt | Đặt `$env:PYTHONUTF8 = '1'` hoặc thêm `-X utf8` sau python. |
| RSS timeout/lỗi XML/rỗng | Xem warning; dữ liệu cũ được giữ nguyên, thử lại sau. Không có dữ liệu ban đầu thì UI hiển thị chưa có bài. |
| Không có bài trên website dù có 30 tin | Đúng thiết kế: cần người đọc và duyệt, không đăng tự động. |
| `fetch` lỗi khi mở HTML | Dùng HTTP server, không mở qua `file://`. |
| Port 8000 đã dùng | Chọn 8001 rồi mở URL tương ứng. |
| WinError 10013 trong môi trường hạn chế | HTTP test cần quyền kết nối loopback; cho phép đúng tiến trình theo chính sách môi trường, không tắt firewall toàn máy. |
| Actions 403/branch protected | Kiểm tra quyền job và quy tắc repo; dùng PR nếu bắt buộc, không force push. |
| Pages 404 | Kiểm tra branch, thư mục `/docs`, URL gồm tên repo, và log Pages. |
| Link nguồn hết hạn hoặc redirect | Mở và kiểm tra nguồn trước khi duyệt; URL HTTPS không bảo đảm nội dung đúng hoặc khả dụng mãi. |

## Trạng thái kiểm chứng

Xem `VERIFICATION.md` để phân biệt những gì đã chạy và phần phụ thuộc tài khoản bên ngoài. Không có analytics, doanh thu, tài khoản Affiliate, API hay LLM thật. Chưa thêm LLM vì MVP không cần và tránh phát sinh chi phí.

## Harness và quy trình Ngày 2

Xem `AGENT_HARNESS.md` cho vai trò agent, lệnh chạy và cơ chế phê duyệt; xem `EDITORIAL_REVIEW.md` để đọc ba bản nháp, `CATALOG_SOURCES.md` để kiểm tra nguồn sản phẩm. Các bản nháp do AI hỗ trợ biên tập trong phiên Codex; harness Python chỉ điều phối các bước xác định, không phải LLM tự viết bài.

```powershell
py -3.14 -X utf8 agent/harness.py
# Thu thập mới; báo lỗi và giữ dữ liệu cũ nếu không có tin mới:
py -3.14 -X utf8 agent/harness.py --collect
# Chỉ chạy sau khi đọc và duyệt bản cụ thể:
$articleId = Read-Host 'ID đã duyệt trong EDITORIAL_REVIEW.md'
$reviewer = Read-Host 'Tên biên tập công khai'
py -3.14 -X utf8 agent/publish.py --drafts data/review_queue.json --id $articleId --reviewer $reviewer --confirm-reviewed
```

Nếu `py` báo không tìm thấy Python, mở terminal mới hoặc dùng đường dẫn cài đặt trực tiếp: `& "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe" -X utf8 agent/harness.py`.
