# Framework thiết kế bài giảng dùng trong skill

Không cần dùng hết. Mỗi framework trả lời **một câu hỏi** ở **một bước** của quy trình. Ghi framework đã chọn vào `THIET-KE.md`.

| Bước | Câu hỏi | Framework |
|---|---|---|
| Cả quy trình | Làm theo thứ tự nào, lặp lại ra sao? | ADDIE (khung lớn), SAM (vòng lặp nhanh) |
| G1 · Mục tiêu | Học xong học viên làm được gì, đo bằng gì? | Backward Design, Bloom |
| G1 · Nội dung cần thiết | Kiến thức nào thực sự cần để làm được việc? | Action Mapping |
| G2 · Cấu trúc chương | Một chương nên đi theo nhịp nào? | Merrill's First Principles, Gagné 9 sự kiện |
| G2 · Độ dài, chia nhỏ | Mỗi đoạn dài bao nhiêu, trình bày thế nào để không quá tải? | Cognitive Load, Mayer (đa phương tiện) |
| G2 · Kỹ năng phức tạp | Dạy một quy trình nhiều bước thế nào? | 4C/ID (nhiệm vụ trọn vẹn) |
| G4 · Thực hành | Bài tập nào giúp nhớ lâu? | Kolb (học qua trải nghiệm), luyện truy xuất |
| Sau khoá | Khoá có hiệu quả không? | Kirkpatrick 4 cấp |

## ADDIE và SAM: khung quy trình

- **ADDIE:** Analyze (phân tích) → Design (thiết kế) → Develop (biên soạn) → Implement (triển khai) → Evaluate (đánh giá). Skill này đi đúng nhịp đó: G0–G1 là Analyze/Design, G2–G4 là Develop, G5 chuẩn bị Implement (quay), Kirkpatrick là Evaluate.
- **SAM (Successive Approximation Model):** làm bản phác nhanh, xem, sửa, lặp lại. Vì vậy có G2 (phác thảo) và G3 (một chương mẫu) trước khi viết hết: sửa trên bản nháp rẻ hơn sửa trên bản hoàn chỉnh.

## Backward Design (Wiggins & McTighe)

Bắt đầu từ **đích đến**, không bắt đầu từ nội dung:

1. **Kết quả mong muốn:** học xong, học viên làm được gì?
2. **Bằng chứng:** nhìn vào đâu để biết họ làm được (sản phẩm, bài tập, câu trả lời)?
3. **Kế hoạch học:** mới đến lúc chọn nội dung, ví dụ, bài giảng.

Áp dụng: mỗi chương mở bằng "**Sau chương này, bạn làm được:**" và kết bằng checklist "Trước khi sang chương sau" (chính là bằng chứng).

## Bloom (bản sửa đổi): động từ cho mục tiêu

| Mức | Động từ gợi ý | Ví dụ mục tiêu |
|---|---|---|
| Nhớ | liệt kê, gọi tên | Gọi tên sáu thành phần của một phần mềm |
| Hiểu | giải thích, so sánh | Giải thích API bằng ví dụ đời thường |
| Áp dụng | làm theo, sử dụng | Dùng prompt mẫu để tạo bản xem thử giao diện |
| Phân tích | chia nhỏ, tìm nguyên nhân | Phân tích một sản phẩm theo khung 6 thành phần |
| Đánh giá | chọn, phản biện | Chọn luồng làm phù hợp cho ý tưởng của mình |
| Sáng tạo | thiết kế, tự làm | Tự làm và đưa lên mạng một sản phẩm của mình |

Khoá cho người mới: phần lớn mục tiêu ở mức **Áp dụng**, kết thúc bằng một dự án ở mức **Sáng tạo**. Tránh động từ không đo được như "biết", "nắm được".

## Action Mapping (Cathy Moore)

Hỏi lần lượt:

1. Mục tiêu thật (kinh doanh/cá nhân) của khoá là gì?
2. Để đạt mục tiêu đó, học viên phải **làm** những hành động nào?
3. Với mỗi hành động: cần **luyện tập** gì để làm được?
4. Chỉ giữ lại **kiến thức tối thiểu** cần cho bài luyện tập đó.

