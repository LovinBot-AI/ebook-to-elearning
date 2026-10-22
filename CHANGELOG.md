# Changelog

## 0.5.0 · 2026-10-22
- Trang chọn mẫu `design/preview/index.html` (`e2e templates`): 4 phong cách S1 Coachio, S2 Studio Đêm, S3 Rừng Xanh, S4 Cobalt × 3 bố cục thumbnail A/B/C; xem trước thumbnail, bìa, trang đọc máy tính và điện thoại; thử logo/mascot; nút "Sao chép lựa chọn".
- `e2e brand-apply --template S3-B --name --teacher --kicker --logo --mascot`: áp mẫu cho ebook, chuyển sang thumbnail video qua handoff.
- Ebook, mindmap, Bộ prompt: chuyển trang trong cùng tab (chỉ link ngoài mở tab mới); mindmap nhớ nhánh đang mở và vị trí cuộn; "← Ebook" về đúng chương đang đọc; trang prompt nhớ vị trí cuộn.
- Giao diện đa thiết bị: không tràn ngang ở 320/360/390/768/1280px; nút mindmap gọn trên điện thoại; khung "Sau chương này" theo màu thương hiệu.

## 0.4.0 · 2026-10-22
- Tải chậm: chưa tới bước video thì không tải skill cắt video, FFmpeg, Remotion, Whisper (trừ khi người dùng yêu cầu). `e2e start` chỉ ghi "⏸ chưa cần" kèm dung lượng; install.sh không hỏi tải nữa.
- Thương hiệu: hỏi ở G0 "đội Coachio hay thương hiệu riêng". Coachio giữ nguyên. Thương hiệu mới: hỏi logo, màu, cảm giác → 2–3 phương án → `e2e brand-preview` (thumbnail, bìa, trang ebook) → duyệt → `e2e brand-apply`. `e2e brand-colors` rút màu từ logo. docs/THUONG-HIEU.md.
- Engine: màu ebook (web, PDF, EPUB, mindmap, trang prompt) và bìa theo `book.json › brand`, logo trên bìa.
- `e2e handoff` mang thương hiệu sang video-to-elearning.

## 0.3.0 · 2026-10-22
- Khởi động: `e2e start [dir]` — liệt kê thiếu skill/phần mềm/kết nối nào, chia "cần ngay" và "cần ở bước sau", mỗi mục ghi 👉 người dùng làm gì và 🤖 Claude làm gì.
- `e2e setup --yes`: tải `sonlovinbot/video-to-elearning` và gắn video-to-elearning + mux-publisher (chỉ sau khi người dùng đồng ý). install.sh hỏi luôn khi chạy.
- `e2e next <dir>`: việc tiếp theo bằng lời thường cho mọi bước, từ hỏi đáp tới đăng Mux và gắn video.
- SKILL.md: mục START HERE; mọi câu trả lời kết thúc bằng "👉 Việc tiếp theo của bạn: …".

## 0.2.0 · 2026-10-22
- Trọn gói sau khi quay: cổng G8 (video → bài học qua video-to-elearning) và G9 (đăng Mux qua mux-publisher, gắn video ngược vào ebook).
- `e2e handoff`: xuất `handoff-v2e.json` (bài dự kiến mã `<chương>.<n>`, câu mở đoạn, phút, thuật ngữ, thứ phải cắt, nội dung bài) + thư mục `quay-video/` có hướng dẫn dán video Zoom (mp4 + .vtt).
- `e2e attach-video`: gắn video đã đăng vào đầu từng chương (Mux public → nhúng player; signed → chỉ link LMS).
- Engine: khung "Video bài học" từ `videos.json`.
- docs/KET-NOI-MUX.md: token upload (hộp thoại `mux-pub connect`) + Mux MCP (`https://mcp.mux.com`, OAuth) cho Claude Desktop và Claude Code.
- install.sh liên kết luôn video-to-elearning và mux-publisher; HUONG-DAN viết lại theo "bạn chỉ cần làm 5 việc".

## 0.1.0 · 2026-10-22
- Quy trình 8 cổng duyệt G0–G7: hỏi đáp tư liệu → thiết kế (đối tượng, trọng tâm) → dàn ý + phác thảo → chương mẫu → ebook đầy đủ → kịch bản quay → đẩy GitHub (hỏi trước) → bản free (nội bộ).
- Tài liệu: bộ câu hỏi đáp, framework thiết kế bài giảng (Backward Design, Bloom, Action Mapping, Merrill, Gagné, Mayer, 4C/ID, Kolb, Kirkpatrick, ADDIE/SAM), phong cách viết, chuẩn bị quay một mạch, bản free.
- Bộ máy build tổng quát từ ebook Vibe Code phần mềm: book.json / mindmap.json / prompts.json; web, PDF, EPUB, site có mật khẩu (AES-GCM) hoặc công khai; bìa tự sinh; nút CTA cho bản free.
- CLI e2e: doctor, new, status, approve, check, build, cover, free, sync-engine.
- Ví dụ thật: examples/vibe-code-phan-mem (dựng lại đúng 157 prompt, 157 ý mindmap, 73 prompt trang Bộ prompt).
