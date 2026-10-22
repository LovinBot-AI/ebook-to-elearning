# Thương hiệu (logo, màu) cho ebook và thumbnail

Hỏi **một lần ở vòng hỏi đáp G0**, dùng cho cả ebook (giao diện, bìa) và thumbnail video sau này.

## Câu hỏi đầu tiên

> Khoá này thuộc **đội ngũ Coachio** (dùng bộ nhận diện Coachio) hay cần **thương hiệu riêng**?

| Trả lời | Làm gì |
|---|---|
| Đội Coachio | Giữ nguyên bộ Coachio: navy, cam, xanh; logo Coachio. Không hỏi thêm. `e2e brand-apply <dir> --coachio` |
| Thương hiệu riêng đã từng làm | Tìm bộ đã duyệt (dự án cũ / thư viện brand của video-to-elearning), cho xem lại, hỏi "dùng lại bộ này?" |
| Thương hiệu mới hoàn toàn | Thiết kế bộ mới theo các bước dưới |

## Thương hiệu mới: hỏi trong MỘT tin nhắn

1. **Logo:** file PNG, nền trong suốt nếu có; có bản ngang càng tốt.
2. **Màu thương hiệu:** mã màu (#…), hoặc "lấy từ logo / website" → `e2e brand-colors <logo>` rút màu chính.
3. **Cảm giác mong muốn:** trẻ trung / chuyên nghiệp / sang trọng / thân thiện…
4. **Tên hiển thị** (ví dụ "Green Shop Academy") và **dòng nhỏ trên thumbnail** (ví dụ "KHOÁ HỌC ONLINE").
5. Tuỳ chọn: ảnh giảng viên hoặc mascot; vài thumbnail/bìa họ thích để tham khảo.

Chưa rõ thì hỏi thêm vài câu ngắn: logo đặt trên nền tối có đọc được không? muốn nhấn màu nào cho chữ nổi bật?

## Thiết kế, xem trước, duyệt

1. Viết `00-ke-hoach/brand-options.json` với **2–3 phương án** (mỗi phương án 4 màu: ink = chữ đậm/nền tối, primary = màu chính, accent = màu nhấn, accent2 = màu phụ; kèm một câu giải thích). Phương án A thường "giữ đúng màu logo", B "tối/sang hơn", C "sáng/trẻ hơn".
2. `e2e brand-preview <dir>` → `00-ke-hoach/brand-preview.html`: mỗi phương án có thumbnail mẫu, bìa ebook, trang ebook. Chụp ảnh gửi người dùng. **Chưa áp dụng gì.**
3. Người dùng chọn hoặc sửa → `e2e brand-apply <dir> --option A` → `e2e cover <dir>` → build lại web để xem trên trang thật.
4. Kiểm tra độ tương phản: chữ trắng trên `ink` và `primary` phải đọc rõ; `accent` dùng cho chữ nổi bật trên nền tối.

## Sang bước video

`e2e handoff` chuyển thương hiệu đã duyệt sang video-to-elearning (logo, màu, dòng chữ nhỏ). Ở đó **vẫn phải duyệt 1 thumbnail thử** trước khi làm cả bộ, vì thumbnail video là sản phẩm khác với trang xem trước.
