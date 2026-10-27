# Biên tập CineTech AI — hàng chờ duyệt ngày 27/10/2026

Đã mở và đọc ba bài nguồn, viết ba tóm tắt tiếng Việt mới trong `data/review_queue.json`. Mọi bản đều ở trạng thái `needs_human_review`; chưa phê duyệt, chưa đưa vào dữ liệu công khai. Mốc đối chiếu: 08:25 (UTC+7), 27/10/2026. "Đã đối chiếu" chỉ có nghĩa nội dung khớp bài báo đã mở, không có nghĩa mọi phát biểu của bài báo đã được xác minh độc lập.

| ID | Chủ đề | Ngày nguồn | Số từ |
|---|---|---|---|
| 03d36d87bd378350 | Phòng vé Trại buôn người | 26/10/2026 | 60 |
| 0eaea32abc3286be | Chương trình điện ảnh châu Á tại Tokyo | 26/10/2026 | 71 |
| 64e81650810f45d8 | Hồ sơ dự án điện ảnh AI của Bona | 06/10/2026 | 74 |

## Nội dung đề xuất

### 03d36d87bd378350 — Phòng vé Việt: Trại buôn người đạt mốc 484 tỷ đồng theo VOH

Theo VOH ngày 26/10/2026, Trại buôn người thu 484 tỷ đồng sau một tháng phát hành, xếp thứ ba trong bảng doanh thu phim Việt được bài báo dẫn. Tác phẩm đầu tay của Toni Dương Bảo Anh ra mắt ngày 25/9. Đây là số liệu tại thời điểm bài nguồn đăng, không phải doanh thu cập nhật trực tiếp.

[Nguồn VOH](https://voh.com.vn/phim-anh/trai-buon-nguoi-lot-top-3-phim-viet-an-khach-nhat-lich-su-675597.html). Chưa đối chiếu cơ sở dữ liệu phòng vé gốc; giữ quy thuộc nguồn và ngày chốt số liệu.

### 0eaea32abc3286be — Tokyo 2026 dành không gian cho các nhà làm phim châu Á mới

Bài viết ngày 26/10/2026 của Thể thao & Văn hóa giới thiệu Asian Future tại Liên hoan phim quốc tế Tokyo như nơi các nhà làm phim trẻ châu Á trình bày tác phẩm. Chương trình CROSSCUT ASIA+ cũng đưa điện ảnh Đông Nam Á đến khán giả Nhật Bản. Hai hoạt động mở thêm không gian trao đổi cho những câu chuyện và cách kể đa dạng trong khu vực.

[Nguồn Thể thao & Văn hóa](https://thethaovanhoa.vn/lhp-quoc-te-tokyo-2026-tham-vong-tro-thanh-cau-noi-dien-anh-toan-cau-20261026093550525.htm). Chưa đối chiếu lịch chiếu chính thức; không dùng bản này làm hướng dẫn đặt vé.

### 64e81650810f45d8 — Hồ sơ điện ảnh AI: dự án Gò Tam Tinh của Bona

Trong bài đăng ngày 6/10/2026, VietTimes giới thiệu Gò Tam Tinh: Chuyện tương lai của Bona là phim dài 100 phút, dùng hình ảnh do AI tạo và không có diễn viên người thật trên màn ảnh. Bài nguồn khi đó nêu lịch dự kiến ra rạp ngày 23/10. Đây là thông tin giới thiệu dự án trước phát hành; bản tóm tắt này không xác nhận doanh thu hay kết quả ra rạp.

[Nguồn VietTimes](https://viettimes.vn/trung-quoc-dua-phim-truyen-ai-khong-can-dien-vien-dau-tien-ra-rap-20-trieu-ndt-cho-cuoc-thu-lua-post206680.html). Đây là bài nền cũ hơn thay cho bài RSS Thế giới điện ảnh không tải được (Cache miss), không phải tin phòng vé mới. Nguồn ghi Theo Sohu; chưa mở được thông cáo gốc của Bona.

## Trước khi đăng

Người duyệt đọc nguồn, chốt tiêu đề/nội dung và xác nhận ID được phép đăng kèm tên người duyệt. Không tự gán tên người dùng vào trường phê duyệt. Không sao chép ảnh hoặc đoạn trích dài từ nguồn. File hàng chờ riêng tránh bị Research Agent ghi đè khi tạo bản nháp tự động.

Dữ liệu sử dụng các trường phù hợp với hàm `approve()`; ID là 16 ký tự đầu của SHA-256 UTF-8 của `source_url + headline`. CLI đã hỗ trợ `--drafts data/review_queue.json`; chỉ thực thi lệnh publish sau khi người dùng xác nhận ID và nội dung cụ thể.
