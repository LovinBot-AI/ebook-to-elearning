#!/bin/zsh
# Cài ebook-to-elearning làm Claude Code skill + kiểm tra môi trường (không tự cài gói).
DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS="$HOME/.claude/skills"
mkdir -p "$SKILLS"
if [[ -e "$SKILLS/ebook-to-elearning" && ! -L "$SKILLS/ebook-to-elearning" ]]; then
  echo "✗ $SKILLS/ebook-to-elearning đã tồn tại (không phải symlink). Đổi tên/xoá thư mục đó rồi chạy lại."
  exit 1
fi
ln -sfn "$DIR" "$SKILLS/ebook-to-elearning"
echo "✔ Skill đã liên kết: $SKILLS/ebook-to-elearning → $DIR"
python3 "$DIR/bin/e2e.py" doctor
