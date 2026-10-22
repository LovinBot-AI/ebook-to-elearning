# ebook-to-elearning

Skill Claude Code giúp chuyên gia, giảng viên thiết kế khoá e-learning bài bản **trước khi quay video**: hỏi đáp gom tư liệu → thiết kế theo framework → dàn ý + phác thảo → ebook đầy đủ (chương, mindmap tương tác, bộ prompt, case, thuật ngữ, giáo án) → kịch bản quay một mạch 3–4 giờ → (hỏi trước) GitHub Pages có mật khẩu → bản free cho workshop.

- Hướng dẫn người dùng: [HUONG-DAN.md](HUONG-DAN.md)
- Luật cho Claude: [SKILL.md](SKILL.md)
- Quy trình: [docs/QUY-TRINH.md](docs/QUY-TRINH.md)

Cài: `zsh install.sh` · CLI: `python3 bin/e2e.py --help`

Cấu trúc:

```
SKILL.md  HUONG-DAN.md  install.sh  VERSION  CHANGELOG.md
bin/e2e.py                 CLI
docs/                      quy trình, câu hỏi, framework, phong cách viết, quay video, bản free
templates/                 BRIEF, TU-LIEU, THIET-KE, DAN-Y, PHAC-THAO, KICH-BAN-QUAY + project/ (book.json, mindmap.json, prompts.json, chương mẫu)
engine/                    bộ máy dựng ebook (web, PDF, EPUB, site mật khẩu/công khai, mindmap, trang prompt, bìa)
examples/vibe-code-phan-mem/   dữ liệu thật của ebook Vibe Code phần mềm
```
