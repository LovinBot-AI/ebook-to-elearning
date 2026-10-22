# Phong cách viết chương (rút từ ebook Vibe Code phần mềm, 10/2026)

## Khung một chương

```markdown
# Chương 7 — Ý tưởng và research: biết mình làm gì trước khi làm

Một đoạn mở 2–3 câu: chương này giải quyết vấn đề gì, vì sao quan trọng.

**Sau chương này, bạn làm được:** 2–3 việc đo được (động từ Bloom).

![Mô tả hình](ebook-assets/diagrams/ten-hinh.svg)

*Hình 7.1 — Chú thích một câu.*

## 7.1. Tên mục (danh từ hoặc động từ + kết quả)

Nội dung ngắn, ưu tiên bảng và danh sách.

> Prompt mẫu để học viên sao chép (blockquote không có chữ đậm ở đầu = ô PROMPT có nút Sao chép).

> **Mẹo:** một mẹo ngắn.

## Trước khi sang Chương 8

- [ ] Việc 1 tôi đã làm được.
- [ ] Việc 2 tôi đã làm được.
```

- Tên file: `chuong-07-y-tuong-va-research.md` (2 chữ số), phụ lục `phu-luc-a-tu-dien-thuat-ngu.md`.
- Tiêu đề H1 bắt buộc dạng `# Chương N — Tên ngắn` (dấu — để tách nhãn và tên).
- Mục H2 đánh số `N.1.`, `N.2.` để mục lục và "Trong chương này" tự sinh.
- Chương cuối phần thì checklist ghi "Trước khi sang Phần …"; chương cuối sách ghi "Trước khi sang Phụ lục".

## Hộp đặc biệt (blockquote)

| Viết | Hiện thành |
|---|---|
| `> Câu lệnh…` (không chữ đậm đầu) | Ô **PROMPT MẪU** có nút Sao chép |
| `> **Mong muốn:** … **Thực tế:** …` | Ô prompt (phiếu lỗi) |
| `> **Mẹo:** …` hoặc `**Gợi ý:**` | Hộp mẹo 💡 |
| `> **Quan trọng:** …`, `**Cảnh báo:**`, `**Không …**` | Hộp cảnh báo ⚠️ |
| `> **Nguyên tắc:** …`, `**Điểm cần nhớ:**` | Hộp nguyên tắc 🧭 |
| `> **Lưu ý:** …` hoặc chữ đậm khác ở đầu | Hộp ghi chú 📌 |
| `> Khi …`, `> Nếu …`, `> Bạn không …` | Hộp ghi chú (không phải prompt) |

Đừng viết nhãn kiểu `> **Prompt để AI làm X:**` bên trong blockquote: nó sẽ thành hộp ghi chú. Đặt nhãn ở đoạn văn phía trên, prompt ở blockquote bên dưới.

## Prompt

- Mỗi hành động học viên cần làm với AI phải có **một prompt sao chép được**.
- Chỗ học viên tự điền để trong `[ngoặc vuông]` (được tô vàng trên trang Bộ prompt).
- Prompt cho người mới luôn có câu chặn: "Đừng viết code vội", "Chưa sửa gì", "Dừng để tôi đọc", "Mở file cho tôi tự dán khoá, đừng hỏi khoá trong chat".
- Mọi prompt cũng khai báo trong `prompts.json` (nguồn duy nhất), gắn vào lá mindmap qua `p`.

## Theo chế độ trọng tâm (`book.mode`)

| Chế độ | Quy tắc |
|---|---|
| `nguoi-moi` | Không cửa sổ lệnh, không câu lệnh; mỗi thuật ngữ có ví dụ đời thường; từ tiếng Anh lần đầu xuất hiện kèm nghĩa tiếng Việt; bảng thay cho đoạn dài; ảnh chụp màn hình thật |
| `ky-thuat` | Được dùng lệnh, code ngắn trong khối code; giải thích lý do kỹ thuật, giới hạn, trường hợp biên |
| `trung-lap` | Viết như người mới, thêm hộp `> **Góc kỹ thuật:** …` cho ai muốn đi sâu |
| `ca-hai` | Các phần đầu theo `nguoi-moi`; phần nâng cao ghi rõ ở tiêu đề phần và đoạn mở chương |

## Giọng văn

- Xưng "bạn", câu ngắn, chủ động. Một ý một câu.
- Một khái niệm, **một phép so sánh đời thường** xuyên suốt (ví dụ: phần mềm như nhà hàng; API như người phục vụ).
- Không phóng đại, không hứa kết quả không kiểm chứng được. Số liệu, kết quả case phải có nguồn; không có thì ghi `❓` để hỏi giảng viên.
- Tên công cụ, giá, tính năng thay đổi nhanh: ghi theo tháng viết, khuyên học viên kiểm tra lại.
- Ghi công: nội dung của giảng viên khác ghi tên ở đoạn mở chương và `teacher` của phần.

## Case study

Khung cố định: **Bài toán** → **Cách làm (luồng, công cụ)** → **Prompt chính** → **Kết quả (ảnh chụp thật)** → **Bài học rút ra** → **Tự làm phiên bản của bạn**.

## Hình

- Sơ đồ: SVG tự sinh (`build_diagrams.py` trong dự án mẫu) hoặc ảnh từ giảng viên. Mỗi hình có chú thích `*Hình N.x — …*`.
- Ảnh chụp màn hình: che email, khoá, thông tin khách hàng trước khi đưa vào.
- Ảnh đặt trong `ebook-assets/<nhóm>/`, bộ máy tự nén sang webp cho web.
