# Nguồn xác minh catalog — 27/10/2026

Catalog chứa ba bản ghi nhận diện sản phẩm theo nguồn chính thức của nhà sản xuất. Đây không phải bảng xếp hạng, đánh giá trải nghiệm hay khuyến nghị mua hàng. Việc có mặt trong catalog không xác nhận giá bán, tồn kho, phân phối tại Việt Nam hoặc khả năng tương thích với thiết bị cụ thể.

Các trang bên dưới đã được mở và đọc bằng công cụ duyệt web trong phiên này. Mốc kiểm tra dùng múi giờ Asia/Bangkok (UTC+07:00): `2026-10-27T08:24:59+07:00`. Đây là thời điểm kiểm tra nguồn, không phải ngày phát hành sản phẩm.

| Bản ghi | Trang chính thức đã mở | Bằng chứng nhận diện |
| --- | --- | --- |
| Sony WH-1000XM5 — Tai nghe | [Sony Electronics](https://electronics.sony.com/audio/headphones/headband/p/wh1000xm5-s) | Phần Product Details và tiêu đề sản phẩm xác định đây là headphones; trường Model ghi WH-1000XM5. Trang nguồn là biến thể màu bạc. |
| BenQ HT2060 — Máy chiếu | [BenQ US](https://www.benq.com/en-us/projector/cinema/ht2060.html) | Tiêu đề trang xác định HT2060 là home theater projector; phần sản phẩm hiển thị HT2060. |
| Sonos Beam (Gen 2) — Loa soundbar | [Sonos Support](https://support.sonos.com/en/article/set-up-your-sonos-beam) | Đoạn mở đầu xác định hướng dẫn dành cho Beam (Gen 2); mô tả hình gọi thiết bị là Sonos Beam soundbar. |

Các liên kết ban đầu đã thử nhưng không dùng làm nguồn catalog: [Sony URL cũ](https://www.sony.com/electronics/headband-headphones/wh-1000xm5) bị timeout; [Sonos cửa hàng](https://www.sonos.com/en-us/shop/beam) trả lỗi 429. Nguồn thay thế phía trên đều thuộc nhà sản xuất và đã đọc thành công, không lấy dữ liệu từ kết quả tìm kiếm của bên thứ ba.

`docs/data/products.json` chỉ lưu các trường của schema hiện có: ID, tên, nhóm, tên nguồn, URL nguồn, thời điểm kiểm tra và `affiliate_url: null`. Không đưa giá, điểm đánh giá, thông số quảng cáo hay tuyên bố trải nghiệm vào catalog. Chưa có liên kết tiếp thị hoặc quan hệ affiliate được xác nhận.

Kiểm tra dữ liệu: hàm `agent.validate.validate_catalog` chấp nhận đủ ba bản ghi; ID không trùng, URL nguồn dùng HTTPS, thời điểm có múi giờ và affiliate để null.
