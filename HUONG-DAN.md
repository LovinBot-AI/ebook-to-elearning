# Hướng dẫn dùng skill ebook-to-elearning

Skill giúp chuyên gia, giảng viên chuẩn bị **toàn bộ nội dung khoá e-learning trước khi quay**: dàn ý, ebook, mindmap chi tiết, bộ prompt, case study, thuật ngữ, giáo án và kịch bản quay một mạch 3–4 giờ. Sau đó (khi bạn đồng ý) đưa ebook lên mạng có mật khẩu, và tách bản free cho workshop.

## Cài đặt

```bash
zsh "/Users/danghuuson/VIDEO AI/CLAUDE REMOTION/ebook-to-elearning/install.sh"
```

Lệnh này liên kết skill vào Claude Code và kiểm tra môi trường (không tự cài gì khi bạn chưa đồng ý).

## Cách bắt đầu

Mở Claude Code, nói một trong các câu:

- "Tôi muốn soạn ebook và dàn ý cho khoá e-learning về [chủ đề], chuẩn bị trước khi quay."
- "Đây là tài liệu bài giảng cũ của tôi [link/file], giúp tôi lên dàn ý khoá học."
- "Từ ebook này tạo bản free cho workshop, CTA về [link landing page]."

## Bạn sẽ được hỏi và duyệt 8 lần

| Bước | Claude làm | Bạn làm |
|---|---|---|
| G0 · Hỏi đáp | Hỏi ý tưởng, học viên, đọc hết tư liệu bạn gửi | Trả lời, gửi bài giảng cũ, mindmap, tài liệu, link |
| G1 · Thiết kế | Đề xuất đối tượng, trọng tâm, mục tiêu theo framework | Chọn: thuần kỹ thuật / người mới / trung lập / cả hai |
| G2 · Dàn ý | Dàn ý + phác thảo từng chương + mindmap nháp bấm thử được | Sửa, thêm, bớt. **Chưa viết nội dung trước khi bạn duyệt bước này.** |
| G3 · Chương mẫu | Viết 1 chương hoàn chỉnh, mở trên web | Duyệt giọng văn, độ sâu |
| G4 · Ebook đầy đủ | Viết hết các chương, prompt, case, thuật ngữ, giáo án | Đọc trên web, góp ý |
| G5 · Kịch bản quay | Bảng đoạn quay, câu mở đoạn, checklist ngày quay | Duyệt, rồi đi quay |
| G6 · Đẩy lên mạng | Hỏi tên repo, riêng tư/công khai, mật khẩu | Đồng ý thì mới đẩy |
| G7 · Bản free | Đề xuất chương, case, prompt cho bản free + nút mời học | Duyệt, đồng ý thì mới đẩy |

Bạn có thể xem tiến độ bất kỳ lúc nào: "dự án đang ở bước nào?"

## Sản phẩm bạn nhận được

- **Ebook web** đọc trên máy tính và điện thoại: mục lục, tìm nhanh, chế độ sáng/tối, đọc tiếp chỗ cũ.
- **Mindmap tương tác:** bấm từng ý để xem giải thích, prompt sao chép, mở chương ở tab mới.
- **Trang Bộ prompt:** lọc theo nhóm, tìm kiếm, nút Sao chép.
- **PDF và EPUB** (khi bạn cần).
- **Bản có mật khẩu** trên GitHub Pages (nội dung được mã hoá thật, sai mật khẩu không đọc được).
- **Bản free công khai** cho workshop, cuối mỗi chương có nút mời học bản đầy đủ.
- **Tài liệu kế hoạch** trong `00-ke-hoach/`: brief, thiết kế, dàn ý, phác thảo, kịch bản quay.

## Tài liệu tham khảo trong skill

- `docs/HOI-DAP.md`: bộ câu hỏi đáp.
- `docs/FRAMEWORKS.md`: các framework thiết kế bài giảng và lúc nào dùng.
- `docs/PHONG-CACH-VIET.md`: khung chương, cách viết prompt, hộp mẹo/cảnh báo.
- `docs/QUAY-VIDEO.md`: chuẩn bị quay một mạch 3–4 giờ.
- `docs/BAN-FREE.md`: bản free cho workshop (nội bộ).
- `examples/vibe-code-phan-mem/`: dữ liệu thật của ebook Vibe Code phần mềm (book.json, mindmap.json, prompts.json).

## Lệnh (Claude tự chạy, bạn không cần gõ)

| Lệnh | Việc |
|---|---|
| `e2e doctor` | Kiểm tra môi trường |
| `e2e new <thư mục> --title "…"` | Tạo dự án mới |
| `e2e status <thư mục>` | Đang ở cổng nào |
| `e2e check <thư mục>` | Kiểm tra lỗi: ảnh thiếu, link sai, prompt sai id, lộ API key |
| `e2e build <thư mục> web pdf epub site` | Dựng ebook |
| `e2e cover <thư mục>` | Dựng ảnh bìa |
| `e2e free <thư mục> --config free.json --out <thư mục free>` | Dựng bản free |
