# Bộ câu hỏi đáp (G0, G1)

Hỏi theo **vòng ngắn**, mỗi tin nhắn tối đa khoảng 7 câu, có ví dụ trả lời và giá trị mặc định. Câu nào giảng viên chưa trả lời được thì ghi `❓` vào brief, không tự đoán.

## Vòng 1 · Ý tưởng và bối cảnh (G0)

| # | Câu hỏi | Ví dụ trả lời | Ghi vào |
|---|---|---|---|
| 1 | Khoá học tên gì (tạm)? Một câu: học xong, học viên **làm được gì**? | "Vibe Code phần mềm: người không biết code tự làm web, app" | BRIEF · Mục tiêu |
| 2 | Học viên là ai? Nghề, độ tuổi, đã biết gì, chưa biết gì? | "Chủ shop, giáo viên, nhân viên văn phòng; chưa từng code" | BRIEF · Học viên |
| 3 | Vì sao họ cần khoá này **bây giờ**? Họ đang đau ở đâu? | "Thuê dev đắt, chờ lâu" | BRIEF · Vấn đề |
| 4 | Khoá nằm ở đâu trong lộ trình của bạn (trước/sau khoá nào, bán kèm gì)? | "Sau workshop free, trước bootcamp nâng cao" | BRIEF · Bối cảnh |
| 5 | Thời lượng quay dự kiến? Quay một mạch hay nhiều buổi? | "Một mạch 3,5 giờ" | BRIEF · Ràng buộc |
| 6 | Hình thức học: tự học e-learning, có buổi live, có nhóm hỗ trợ? | "Tự học + nhóm Zalo" | BRIEF · Hình thức |
| 7 | Sản phẩm cuối khoá học viên mang về là gì? | "Một app chạy trên mạng có link" | BRIEF · Sản phẩm cuối |
| 8 | Khoá thuộc **đội ngũ Coachio** hay cần **thương hiệu riêng**? Nếu riêng: gửi logo, mã màu (hoặc website để lấy màu). | "Thương hiệu riêng, logo đính kèm" | book.json › brand (docs/THUONG-HIEU.md) |

## Vòng 1b · Tư liệu đã có (G0)

Xin **tất cả** những gì đã có, kể cả còn thô. Đọc hết trước khi viết brief.

| Loại | Ví dụ | Cách dùng |
|---|---|---|
| Bài giảng cũ | Video/transcript Zoom, ghi chú buổi dạy | Lấy ví dụ, câu chữ quen miệng của giảng viên, câu hỏi học viên hay hỏi |
| Mindmap | Ảnh mindmap, file XMind | Khung nhánh cho `mindmap.json`, kiểm tra dàn ý có thiếu nhánh nào |
| Tài liệu | Lark, Google Docs, Notion, PDF | Nội dung chính, prompt, quy trình |
| Slide cũ | Google Slides, PPTX | Thứ tự trình bày, hình minh hoạ |
| Case study | Sản phẩm học viên, dự án thật, ảnh chụp | Chương case, minh chứng |
| Repo/công cụ | GitHub, link sản phẩm mẫu | Tài nguyên tải về, bài thực hành |
| Câu hỏi học viên | Nhóm Zalo, form khảo sát | Mục "lỗi thường gặp", FAQ |
| Trang bán hàng | Landing page khoá | Lời hứa với học viên: nội dung phải giữ đúng lời hứa |

Ghi từng nguồn vào `TU-LIEU.md`: nguồn → có gì → độ tin cậy → dùng ở chương nào. Tài liệu của **giảng viên khác** ghi rõ tên để ghi công.

## Vòng 2 · Trọng tâm và đối tượng (G1)

| # | Câu hỏi | Lựa chọn |
|---|---|---|
| 1 | Bạn muốn nội dung **thiên về** hướng nào? | (a) Thuần kỹ thuật · (b) Dành cho người mới 100% · (c) Trung lập · (d) Cả hai: phần cơ bản cho người mới + phần nâng cao |
| 2 | Có được dùng cửa sổ lệnh, câu lệnh, code trong bài không? | Không / Có, giải thích kỹ / Có, tự nhiên |
| 3 | Mức độ sâu cuối khoá (Bloom)? | Hiểu và làm theo · Tự làm được sản phẩm của mình · Đánh giá, tối ưu, dạy lại người khác |
| 4 | Công cụ chính dùng trong khoá? Công cụ nào chỉ giới thiệu? | Ví dụ: chính Claude Code, Codex; phụ Antigravity |
| 5 | Phong cách giọng văn? | Thân mật "bạn" · Trang trọng · Hài hước nhẹ |
| 6 | Có phần nào của giảng viên khác? Ai phụ trách phần nào? | Ghi tên để đặt `teacher` cho từng phần |
| 7 | Có làm bản free cho workshop không? Landing page khoá trả phí là link nào? | Dùng ở G7 (nội bộ) |

## Vòng 3 · Chốt dàn ý (G2), chỉ hỏi khi cần

- Chương nào bạn muốn **demo trực tiếp** khi quay, chương nào chỉ giảng?
- Có case nào bắt buộc phải có? Có gì tuyệt đối không được nói/chiếu (khách hàng, số liệu nội bộ)?
- Phần nào muốn đưa vào bản free, phần nào chỉ cho học viên trả phí?
