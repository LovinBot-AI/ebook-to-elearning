# Kết nối tài khoản Mux

Mux là nơi lưu và phát video bài học. Có **hai kết nối**, mỗi cái một việc:

| Kết nối | Để làm gì | Bắt buộc? |
|---|---|---|
| **1. Token upload** (lưu trên máy) | Skill đẩy hàng loạt video bài học lên Mux, lấy link, mã nhúng | Có, trước khi đăng video |
| **2. Mux MCP** (connector trong Claude) | Hỏi Claude về video đã có: danh sách, trạng thái, lượt xem, sửa tiêu đề | Không, tiện thêm |

Upload file lớn đi qua token (1), vì MCP không phù hợp để gửi video vài trăm MB.

## Trước hết: tài khoản Mux

1. Đăng ký tại **dashboard.mux.com** (có gói miễn phí, tối đa 10 video; khoá học thật cần nâng gói ở Dashboard → Billing, bạn tự làm, Claude không làm phần thanh toán).
2. Chọn môi trường (environment), thường là **Production**.

## 1. Token upload (bắt buộc)

**Bạn làm (2 phút):**

1. dashboard.mux.com → **Settings → Access Tokens → Generate new token**.
2. Environment: Production. Quyền: **Mux Video: Read + Write** (không cần Data, System).
3. Bấm Generate. Màn hình hiện **Token ID** và **Secret Key**. Secret chỉ hiện **một lần**: giữ trang này mở.

**Nói với Claude:** *"Kết nối Mux giúp tôi."* Claude chạy `mux-pub connect`, máy bạn hiện **hai hộp thoại**: dán Token ID, rồi dán Secret Key. Token được lưu vào máy bạn tại `~/.config/video-to-elearning/mux.json` (chỉ tài khoản của bạn đọc được), Claude kiểm tra kết nối và báo "Kết nối OK".

> **Quan trọng:** không dán token vào khung chat, email, Zalo hay GitHub. Lộ token là người khác có thể xoá hoặc đăng video lên tài khoản của bạn. Nếu lỡ lộ: Dashboard → Access Tokens → Revoke, tạo token mới, chạy lại "Kết nối Mux".

## 2. Mux MCP (tuỳ chọn)

Mux có MCP chính thức tại `https://mcp.mux.com`, đăng nhập bằng tài khoản Mux (OAuth), không cần copy token.

**Trên Claude Desktop / claude.ai:**

1. Settings → **Connectors** → **Add custom connector**.
2. Name: `Mux` · URL: `https://mcp.mux.com` → Add.
3. Bấm **Connect**, đăng nhập dashboard.mux.com, chọn environment (Production) → Allow.

**Trên Claude Code (cửa sổ lệnh), nếu bạn dùng:**

```bash
claude mcp add --transport http mux https://mcp.mux.com
```

Sau đó gõ `/mcp` trong Claude Code, chọn `mux` → Authenticate để đăng nhập.

**Thử:** hỏi Claude *"Liệt kê 5 video mới nhất trên Mux của tôi."*

> **Lưu ý:** MCP làm được mọi việc mà quyền đăng nhập cho phép, kể cả xoá video. Skill luôn hỏi bạn trước mọi thao tác thay đổi dữ liệu trên Mux; nếu chỉ muốn xem, khi đăng nhập hãy chọn môi trường phụ hoặc dùng token chỉ có quyền Read.

## Chọn chế độ phát (hỏi mỗi lần đăng)

| Chế độ | Ai xem được | Dùng khi |
|---|---|---|
| `public` | Ai có link | Video giới thiệu, bài free, nhúng thẳng vào ebook |
| `signed` | Chỉ trang web có khoá ký (LMS) | Khoá học trả phí. Ebook chỉ hiện link sang bài trên LMS |

Skill không tự chọn: bạn quyết định ở bước xác nhận trước khi đăng.

Nguồn: [Mux MCP Server](https://www.mux.com/docs/integrations/mcp-server) · [Cài Mux MCP trên máy](https://www.mux.com/docs/integrations/installing-mcp-server-locally)
