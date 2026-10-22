#!/bin/zsh
# Cài ebook-to-elearning + hai skill đi kèm (video-to-elearning, mux-publisher) làm Claude Code skill.
# Không tự cài gói/phần mềm: chỉ liên kết skill và kiểm tra môi trường.
DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS="$HOME/.claude/skills"
mkdir -p "$SKILLS"
link() { # link <tên> <thư mục>
  if [[ -e "$SKILLS/$1" && ! -L "$SKILLS/$1" ]]; then echo "✗ $SKILLS/$1 đã tồn tại (không phải symlink) — bỏ qua"; return; fi
  ln -sfn "$2" "$SKILLS/$1" && echo "✔ $1 → $2"
}
link ebook-to-elearning "$DIR"

# video-to-elearning: dùng bản đã cài, hoặc thư mục cạnh repo này, hoặc biến V2E_DIR
V2E=""
if [[ -L "$SKILLS/video-to-elearning" || -d "$SKILLS/video-to-elearning" ]]; then
  V2E="$(cd "$SKILLS/video-to-elearning" 2>/dev/null && pwd -P)"
fi
for c in "$V2E_DIR" "$DIR/../video-to-elearning" "$HOME/video-to-elearning"; do
  [[ -z "$V2E" && -n "$c" && -f "$c/bin/v2e.mjs" ]] && V2E="$(cd "$c" && pwd)"
done
if [[ -n "$V2E" && -f "$V2E/bin/v2e.mjs" ]]; then
  link video-to-elearning "$V2E"
  link mux-publisher "$V2E/skills/mux-publisher"
else
  echo "⚠ Chưa có video-to-elearning (cần cho bước cắt video + đăng Mux). Tải về cạnh thư mục này rồi chạy lại:"
  echo "    git clone https://github.com/sonlovinbot/video-to-elearning.git \"$DIR/../video-to-elearning\""
fi

python3 "$DIR/bin/e2e.py" doctor
[[ -n "$V2E" ]] && echo "\nBước cắt video: Claude sẽ chạy 'v2e doctor' và HỎI bạn trước khi cài ffmpeg/Whisper/Remotion."
