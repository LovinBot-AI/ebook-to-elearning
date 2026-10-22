"""Khởi động (e2e start), cài skill đi kèm (e2e setup) và "việc tiếp theo" (e2e next).

Nguyên tắc: người dùng không phải đọc lệnh. Mỗi dòng in ra có 2 phần:
  👉 Bạn: việc người dùng cần làm (bằng lời thường)
  🤖 Claude: việc Claude sẽ làm (sau khi hỏi nếu cần)
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SKILLS = Path.home() / '.claude' / 'skills'
MUX_TOKEN = Path.home() / '.config' / 'video-to-elearning' / 'mux.json'
V2E_REPO = 'sonlovinbot/video-to-elearning'
COMPANIONS = [
    # tên skill, vì sao cần, file phải có trong skill
    ('video-to-elearning', 'cắt video buổi quay thành bộ bài học, thumbnail, render', 'bin/v2e.mjs'),
    ('mux-publisher', 'đăng video bài học lên Mux, lấy link và mã nhúng', 'scripts/mux-pub.mjs'),
]
PY_MODS = {'markdown_it': 'markdown-it-py', 'bs4': 'beautifulsoup4', 'PIL': 'pillow', 'playwright': 'playwright',
           'fitz': 'pymupdf', 'pypdf': 'pypdf', 'cryptography': 'cryptography'}


def _skill_ok(name: str, must: str) -> Path | None:
    p = SKILLS / name
    return p.resolve() if (p / must).exists() else None


def _v2e_dir() -> Path | None:
    p = _skill_ok('video-to-elearning', 'bin/v2e.mjs')
    if p:
        return p
    for c in [SKILL.parent / 'video-to-elearning', Path.home() / 'video-to-elearning']:
        if (c / 'bin' / 'v2e.mjs').exists():
            return c.resolve()
    return None


def checks() -> list[dict]:
    """Danh sách kiểm tra khởi động. level: need (bắt buộc ngay) | later (cần ở bước sau) | nice (tuỳ chọn)."""
    out = []
    linked = (SKILLS / 'ebook-to-elearning').resolve() == SKILL if (SKILLS / 'ebook-to-elearning').exists() else False
    out.append({'ok': linked, 'level': 'need', 'what': 'Skill ebook-to-elearning đã gắn vào Claude Code',
                'you': 'Không cần làm gì.', 'claude': 'Chạy install.sh của skill để gắn.'})
    missing = [pkg for m, pkg in PY_MODS.items() if not importlib.util.find_spec(m)]
    out.append({'ok': not missing, 'level': 'need', 'what': 'Thư viện Python để dựng ebook' + (f' (thiếu: {", ".join(missing)})' if missing else ''),
                'you': 'Trả lời "đồng ý" khi Claude hỏi cài.', 'claude': f'Hỏi bạn rồi cài: pip install -r engine/requirements.txt'})
    chrome = Path('/Applications/Google Chrome.app').exists() or bool(shutil.which('google-chrome'))
    out.append({'ok': chrome, 'level': 'later', 'what': 'Google Chrome (để xuất PDF và ảnh bìa)',
                'you': 'Cài Google Chrome từ google.com/chrome nếu muốn có bản PDF.', 'claude': 'Bỏ qua PDF cho tới khi có Chrome.'})
    v2e = _v2e_dir()
    for name, why, must in COMPANIONS:
        ok = bool(_skill_ok(name, must))
        out.append({'ok': ok, 'level': 'later', 'what': f'Skill {name}: {why}',
                    'you': 'Trả lời "đồng ý" khi Claude hỏi tải về (cần quyền vào repo trên GitHub).',
                    'claude': ('Gắn bản đã có trên máy: ' + str(v2e)) if (v2e and not ok) else f'Hỏi bạn rồi tải {V2E_REPO} và gắn vào Claude Code (e2e setup).'})
    node = shutil.which('node')
    out.append({'ok': bool(node), 'level': 'later', 'what': 'Node.js (để cắt video và đăng Mux)',
                'you': 'Cài Node.js bản LTS từ nodejs.org (bấm tải, bấm Next tới hết).', 'claude': 'Kiểm tra lại sau khi bạn cài.'})
    v2e_ready = False
    if v2e and (v2e / 'state' / 'setup.json').exists():
        try:
            v2e_ready = json.loads((v2e / 'state' / 'setup.json').read_text())['ready']
        except Exception:  # noqa: BLE001
            pass
    out.append({'ok': v2e_ready, 'level': 'later', 'what': 'Công cụ xử lý video (ffmpeg, Whisper, Remotion)',
                'you': 'Trả lời "đồng ý" khi Claude hỏi cài (chỉ cần trước khi cắt video).', 'claude': 'Chạy v2e doctor, liệt kê thứ cần cài, hỏi bạn rồi mới cài.'})
    out.append({'ok': MUX_TOKEN.exists(), 'level': 'later', 'what': 'Tài khoản Mux đã kết nối (để đăng video)',
                'you': 'Tạo Access Token trong dashboard.mux.com (Settings → Access Tokens, quyền Mux Video Read + Write), rồi nói "Kết nối Mux". Xem docs/KET-NOI-MUX.md.',
                'claude': 'Mở hộp thoại để bạn dán token (không qua chat), kiểm tra kết nối.'})
    gh = bool(shutil.which('gh'))
    out.append({'ok': gh, 'level': 'nice', 'what': 'GitHub CLI (để đưa ebook lên GitHub Pages)',
                'you': 'Chỉ cần khi muốn đưa ebook lên mạng.', 'claude': 'Hướng dẫn cài khi tới bước đó.'})
    return out


def cmd_start(a):
    print('━━ KHỞI ĐỘNG ebook-to-elearning ━━\n')
    cs = checks()
    groups = [('need', 'Cần ngay'), ('later', 'Cần ở bước sau (cắt video, đăng Mux)'), ('nice', 'Tuỳ chọn')]
    for lv, title in groups:
        items = [c for c in cs if c['level'] == lv]
        print(f'{title}:')
        for c in items:
            print(f'  {"✅" if c["ok"] else "❌"} {c["what"]}')
            if not c['ok']:
                print(f'       👉 Bạn: {c["you"]}\n       🤖 Claude: {c["claude"]}')
        print()
    blockers = [c for c in cs if not c['ok'] and c['level'] == 'need']
    later = [c for c in cs if not c['ok'] and c['level'] == 'later']
    if blockers:
        print('▶ Cần xử lý mục "Cần ngay" trước khi bắt đầu.')
    elif later:
        print(f'▶ Bắt đầu soạn khoá học được rồi. {len(later)} mục cho bước video sẽ chuẩn bị sau (có thể làm ngay: "cài đủ các skill đi kèm").')
    else:
        print('▶ Đã sẵn sàng toàn bộ quy trình, từ soạn nội dung tới đăng Mux.')
    if getattr(a, 'dir', None):
        print()
        cmd_next(a)


def cmd_setup(a):
    """Tải + gắn skill đi kèm. Chỉ chạy sau khi người dùng đồng ý (--yes)."""
    v2e = _v2e_dir()
    if not v2e:
        dst = SKILL.parent / 'video-to-elearning'
        if not a.yes:
            print(f'Sẽ tải {V2E_REPO} về {dst} (~vài chục MB) và gắn video-to-elearning + mux-publisher vào Claude Code.\nHỏi người dùng; đồng ý thì chạy lại với --yes.')
            return
        if shutil.which('gh'):
            r = subprocess.call(['gh', 'repo', 'clone', V2E_REPO, str(dst)])
        else:
            r = subprocess.call(['git', 'clone', f'https://github.com/{V2E_REPO}.git', str(dst)])
        if r != 0:
            raise SystemExit(f'✗ Không tải được {V2E_REPO}. Repo private: nhờ chủ repo mời tài khoản GitHub của bạn, đăng nhập gh (gh auth login) rồi thử lại.')
        v2e = dst.resolve()
    SKILLS.mkdir(parents=True, exist_ok=True)
    for name, target in [('video-to-elearning', v2e), ('mux-publisher', v2e / 'skills' / 'mux-publisher')]:
        link = SKILLS / name
        if link.exists() and not link.is_symlink():
            print(f'⚠ {link} là thư mục thật, không phải liên kết → giữ nguyên')
            continue
        if link.is_symlink():
            link.unlink()
        link.symlink_to(target)
        print(f'✔ {name} → {target}')
    print('▶ Tiếp: khi tới bước cắt video, Claude chạy "v2e doctor" và hỏi bạn trước khi cài ffmpeg/Whisper/Remotion.')


# ---------------------------------------------------------------- việc tiếp theo
def _gates(d: Path) -> dict:
    f = d / '00-ke-hoach' / 'state.json'
    return json.loads(f.read_text(encoding='utf-8')).get('gates', {}) if f.exists() else {}


def _filled(f: Path) -> bool:
    return f.exists() and '{{' not in f.read_text(encoding='utf-8') and f.read_text(encoding='utf-8').count('…') < 6


def next_step(d: Path) -> tuple[str, str, str]:
    """(bước, 👉 bạn, 🤖 claude)."""
    g = _gates(d)
    k = d / '00-ke-hoach'
    chs = sorted(d.glob('chuong-[0-9][0-9]-*.md'))
    if 'G0' not in g:
        if not _filled(k / 'BRIEF.md'):
            return ('G0 · Hỏi đáp', 'Trả lời các câu hỏi về khoá học và gửi mọi tư liệu đã có (bài giảng cũ, mindmap, tài liệu, link).',
                    'Đọc hết tư liệu, viết BRIEF.md và TU-LIEU.md.')
        return ('G0 · Duyệt brief', 'Đọc tóm tắt brief Claude gửi, sửa chỗ sai, trả lời "duyệt".', 'Ghi nhận duyệt, chuyển sang câu hỏi về đối tượng và trọng tâm.')
    if 'G1' not in g:
        return ('G1 · Thiết kế', 'Chọn trọng tâm: thuần kỹ thuật / người mới / trung lập / cả hai; xem bảng mục tiêu rồi trả lời "duyệt".',
                'Viết THIET-KE.md theo framework (mục tiêu, Action Mapping).')
    if 'G2' not in g:
        return ('G2 · Dàn ý', 'Xem dàn ý, phác thảo và mindmap nháp; ghi chỗ muốn thêm/bớt, rồi "duyệt".', 'Viết DAN-Y.md, PHAC-THAO.md, mindmap nháp. Chưa viết chương.')
    if 'G3' not in g:
        return ('G3 · Chương mẫu', 'Đọc chương mẫu trên web, nhận xét giọng văn và độ sâu, rồi "duyệt".', 'Viết 1 chương hoàn chỉnh, build, gửi link xem thử.')
    if 'G4' not in g:
        return ('G4 · Ebook đầy đủ', 'Đọc ebook, mindmap, Bộ prompt trên web; góp ý; "duyệt" khi ổn.', f'Viết các chương còn lại (đang có {len(chs)}), prompt, case, thuật ngữ, giáo án.')
    if 'G5' not in g:
        return ('G5 · Kịch bản quay', 'Đọc kịch bản quay, chỉnh thời lượng và câu mở đoạn, rồi "duyệt".', 'Viết KICH-BAN-QUAY.md, tạo thư mục quay-video/.')
    vdir = d / 'quay-video'
    has_video = vdir.exists() and any(p.suffix.lower() in ('.mp4', '.mov', '.m4v') for p in vdir.iterdir())
    if not has_video:
        return ('Quay video', 'Quay video theo kịch bản. Xong thì chép file .mp4 (và file transcript .vtt của Zoom) vào thư mục quay-video/, rồi nói "đã dán video".',
                'Chuẩn bị sẵn thư mục và hướng dẫn (e2e handoff). Có thể làm song song: đưa ebook lên mạng (G6), bản free (G7).')
    p = d / 'video-elearning'
    if not (p / 'work' / 'project.json').exists():
        return ('G8 · Bắt đầu cắt video', 'Không cần làm gì, chờ Claude chép lời.', 'e2e handoff → v2e init --from-ebook → prepare → transcribe → align.')
    if not (p / 'PLAN.md').exists():
        return ('G8 · Chia bài', 'Chờ Claude gửi PLAN chia bài.', 'Chạy v2e align, đọc transcript, viết PLAN.md.')
    if not (p / 'edl.json').exists():
        return ('G8 · Duyệt PLAN', 'Đọc PLAN (tên bài, chỗ cắt, đoạn lỗi), sửa nếu cần, rồi "duyệt".', 'Chuyển PLAN thành edl.json.')
    n = lambda x: len([f for f in (p / x).iterdir() if not f.name.startswith('.')]) if (p / x).exists() else 0  # noqa: E731
    if n('out/thumb') == 0:
        return ('G8 · Thumbnail', 'Xem thumbnail thử (và logo/màu nếu là brand mới), rồi "duyệt".', 'Dựng 1 thumbnail thử, sau đó cả bộ.')
    if n('out/sample') == 0:
        return ('G8 · Bài mẫu', 'Xem 1 video bài mẫu, góp ý cách cắt, rồi "duyệt".', 'Render 1 bài mẫu.')
    if n('out/final') == 0:
        return ('G8 · Render cả bộ', 'Không cần làm gì (có thể để máy chạy qua đêm).', 'Render toàn bộ bài, kiểm tra chất lượng, quét lộ thông tin.')
    mp = p / 'mux-publish'
    if not MUX_TOKEN.exists():
        return ('G9 · Kết nối Mux', 'Tạo Access Token trong dashboard.mux.com (Settings → Access Tokens), rồi nói "Kết nối Mux".', 'Mở hộp thoại để bạn dán token, kiểm tra kết nối.')
    exported = mp.exists() and any((mp / 'export').glob('*/course.json'))
    if not exported:
        return ('G9 · Đăng Mux', 'Xem bảng xác nhận, chọn signed (khoá trả phí) hay public, đồng ý; xem thử video đầu tiên.',
                'Soạn nội dung bài từ ebook, mux-pub init → plan → đăng thử 1 video → đăng cả bộ → export.')
    if not (d / 'videos.json').exists():
        return ('G9 · Gắn video vào ebook', 'Đồng ý cho Claude build lại và đưa ebook có video lên mạng.', 'e2e attach-video, build, xem thử, hỏi trước khi đẩy.')
    return ('Hoàn tất', 'Kiểm tra khoá học trên LMS. Muốn làm bản free cho workshop thì nói "làm bản free".', 'Báo cáo bảng bài học, link video, thư mục bàn giao.')


def cmd_next(a):
    d = Path(a.dir).resolve()
    if not (d / 'book.json').exists():
        print('👉 Bạn: nói với Claude chủ đề khoá học muốn làm.\n🤖 Claude: tạo dự án mới (e2e new) rồi bắt đầu hỏi đáp.')
        return
    step, you, claude = next_step(d)
    print(f'Bước hiện tại: {step}\n👉 Việc tiếp theo của bạn: {you}\n🤖 Claude sẽ: {claude}')