Dùng để **cắt bớt**: phần lý thuyết nào không phục vụ một hành động thì chuyển xuống phụ lục hoặc bỏ. Đây là công cụ chính để ép 3–4 giờ video không bị lan man.

## Merrill's First Principles

Một chương tốt xoay quanh **một vấn đề thật**, đi qua bốn pha:

| Pha | Trong ebook / khi quay |
|---|---|
| Kích hoạt (Activation) | Gợi lại điều học viên đã biết, ví dụ đời thường |
| Trình diễn (Demonstration) | Giảng viên làm mẫu: demo, ảnh chụp, prompt mẫu |
| Áp dụng (Application) | Học viên tự làm theo: bài tập, prompt điền chỗ trống |
| Tích hợp (Integration) | Áp vào sản phẩm của chính mình, chia sẻ kết quả |

## Gagné: 9 sự kiện dạy học

Dùng làm nhịp cho **một đoạn video** hoặc một chương:

1. Thu hút chú ý (vấn đề, câu hỏi, kết quả cuối) · 2. Nêu mục tiêu · 3. Gợi kiến thức cũ · 4. Trình bày nội dung · 5. Hướng dẫn (ví dụ, sơ đồ) · 6. Cho thực hành · 7. Phản hồi · 8. Đánh giá · 9. Giúp nhớ lâu và áp dụng.

Trong `KICH-BAN-QUAY.md`, mỗi đoạn quay có ít nhất: (1) mở bằng vấn đề, (2) mục tiêu, (4–5) nội dung + demo, (6) giao bài, (9) tóm tắt.

## Cognitive Load và nguyên tắc Mayer

- **Chia nhỏ (segmenting):** mỗi bài video 5–12 phút, mỗi chương 4–8 mục.
- **Báo hiệu (signaling):** tiêu đề rõ, bảng, in đậm ý chính, sơ đồ.
- **Bớt thừa (coherence):** bỏ chuyện lan man, nhạc nền khi giảng, hình trang trí.
- **Kênh đôi (modality):** khi quay, nói giải thích + màn hình minh hoạ; không đọc nguyên văn chữ trên màn hình.
- **Ví dụ đã làm sẵn (worked example):** người mới học nhanh hơn khi thấy bài mẫu làm xong từng bước trước khi tự làm.
- **Cá nhân hoá:** giọng "bạn", thân mật, ngắn gọn.

## 4C/ID: dạy kỹ năng phức tạp

Cho quy trình dài (ví dụ ý tưởng → PRD → thiết kế → code → deploy): cho học viên làm **trọn một nhiệm vụ nhỏ từ đầu đến cuối** trước, rồi tăng dần độ khó, thay vì học rời từng bước mà không thấy toàn cảnh. Trong ebook: bài tập đi từ "mini tool một buổi" đến "sản phẩm đầy đủ".

## Kolb và luyện truy xuất

- Vòng Kolb: trải nghiệm → suy ngẫm → rút ra nguyên tắc → thử lại. Mỗi bài tập có **phiếu tự đánh giá** (đã làm được gì, vướng gì, lần sau làm khác gì).
- Luyện truy xuất: câu hỏi kiểm tra cuối buổi trong giáo án, checklist cuối chương, bài tập lặp lại kỹ năng cũ ở chương sau.

## Kirkpatrick: đánh giá sau khoá

| Cấp | Đo gì | Gợi ý công cụ |
|---|---|---|
| 1 Phản ứng | Học viên có thích, thấy dễ hiểu? | Form 3 câu cuối khoá |
| 2 Học được | Có làm được bài tập? | Checklist, sản phẩm nộp |
| 3 Hành vi | Có áp dụng vào công việc? | Hỏi lại sau 2–4 tuần |
| 4 Kết quả | Có kết quả kinh doanh/cá nhân? | Case học viên cho bản sau |

## Khi nào dùng gì (tóm tắt cho Claude)

- Luôn: Backward Design + Bloom (mục tiêu) và Action Mapping (cắt bớt).
- Chương hướng dẫn làm: Merrill. Đoạn video: Gagné rút gọn.
- Người mới: Mayer + worked example + glossary bắt buộc.
- Quy trình nhiều bước: 4C/ID (dự án nhỏ trọn vẹn trước).
- Sau khoá: gợi ý form Kirkpatrick cấp 1–2 trong phụ lục giáo án.
