# Chuẩn bị quay video một mạch 3–4 giờ (G5)

Video quay **sau cùng**, một mạch. Ebook, mindmap, prompt và kịch bản quay giúp giảng viên không phải nhớ, không phải dừng giữa chừng tìm tài liệu, và giúp bước cắt bài sau này (skill `video-to-elearning`) nhanh, sạch.

## Nguyên tắc

1. **Đoạn quay = chương ebook.** Mỗi đoạn có tiêu đề trùng tên chương, thời lượng mục tiêu, mở và đóng rõ ràng.
2. **Câu chuyển đoạn:** đầu mỗi đoạn nói một câu cố định, ví dụ *"Phần tiếp theo: Chương 7, ý tưởng và research."* Cuối đoạn: *"Tóm lại chương 7…"*. Transcript có câu này thì cắt bài gần như tự động.
3. **Không chiếu thông tin nhạy cảm:** màn hình đăng nhập, email, mật khẩu, API key, dữ liệu khách hàng. Đăng nhập sẵn trước khi bấm quay; nếu lỡ chiếu, nói "đoạn này cắt" để dễ tìm.
4. **Mỗi demo có đường lui:** chuẩn bị sẵn kết quả đã làm xong (ảnh, link) để nếu demo lỗi vẫn giảng tiếp được. Lỗi có giá trị dạy (cách sửa) thì giữ lại.
5. **Nghỉ có chủ đích:** mỗi 50–60 phút nghỉ 5 phút; nói "nghỉ 5 phút" để dễ cắt.

## Ngân sách thời gian

| Loại đoạn | Thời lượng gợi ý |
|---|---|
| Mở khoá: kết quả cuối, lộ trình (mở mindmap) | 5–8 phút |
| Chương khái niệm | 8–15 phút |
| Chương làm mẫu (demo) | 15–30 phút |
| Case study | 5–10 phút mỗi case |
| Tổng kết, bài tập, hướng đi tiếp | 5–10 phút |

Tổng 180–240 phút. Nếu dàn ý vượt, đưa phần ít quan trọng sang phụ lục đọc thêm hoặc video bonus.

## Nhịp một đoạn (Gagné rút gọn)

1. **Vấn đề** (30 giây): một tình huống thật.
2. **Mục tiêu:** đọc dòng "Sau chương này, bạn làm được".
3. **Nội dung:** mở chương ebook hoặc mindmap trên màn hình, giảng theo bảng/sơ đồ.
4. **Demo:** làm mẫu với prompt trong ebook (bấm Sao chép ngay trên trang Bộ prompt để học viên thấy nguồn).
5. **Giao bài:** chỉ vào bài tập/checklist cuối chương.
6. **Tóm tắt:** 2–3 câu.

## Màn hình khi quay

- Tab 1: ebook (đã mở khoá mật khẩu, chế độ sáng, chữ to A+).
- Tab 2: mindmap, tab 3: Bộ prompt.
- Công cụ demo đã đăng nhập, thư mục dự án mẫu đã tạo sẵn.
- Tắt thông báo, ẩn bookmark, đóng tab cá nhân.

## Checklist ngày quay

- [ ] Đã đọc lại `KICH-BAN-QUAY.md`, in hoặc mở trên màn hình phụ.
- [ ] Tài khoản công cụ đã đăng nhập; hạn mức (quota) còn đủ.
- [ ] Dự án demo ở trạng thái đầu; có bản đã làm xong để dự phòng.
- [ ] Mic, ánh sáng, độ phân giải màn hình (1920×1080, phóng chữ 125%).
- [ ] Ghi âm thử 1 phút, nghe lại.
- [ ] Nước, ghi chú thời gian bắt đầu từng đoạn (hoặc để transcript lo).

## Sau khi quay

1. Tải về và chép vào thư mục `quay-video/` của dự án (có hướng dẫn trong `HUONG-DAN-DAN-VIDEO.md`):
   - **Zoom Cloud:** zoom.us → Recordings → Cloud recordings → chọn buổi → tải **Shared screen with speaker view (MP4)** và **Audio transcript (VTT)**. Có VTT là tốt nhất: chép lời nhanh và chính xác.
   - **Zoom ghi trên máy / OBS / QuickTime:** chỉ có file video, skill tự chép lời (lâu hơn).
2. Nói với Claude: "Đã dán video, làm tiếp". Claude dò câu mở đoạn để chia bài theo chương, gửi bạn PLAN, thumbnail, một bài mẫu để duyệt, rồi render cả bộ.
3. Khi đã kết nối Mux (docs/KET-NOI-MUX.md), Claude hỏi xác nhận rồi mới đăng, sau đó gắn video vào từng chương ebook.
