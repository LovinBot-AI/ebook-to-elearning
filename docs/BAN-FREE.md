# Bản FREE cho workshop (NỘI BỘ, G7)

> **Quan trọng:** tài liệu này là chiến lược nội bộ. Không đưa các chữ "lead", "phễu", "lead magnet" vào nội dung học viên đọc.

## Mục đích

Workshop miễn phí cần một món quà **thật sự hữu ích** để người tham dự để lại thông tin và tin tưởng giảng viên. Bản free lấy từ bản full, nên không tốn công soạn lại. Cuối mỗi chương có lời mời học tiếp bản đầy đủ (landing page khoá e-learning).

## Bản free nên có

| Nên đưa | Vì sao |
|---|---|
| Mindmap toàn khoá (đủ nhánh) | Thấy được bức tranh lớn và độ sâu của khoá trả phí |
| 1–3 chương nền tảng (khái niệm, bản đồ quy trình) | Đủ để hiểu và làm được một việc nhỏ |
| 1–2 case study có ảnh thật | Bằng chứng kết quả |
| Một nhóm prompt khởi động | Dùng được ngay trong buổi workshop |
| Từ điển thuật ngữ | Hữu ích, ít rủi ro |

| Giữ cho bản trả phí | Vì sao |
|---|---|
| Quy trình đầy đủ từng bước, bài tập, giáo án | Giá trị cốt lõi |
| Toàn bộ thư viện prompt | Giá trị dùng lâu dài |
| Phần nâng cao, repo mẫu, tài nguyên tải về | Lý do để nâng cấp |

Nguyên tắc: bản free **giải quyết trọn một vấn đề nhỏ** (học viên làm được một việc), và cho thấy rõ **những vấn đề lớn hơn** bản đầy đủ sẽ giải quyết. Không cắt cụt giữa chừng một hướng dẫn.

## free.json

```json
{
  "title_suffix": " · Bản giới thiệu",
  "chapters": [1, 2, 6],
  "appendices": ["a"],
  "mindmap_branches": "all",
  "mindmap_locked_note": "Có trong bản đầy đủ",
  "prompt_steps": ["bat-dau", "y-tuong"],
  "cta": {"label": "Học bản đầy đủ →", "url": "https://…landing-page…", "text": "Bạn vừa xem 3/22 chương. Bản đầy đủ có quy trình từng bước, 70+ prompt, bài tập và video hướng dẫn."},
  "downloads": []
}
```

- `chapters`: số chương giữ lại (được đánh số lại liên tục trong bản free).
- `mindmap_branches`: `"all"` hoặc danh sách nhãn nhánh. Lá thuộc chương không có trong bản free vẫn hiện (để thấy độ sâu) nhưng không có prompt, kèm ghi chú `mindmap_locked_note`.
- `prompt_steps`: các bước prompt giữ lại.
- `cta`: nút trên trang bìa + hộp mời cuối mỗi chương.

Lệnh: `e2e free <dự án full> --config free.json --out <thư mục bản free>`. Bản free là một dự án riêng, `public: true` (không mật khẩu), build và xem trước, **hỏi trước khi đẩy lên mạng**.

## Dẫn dắt trong workshop

1. Mở mindmap bản free, đi một vòng toàn cảnh (5 phút).
2. Làm cùng học viên một việc nhỏ theo chương free (30–45 phút).
3. Chiếu 1 case thật.
4. Chỉ phần mindmap "có trong bản đầy đủ", giới thiệu khoá, link landing page.
