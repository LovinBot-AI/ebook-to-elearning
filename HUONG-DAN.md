# Hướng dẫn dùng skill ebook-to-elearning

Skill giúp chuyên gia, giảng viên chuẩn bị **toàn bộ nội dung khoá e-learning trước khi quay**: dàn ý, ebook, mindmap chi tiết, bộ prompt, case study, thuật ngữ, giáo án và kịch bản quay một mạch 3–4 giờ. Sau đó (khi bạn đồng ý) đưa ebook lên mạng có mật khẩu, và tách bản free cho workshop.

## Bạn chỉ cần làm 5 việc

| # | Việc của bạn | Claude lo phần còn lại |
|---|---|---|
| 1 | Trả lời câu hỏi, gửi tư liệu đã có (bài giảng cũ, mindmap, tài liệu, link) | Đọc hết, lập brief, thiết kế bài giảng theo framework |
| 2 | Duyệt và chỉnh: dàn ý, chương mẫu, ebook, kịch bản quay | Viết ebook, mindmap, bộ prompt, case, thuật ngữ, giáo án |
| 3 | **Quay video** một mạch 3–4 giờ theo kịch bản | — |
| 4 | **Dán video** vào thư mục `quay-video/` của dự án (Zoom: file MP4 + file transcript .vtt là tốt nhất) | Chép lời, chia bài theo chương, cắt đoạn thừa, khử ồn |
| 5 | Duyệt PLAN, thumbnail, 1 bài mẫu; đồng ý trước khi đăng Mux / GitHub | Render cả bộ, tạo nội dung từng bài, đăng Mux, gắn video vào ebook |

Bạn không cần gõ lệnh nào. Claude chạy mọi lệnh và luôn hỏi trước khi cài phần mềm, đăng video hay đẩy lên mạng.

## Cài đặt (một lần)

```bash
zsh "/đường/dẫn/tới/ebook-to-elearning/install.sh"
```

Lệnh này liên kết 3 skill vào Claude Code: **ebook-to-elearning** (soạn nội dung), **video-to-elearning** (cắt video thành bài) và **mux-publisher** (đăng Mux). Nếu máy chưa có video-to-elearning, lệnh sẽ in câu lệnh tải về. Không có gì được cài thêm khi bạn chưa đồng ý.

Kết nối tài khoản Mux (một lần, trước khi đăng video): xem **[docs/KET-NOI-MUX.md](docs/KET-NOI-MUX.md)**. Tóm tắt: tạo Access Token trong dashboard.mux.com, nói với Claude "Kết nối Mux", rồi dán token vào **hộp thoại hiện trên máy** (không dán vào chat). Muốn hỏi Claude về video trên Mux thì thêm connector `https://mcp.mux.com` trong Claude (Settings → Connectors).

## Lấy video từ Zoom

1. zoom.us → **Recordings → Cloud recordings** → chọn buổi quay.
2. Tải **Shared screen with speaker view** (file .mp4) và **Audio transcript** (file .vtt).
3. Chép cả hai vào thư mục `quay-video/` trong dự án (Claude tạo sẵn thư mục này kèm hướng dẫn). Không cần đổi tên.
4. Nói với Claude: **"Đã dán video vào quay-video, làm tiếp."**

Ghi trên máy (Zoom local, OBS, QuickTime) thì chỉ có file video: vẫn dùng được, Claude tự chép lời nhưng lâu hơn.

## Cách bắt đầu

Mở Claude Code, nói một trong các câu:

- "Tôi muốn soạn ebook và dàn ý cho khoá e-learning về [chủ đề], chuẩn bị trước khi quay."
- "Đây là tài liệu bài giảng cũ của tôi [link/file], giúp tôi lên dàn ý khoá học."
- "Đã quay xong, video ở [đường dẫn], làm bộ bài học và đăng Mux."
- "Từ ebook này tạo bản free cho workshop, CTA về [link landing page]."

## Các bước duyệt

| Bước | Claude làm | Bạn làm |
|---|---|---|
| G0 · Hỏi đáp | Hỏi ý tưởng, học viên, đọc hết tư liệu bạn gửi | Trả lời, gửi bài giảng cũ, mindmap, tài liệu, link |
| G1 · Thiết kế | Đề xuất đối tượng, trọng tâm, mục tiêu theo framework | Chọn: thuần kỹ thuật / người mới / trung lập / cả hai |
| G2 · Dàn ý | Dàn ý + phác thảo từng chương + mindmap nháp bấm thử được | Sửa, thêm, bớt. **Chưa viết nội dung trước khi bạn duyệt bước này.** |
| G3 · Chương mẫu | Viết 1 chương hoàn chỉnh, mở trên web | Duyệt giọng văn, độ sâu |
| G4 · Ebook đầy đủ | Viết hết các chương, prompt, case, thuật ngữ, giáo án | Đọc trên web, góp ý |
| G5 · Kịch bản quay | Bảng đoạn quay, câu mở đoạn, checklist ngày quay, thư mục `quay-video/` | Duyệt, rồi đi quay |
| G6 · Đẩy ebook lên mạng | Hỏi tên repo, riêng tư/công khai, mật khẩu | Đồng ý thì mới đẩy |
| G7 · Bản free | Đề xuất chương, case, prompt cho bản free + nút mời học | Duyệt, đồng ý thì mới đẩy |
| G8 · Video thành bài học | Chia bài theo chương, PLAN, thumbnail, 1 bài mẫu, rồi render cả bộ | Dán video; duyệt PLAN, thumbnail, bài mẫu |
| G9 · Đăng Mux + gắn vào ebook | Bảng xác nhận (chế độ phát, danh sách video), đăng thử 1 video, rồi cả bộ; gắn video vào chương | Chọn signed/public, đồng ý, xem thử video đầu |

Bài kiểm tra (quiz) cho từng bài sẽ được bổ sung ở bản sau.

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
- `docs/KET-NOI-MUX.md`: kết nối Mux (token upload + MCP).
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
| `e2e handoff <thư mục>` | Chuẩn bị bàn giao cho bước cắt video, tạo thư mục `quay-video/` |
| `e2e attach-video <thư mục> --from course.json` | Gắn video đã đăng vào từng chương |
| `v2e …`, `mux-pub …` | Lệnh của video-to-elearning và mux-publisher |
