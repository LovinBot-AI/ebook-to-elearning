# Quy trình ebook-to-elearning

```
Hỏi đáp tư liệu ─► Thiết kế ─► Dàn ý + phác thảo ─► Chương mẫu ─► Ebook đầy đủ ─► Kịch bản quay ─► QUAY ─► (video-to-elearning)
     G0               G1              G2                G3             G4               G5
                                                                         │
                                                                         ├─► Đẩy GitHub Pages (G6, hỏi trước)
                                                                         └─► Bản free cho workshop (G7, nội bộ)
```

## Vì sao làm theo thứ tự này

| Bước | Vì sao không bỏ qua |
|---|---|
| Hỏi đáp tư liệu trước | Giảng viên đã có rất nhiều thứ (bài giảng cũ, mindmap, tài liệu). Viết từ đầu mà không đọc là phí và lệch giọng giảng viên. |
| Thiết kế (đối tượng, trọng tâm) | Cùng một chủ đề, bản cho người mới và bản kỹ thuật khác nhau hoàn toàn. Chọn sai là viết lại toàn bộ. |
| Dàn ý + phác thảo trước nội dung | Sửa dàn ý mất 5 phút, sửa 20 chương mất 2 ngày. Đây là luật quan trọng nhất. |
| Một chương mẫu | Chốt giọng văn, độ sâu, cách trình bày trước khi nhân lên cả sách. |
| Ebook đầy đủ trước khi quay | Giảng viên quay một mạch 3–4 giờ, không vấp, không quên, có sẵn prompt và case để chiếu. |
| Kịch bản quay | Mỗi đoạn quay = một chương, có câu chuyển đoạn, nên bước cắt bài sau đó gần như tự động. |
| Bản full trước, bản free sau | Bản free chỉ là lựa chọn từ bản full, không phải soạn lại. |

## Sản phẩm của từng bước

| Cổng | File | Người duyệt nhìn vào đâu |
|---|---|---|
| G0 | `00-ke-hoach/BRIEF.md`, `TU-LIEU.md` | Mục tiêu một câu, học viên, tư liệu đã đọc |
| G1 | `00-ke-hoach/THIET-KE.md`, `book.json → mode` | Chế độ trọng tâm, bảng mục tiêu, bảng Action Mapping |
| G2 | `00-ke-hoach/DAN-Y.md`, `PHAC-THAO.md`, `mindmap.json` (nháp) | Bảng dàn ý, tổng phút video, mindmap bấm thử |
| G3 | 1 chương `.md` + bản web | Trang web chương mẫu trên máy tính và điện thoại |
| G4 | Toàn bộ chương, phụ lục, `prompts.json`, `mindmap.json` | Link xem thử ebook, mindmap, Bộ prompt |
| G5 | `00-ke-hoach/KICH-BAN-QUAY.md` | Bảng đoạn quay, câu mở đoạn, thứ không được chiếu |
| G6 | Repo GitHub, GitHub Pages, mật khẩu | Link thật, thử mật khẩu |
| G7 | `free.json` → dự án bản free | Link xem thử bản free, nút mời học bản đầy đủ |

## Kết nối với video-to-elearning (làm sau)

Sau khi quay, skill `video-to-elearning` cắt video thành bài. Dự kiến ráp nối:
- Tên bài trong PLAN lấy từ tên chương / đoạn trong `KICH-BAN-QUAY.md`.
- Câu chuyển đoạn trong transcript dùng làm mốc cắt.
- Link video từng bài gắn ngược vào chương ebook (mục "Xem video bài này").
