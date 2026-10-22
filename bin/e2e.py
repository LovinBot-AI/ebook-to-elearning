#!/usr/bin/env python3
"""e2e — ebook-to-elearning CLI.

  e2e start [dir]                    KHỞI ĐỘNG: thiếu skill/phần mềm/kết nối nào, ai làm gì; có dir thì báo luôn việc tiếp theo
  e2e next <dir>                     việc tiếp theo của người dùng và của Claude (lời thường)
  e2e setup [--yes]                  tải + gắn skill đi kèm (video-to-elearning, mux-publisher) — chỉ --yes sau khi người dùng đồng ý
  e2e doctor                         kiểm tra môi trường (không tự cài)
  e2e new <dir> --title … --slug … [--author …] [--mark AB]
  e2e status <dir>                   các cổng G0–G7 đã duyệt chưa, tài liệu kế hoạch nào đã có
  e2e approve <dir> G2 [--note …]    ghi nhận người dùng ĐÃ duyệt một cổng (chỉ chạy sau khi họ nói đồng ý)
  e2e check <dir>                    kiểm tra cấu trúc chương, link, ảnh, id prompt, mindmap
  e2e build <dir> [web pdf epub site]
  e2e cover <dir>                    sinh ebook-assets/cover.png từ book.json → cover
  e2e free <dir> --config free.json --out <dir-free>   dựng bản free (công khai) từ bản full
  e2e sync-engine <dir>              cập nhật bộ máy build của dự án lên bản mới nhất của skill
  e2e handoff <dir>                  xuất 00-ke-hoach/handoff-v2e.json cho video-to-elearning + tạo thư mục quay-video/
  e2e attach-video <dir> --from course.json   gắn video đã đăng (Mux/YouTube) vào đầu từng chương
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import onboard  # noqa: E402
ENGINE = SKILL / 'engine'
TPL = SKILL / 'templates'
GATES = {
    'G0': 'Brief + tư liệu', 'G1': 'Thiết kế: đối tượng, trọng tâm, mục tiêu', 'G2': 'Dàn ý + phác thảo + mindmap nháp',
    'G3': 'Chương mẫu', 'G4': 'Ebook đầy đủ', 'G5': 'Kịch bản quay', 'G6': 'Đẩy GitHub / Pages', 'G7': 'Bản free',
    'G8': 'Video: dán video → video-to-elearning (PLAN, thumbnail, bài mẫu, render)', 'G9': 'Đăng Mux + gắn video vào ebook',
}
PLAN_FILES = {'G0': ['BRIEF.md', 'TU-LIEU.md'], 'G1': ['THIET-KE.md'], 'G2': ['DAN-Y.md', 'PHAC-THAO.md'], 'G5': ['KICH-BAN-QUAY.md']}
ENGINE_ITEMS = ['build', 'build_ebook.py', 'requirements.txt', 'ebook-assets/app', 'ebook-assets/fonts', '.github']


def ok(m): print(f'  ✔ {m}')
def bad(m): print(f'  ✗ {m}')
def warn(m): print(f'  ⚠ {m}')


# ------------------------------------------------------------------ doctor
def cmd_doctor(a):
    print('Python', sys.version.split()[0])
    mods = {'markdown_it': 'markdown-it-py', 'bs4': 'beautifulsoup4', 'PIL': 'pillow', 'playwright': 'playwright',
            'fitz': 'pymupdf', 'pypdf': 'pypdf', 'cryptography': 'cryptography'}
    missing = []
    for m, pkg in mods.items():
        (ok if importlib.util.find_spec(m) else bad)(pkg)
        if not importlib.util.find_spec(m):
            missing.append(pkg)
    chrome = Path('/Applications/Google Chrome.app').exists()
    (ok if chrome else warn)('Google Chrome (cần cho PDF và bìa)' if chrome else 'Không thấy Google Chrome: PDF và bìa sẽ không dựng được')
    (ok if shutil.which('ffmpeg') else warn)('ffmpeg (chỉ cần khi ebook có ảnh GIF)')
    (ok if shutil.which('gh') else warn)('GitHub CLI gh (chỉ cần khi đẩy lên GitHub, G6)')
    if missing:
        print(f'\nCòn thiếu: {", ".join(missing)}\nCài (HỎI NGƯỜI DÙNG TRƯỚC): pip install -r "{ENGINE / "requirements.txt"}"')


# ------------------------------------------------------------------ new
def copy_engine(dst: Path):
    for item in ENGINE_ITEMS:
        s = ENGINE / item
        d = dst / item
        if s.is_dir():
            shutil.copytree(s, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
        elif s.exists():
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)


def unaccent(s: str) -> str:
    import unicodedata
    s = s.replace('đ', 'd').replace('Đ', 'D')
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def fill(text: str, v: dict) -> str:
    for k, val in v.items():
        text = text.replace('{{' + k + '}}', val)
    return text


def cmd_new(a):
    d = Path(a.dir).expanduser().resolve()
    if d.exists() and any(d.iterdir()) and not a.force:
        sys.exit(f'✗ {d} đã có nội dung. Dùng --force nếu chắc chắn muốn tạo vào đây.')
    d.mkdir(parents=True, exist_ok=True)
    slug = a.slug or re.sub(r'[^A-Za-z0-9]+', '-', unaccent(a.title)).strip('-')
    mark = a.mark or ''.join(w[0] for w in a.title.split()[:2]).upper()
    today = dt.date.today()
    v = {'TITLE': a.title, 'SLUG': slug, 'AUTHOR': a.author or 'GV …', 'MARK': mark[:3],
         'MONTH': f'{today.month:02d}/{today.year}', 'DATE': today.isoformat(), 'COVER_TITLE': a.title.split(' cho ')[0][:16]}
    copy_engine(d)
    (d / '00-ke-hoach').mkdir(exist_ok=True)
    (d / 'nguon').mkdir(exist_ok=True)
    (d / 'nguon' / 'README.md').write_text('Đặt tư liệu thô của giảng viên ở đây: transcript, ảnh mindmap, tài liệu, slide. Thư mục này không đưa lên git.\n', encoding='utf-8')
    for f in ['BRIEF.md', 'TU-LIEU.md', 'THIET-KE.md', 'DAN-Y.md', 'PHAC-THAO.md', 'KICH-BAN-QUAY.md']:
        (d / '00-ke-hoach' / f).write_text(fill((TPL / f).read_text(encoding='utf-8'), v), encoding='utf-8')
    p = TPL / 'project'
    for f in ['book.json', 'mindmap.json', 'prompts.json', 'chuong-01-bat-dau.md', 'phu-luc-a-tu-dien-thuat-ngu.md', 'free.example.json']:
        (d / f).write_text(fill((p / f).read_text(encoding='utf-8'), v), encoding='utf-8')
    (d / '.gitignore').write_text((p / 'gitignore').read_text(encoding='utf-8'), encoding='utf-8')
    (d / '00-ke-hoach' / 'state.json').write_text(fill((p / 'state.json').read_text(encoding='utf-8'), v), encoding='utf-8')
    (d / 'ebook-assets' / 'diagrams').mkdir(parents=True, exist_ok=True)
    print(f'✔ Đã tạo dự án: {d}\n  Bước tiếp theo: hỏi đáp vòng 1 (docs/HOI-DAP.md) → điền 00-ke-hoach/BRIEF.md, TU-LIEU.md → cổng G0.')


# ------------------------------------------------------------------ status / approve
def load_state(d: Path) -> dict:
    f = d / '00-ke-hoach' / 'state.json'
    return json.loads(f.read_text(encoding='utf-8')) if f.exists() else {'gates': {}}


def cmd_status(a):
    d = Path(a.dir).resolve()
    st = load_state(d)
    print(f'Dự án: {d.name}')
    for g, name in GATES.items():
        rec = st['gates'].get(g)
        files = PLAN_FILES.get(g, [])
        have = [f for f in files if (d / '00-ke-hoach' / f).exists() and '{{' not in (d / '00-ke-hoach' / f).read_text(encoding='utf-8')[:400]]
        mark = '✔' if rec else '·'
        extra = f' — duyệt {rec["at"]}' + (f' ({rec["note"]})' if rec.get('note') else '') if rec else ''
        print(f'  {mark} {g} {name}{extra}' + (f'   [file: {", ".join(files)}]' if files else ''))
    nxt = next((g for g in GATES if g not in st['gates']), None)
    if nxt:
        print(f'\nCổng tiếp theo: {nxt} · {GATES[nxt]} — chưa được làm bước sau cổng này trước khi người dùng duyệt.')
    chs = sorted(d.glob('chuong-*.md'))
    print(f'Chương: {len(chs)} · Phụ lục: {len(list(d.glob("phu-luc-*.md")))}')


def cmd_approve(a):
    d = Path(a.dir).resolve()
    g = a.gate.upper()
    if g not in GATES:
        sys.exit(f'✗ Cổng không hợp lệ: {g}. Có: {", ".join(GATES)}')
    order = list(GATES)
    st = load_state(d)
    missing = [x for x in order[:order.index(g)] if x not in st['gates'] and x not in ('G6', 'G7', 'G9')]
    if missing and not a.force:
        sys.exit(f'✗ Chưa duyệt các cổng trước: {", ".join(missing)}. Không được nhảy cổng (dùng --force chỉ khi người dùng yêu cầu rõ).')
    st['gates'][g] = {'at': dt.datetime.now().strftime('%Y-%m-%d %H:%M'), 'note': a.note or ''}
    (d / '00-ke-hoach').mkdir(exist_ok=True)
    (d / '00-ke-hoach' / 'state.json').write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'✔ Đã ghi nhận duyệt {g} · {GATES[g]}')


# ------------------------------------------------------------------ check
def cmd_check(a):
    d = Path(a.dir).resolve()
    errs = warns = 0

    def E(m):
        nonlocal errs; errs += 1; bad(m)

    def W(m):
        nonlocal warns; warns += 1; warn(m)

    try:
        cfg = json.loads((d / 'book.json').read_text(encoding='utf-8'))
    except Exception as e:  # noqa: BLE001
        sys.exit(f'✗ book.json lỗi: {e}')
    chs = sorted(d.glob('chuong-[0-9][0-9]-*.md'))
    nums = [int(re.match(r'chuong-(\d+)', c.name).group(1)) for c in chs]
    covered = set()
    for p in cfg['parts']:
        lo, hi = p['chapters']
        covered |= set(range(lo, hi + 1))
    for n in nums:
        if n not in covered:
            E(f'Chương {n} không thuộc phần nào trong book.json → parts')
    if nums and nums != list(range(1, len(nums) + 1)):
        W(f'Số chương không liên tục: {nums}')
    ids = {f'chap-{n:02d}' for n in nums} | {f'phu-luc-{re.match(r"phu-luc-([a-z])", p.name).group(1)}' for p in d.glob('phu-luc-*.md')}
    for f in chs + sorted(d.glob('phu-luc-*.md')):
        t = f.read_text(encoding='utf-8')
        if not re.search(r'^# .+ — .+$', t, re.M):
            E(f'{f.name}: thiếu tiêu đề "# Chương N — Tên"')
        if 'Sau chương này' not in t and 'Sau phụ lục này' not in t:
            W(f'{f.name}: thiếu dòng "Sau chương này, bạn làm được"')
        if f.name.startswith('chuong') and not re.search(r'^- \[ \] ', t, re.M):
            W(f'{f.name}: thiếu checklist cuối chương')
        for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', t):
            src = m.group(1)
            if not src.startswith('http') and not (d / src).exists():
                E(f'{f.name}: thiếu ảnh {src}')
        for m in re.finditer(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', t):
            h = m.group(1)
            if h.startswith('#/') and h[2:] not in ids:
                E(f'{f.name}: link chương không tồn tại {h}')
        if re.search(r'(sk-[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{30,}|ghp_[A-Za-z0-9]{30,})', t):
            E(f'{f.name}: CÓ VẺ CHỨA API KEY — xoá ngay')
        if '❓' in t:
            W(f'{f.name}: còn chỗ ❓ chưa hỏi giảng viên')
    pids = set()
    if (d / 'prompts.json').exists():
        pj = json.loads((d / 'prompts.json').read_text(encoding='utf-8'))
        for s in pj.get('steps', []):
            if s.get('chap') and s['chap'] not in ids:
                E(f'prompts.json: bước {s["id"]} trỏ tới {s["chap"]} không tồn tại')
            for p in s['prompts']:
                if p[0] in pids:
                    E(f'prompts.json: trùng id {p[0]}')
                pids.add(p[0])
                for k in s['flows']:
                    if k not in pj.get('flows', {}):
                        E(f'prompts.json: bước {s["id"]} dùng nhóm "{k}" chưa khai báo trong flows')
        pids |= {t[0] for t in pj.get('templates', [])}
    if (d / 'mindmap.json').exists():
        def walk(n):
            if n.get('chap') and n['chap'] not in ids:
                E(f'mindmap.json: "{n["label"]}" trỏ tới {n["chap"]} không tồn tại')
            for p in n.get('p', []):
                if p not in pids:
                    E(f'mindmap.json: "{n["label"]}" dùng prompt "{p}" không có trong prompts.json')
            for k in n.get('kids', []):
                walk(k)
        walk(json.loads((d / 'mindmap.json').read_text(encoding='utf-8')))
    gi = (d / '.gitignore').read_text(encoding='utf-8') if (d / '.gitignore').exists() else ''
    if '.ebook-password' not in gi:
        E('.gitignore chưa chặn .ebook-password')
    print(f'\n{len(chs)} chương · {errs} lỗi · {warns} cảnh báo')
    sys.exit(1 if errs else 0)


# ------------------------------------------------------------------ build / cover
def cmd_build(a):
    d = Path(a.dir).resolve()
    sys.exit(subprocess.call([sys.executable, str(d / 'build_ebook.py'), *a.targets], cwd=d))


def cmd_cover(a):
    d = Path(a.dir).resolve()
    sys.exit(subprocess.call([sys.executable, str(d / 'build' / 'cover.py')], cwd=d))


def cmd_sync(a):
    d = Path(a.dir).resolve()
    copy_engine(d)
    print(f'✔ Đã cập nhật bộ máy build cho {d.name} (nội dung, book.json, mindmap.json, prompts.json giữ nguyên)')


# ------------------------------------------------------------------ free
def cmd_free(a):
    src = Path(a.dir).resolve()
    out = Path(a.out).expanduser().resolve()
    fc = json.loads(Path(a.config).read_text(encoding='utf-8'))
    if out.exists() and any(out.iterdir()) and not a.force:
        sys.exit(f'✗ {out} đã có nội dung. Dùng --force để ghi đè.')
    out.mkdir(parents=True, exist_ok=True)
    copy_engine(out)
    keep = sorted(fc['chapters'])
    remap = {f'chap-{o:02d}': f'chap-{i:02d}' for i, o in enumerate(keep, 1)}
    apps = [x.lower() for x in fc.get('appendices', [])]
    # chương: đánh số lại liên tục
    for i, o in enumerate(keep, 1):
        f = next(src.glob(f'chuong-{o:02d}-*.md'))
        t = f.read_text(encoding='utf-8')
        t = re.sub(r'^# Chương \d+ —', f'# Chương {i} —', t, count=1, flags=re.M)
        t = re.sub(rf'^## {o}\.(\d+)\.', rf'## {i}.\1.', t, flags=re.M)
        t = re.sub(r'^## Trước khi sang .+$', '## Trước khi kết thúc chương', t, flags=re.M)
        (out / re.sub(r'chuong-\d+', f'chuong-{i:02d}', f.name)).write_text(t, encoding='utf-8')
    for x in apps:
        for f in src.glob(f'phu-luc-{x}-*.md'):
            shutil.copy2(f, out / f.name)
    # ảnh được dùng
    for f in list(out.glob('chuong-*.md')) + list(out.glob('phu-luc-*.md')):
        for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', f.read_text(encoding='utf-8')):
            s = src / m.group(1)
            if s.exists():
                (out / m.group(1)).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(s, out / m.group(1))
    if (src / 'ebook-assets' / 'cover.png').exists():
        shutil.copy2(src / 'ebook-assets' / 'cover.png', out / 'ebook-assets' / 'cover.png')
    # book.json
    cfg = json.loads((src / 'book.json').read_text(encoding='utf-8'))
    b = cfg['book']
    b['title'] += fc.get('title_suffix', ' · Bản giới thiệu')
    b['slug'] += '-Free'
    b['storage'] = re.sub(r'[^a-z0-9]+', '-', b['slug'].lower())[:24] + '-'
    b['public'] = True
    b['cta'] = fc['cta']
    b['downloads'] = fc.get('downloads', [])
    b['resources'] = [r for r in b.get('resources', []) if not r[1].startswith('http') or fc.get('keep_external_resources')]
    b['resources'].append([fc['cta']['label'].rstrip(' →'), fc['cta']['url'], 'Xem khoá ↗'])
    if b.get('prompt_appendix') and b['prompt_appendix'].split('-')[2] not in apps:
        b.pop('prompt_appendix')
    if b.get('glossary_file') and b['glossary_file'].split('-')[2] not in apps:
        b.pop('glossary_file')
    parts = []
    for p in cfg['parts']:
        lo, hi = p['chapters']
        inside = [i for i, o in enumerate(keep, 1) if lo <= o <= hi]
        if inside:
            parts.append(dict(p, chapters=[min(inside), max(inside)]))
    for i, p in enumerate(parts, 1):
        p['id'] = f'part-{i}'
    cfg['parts'] = parts
    b['second_cta'] = ['Xem phần tiếp', parts[1]['id'] if len(parts) > 1 else parts[0]['id']]
    (out / 'book.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8')
    # prompts.json
    kept_p = set()
    if (src / 'prompts.json').exists():
        pj = json.loads((src / 'prompts.json').read_text(encoding='utf-8'))
        steps = [dict(s, chap=remap.get(s.get('chap'))) for s in pj['steps'] if s['id'] in fc.get('prompt_steps', [])]
        pj['steps'] = steps
        used = {k for s in steps for k in s['flows']}
        pj['flows'] = {k: v for k, v in pj['flows'].items() if k in used}
        kept_p = {p[0] for s in steps for p in s['prompts']} | {t[0] for t in pj.get('templates', [])}
        if steps:
            (out / 'prompts.json').write_text(json.dumps(pj, ensure_ascii=False, indent=2), encoding='utf-8')
    # mindmap.json: giữ cấu trúc (thấy độ sâu), khoá phần không có trong bản free
    if (src / 'mindmap.json').exists():
        mj = json.loads((src / 'mindmap.json').read_text(encoding='utf-8'))
        mj['label'] = b['title']
        note = fc.get('mindmap_locked_note', 'Có trong bản đầy đủ')
        app_ids = {f'phu-luc-{x}' for x in apps}

        def fix(n):
            c = n.get('chap')
            if c in remap or c in app_ids:
                n['chap'] = remap.get(c, c)
            elif c:
                n['chap'] = None
                n['d'] = (n.get('d', '') + f' 🔒 {note}.').strip()
                n['label'] = n['label'] + ' 🔒'
            n['p'] = [p for p in n.get('p', []) if p in kept_p] if (out / 'prompts.json').exists() else []
            for k in n.get('kids', []):
                fix(k)
        if fc.get('mindmap_branches', 'all') != 'all':
            mj['kids'] = [k for k in mj['kids'] if k['label'] in fc['mindmap_branches']]
        for k in mj['kids']:
            fix(k)
        mj['glossary_branch'] = bool(b.get('glossary_file'))
        (out / 'mindmap.json').write_text(json.dumps(mj, ensure_ascii=False, indent=2), encoding='utf-8')
    gi = (TPL / 'project' / 'gitignore').read_text(encoding='utf-8')
    (out / '.gitignore').write_text(gi, encoding='utf-8')
    print(f'✔ Bản free: {out}\n  {len(keep)} chương · phụ lục {", ".join(apps) or "không"} · CTA → {fc["cta"]["url"]}')
    print('  Lưu ý: nhắc tới "Chương N" trong lời văn có thể lệch số sau khi đánh số lại — rà lại bằng mắt.')
    print(f'  Build: e2e build "{out}" web site   (bản công khai, không mật khẩu). HỎI NGƯỜI DÙNG trước khi đẩy lên mạng.')


# ------------------------------------------------------------------ handoff → video-to-elearning
VIDEO_DIR = 'quay-video'
VIDEO_README = """# Dán video buổi quay vào thư mục này

Sau khi quay xong, chép vào đây (tên file tuỳ ý):

| File | Bắt buộc | Lấy ở đâu |
|---|---|---|
| Video `.mp4` | Có | Zoom: zoom.us → Recordings → Cloud recordings → buổi quay → Download "Shared screen with speaker view". Ghi trên máy: thư mục Zoom trong Documents. OBS/QuickTime: file .mp4 / .mov. |
| Transcript `.vtt` | Rất nên có | Zoom Cloud: tải file "Audio transcript" (.vtt). Có file này thì chép lời chính xác và nhanh hơn nhiều. Không có thì skill tự chép lời bằng Whisper (chậm hơn). |
| `zoom.json` | Không | Chỉ khi Zoom cho tải "Timeline" (tên người nói). |

Không cần đổi tên, không cần cắt gì. Chép xong, nói với Claude: **"Đã dán video vào quay-video, làm tiếp"**.

Lưu ý: thư mục này không đưa lên GitHub (video rất nặng và có thể lộ thông tin).
"""


def _chap_meta(d: Path, f: Path) -> dict:
    t = f.read_text(encoding='utf-8')
    n = int(re.match(r'chuong-(\d+)', f.name).group(1))
    title = re.search(r'^# (.+)$', t, re.M).group(1).strip()
    short = title.split(' — ', 1)[-1]
    goal = re.search(r'\*\*Sau chương này, bạn làm được:\*\*\s*(.+)', t)
    objectives = [x.strip(' .') for x in re.split(r';|, và | và (?=[a-zđ])', goal.group(1))] if goal else []
    sections = [re.sub(r'^\d+\.\d+\.\s*', '', h) for h in re.findall(r'^## (\d+\.\d+\..+)$', t, re.M)]
    intro = next((ln.strip() for ln in t.splitlines()[1:] if ln.strip() and not ln.startswith(('#', '>', '|', '!', '*', '-'))), '')
    checklist = [x.strip() for x in re.findall(r'^- \[ \] (.+)$', t, re.M)]
    return {'chapter': n, 'id': f'chap-{n:02d}', 'title': short, 'fullTitle': title, 'intro': re.sub(r'\*\*', '', intro),
            'objectives': [o for o in objectives if o], 'sections': sections, 'checklist': checklist, 'text': t}


def _run_of_show(d: Path) -> dict:
    """Đọc bảng trong KICH-BAN-QUAY.md: cột Đoạn = Chương, Phút, Câu mở đoạn, Không được chiếu."""
    f = d / '00-ke-hoach' / 'KICH-BAN-QUAY.md'
    out = {}
    if not f.exists():
        return out
    rows = [r for r in f.read_text(encoding='utf-8').splitlines() if r.startswith('|') and not r.startswith('|---')]
    if not rows:
        return out
    head = [c.strip().lower() for c in rows[0].strip('|').split('|')]

    def col(*keys):
        return next((i for i, h in enumerate(head) if any(k in h for k in keys)), None)
    ci, cm, cp, cn = col('chương', 'đoạn'), col('câu mở'), col('phút'), col('không được')
    for r in rows[1:]:
        c = [x.strip() for x in r.strip('|').split('|')]
        m = re.search(r'Chương (\d+)', c[ci] if ci is not None and ci < len(c) else '')
        if not m:
            continue
        out[int(m.group(1))] = {'marker': c[cm].strip('"“” ') if cm is not None and cm < len(c) else '',
                               'minutes': int(re.sub(r'\D', '', c[cp]) or 0) if cp is not None and cp < len(c) else 0,
                               'mustCut': c[cn] if cn is not None and cn < len(c) and c[cn] not in ('—', '-', '') else ''}
    return out


def cmd_handoff(a):
    d = Path(a.dir).resolve()
    cfg = json.loads((d / 'book.json').read_text(encoding='utf-8'))
    b = cfg['book']
    terms = list(b.get('proper_nouns', []))
    gf = d / b.get('glossary_file', '') if b.get('glossary_file') else None
    if gf and gf.exists():
        for r in gf.read_text(encoding='utf-8').splitlines():
            if r.startswith('|') and not r.startswith(('|---', '| Thuật ngữ')):
                term = r.strip('|').split('|')[0].strip().replace('`', '')
                if term and len(term) <= 40:
                    terms.append(term)
    prompts = {}
    if (d / 'prompts.json').exists():
        for s in json.loads((d / 'prompts.json').read_text(encoding='utf-8')).get('steps', []):
            prompts.setdefault(s.get('chap'), []).extend(p[1] for p in s['prompts'])
    ros = _run_of_show(d)
    parts = {}
    lessons = []
    for f in sorted(d.glob('chuong-[0-9][0-9]-*.md')):
        m = _chap_meta(d, f)
        n = m['chapter']
        part = next((p for p in cfg['parts'] if p['chapters'][0] <= n <= p['chapters'][1]), None)
        pkey = (part or {}).get('label', 'Phần').replace('Phần ', '') or 'A'
        if part:
            parts[pkey] = part['title']
        r = ros.get(n, {})
        low = m['text'].lower()
        lessons.append({
            'chapter': n, 'code': f'{n}.1', 'part': pkey, 'title': m['title'], 'chapterTitle': m['fullTitle'],
            'teacher': (part or {}).get('teacher') or b.get('teacher', ''),
            'marker': r.get('marker') or f'Chương {n}', 'targetMinutes': r.get('minutes') or None,
            'mustCut': r.get('mustCut', ''),
            'summary': m['intro'], 'objectives': m['objectives'], 'bullets': m['sections'][:3], 'checklist': m['checklist'],
            'keyTerms': sorted({t for t in terms if t.lower() in low})[:12], 'prompts': prompts.get(m['id'], []),
            'ebook': {'id': m['id'], 'url': (b.get('site_url', '').rstrip('/') + f'/#/{m["id"]}') if b.get('site_url') else f'#/{m["id"]}'},
        })
    vdir = d / VIDEO_DIR
    vdir.mkdir(exist_ok=True)
    (vdir / 'HUONG-DAN-DAN-VIDEO.md').write_text(VIDEO_README, encoding='utf-8')
    gi = d / '.gitignore'
    if gi.exists() and VIDEO_DIR not in gi.read_text(encoding='utf-8'):
        gi.write_text(gi.read_text(encoding='utf-8').rstrip() + f'\n{VIDEO_DIR}/\nvideo-elearning/\n', encoding='utf-8')
    videos = sorted([p for p in vdir.iterdir() if p.suffix.lower() in ('.mp4', '.mov', '.m4v')], key=lambda p: p.stat().st_size, reverse=True)
    subs = [p for p in vdir.iterdir() if p.suffix.lower() in ('.vtt', '.srt', '.sbv')]
    data = {
        'schema': 'e2e.handoff/1', 'createdAt': dt.datetime.now().isoformat(timespec='seconds'),
        'ebookDir': str(d), 'course': b['title'], 'subtitle': b.get('subtitle', ''), 'slug': b['slug'],
        'org': b.get('org', ''), 'author': b.get('author', ''), 'mode': b.get('mode', ''), 'audience': b.get('audience', ''),
        'parts': parts, 'glossaryTerms': sorted(set(terms)), 'lessons': lessons,
        'targetMinutes': sum(l['targetMinutes'] or 0 for l in lessons) or None,
        'video': {'dir': str(vdir), 'file': str(videos[0]) if videos else None, 'transcript': str(subs[0]) if subs else None,
                  'zoomJson': str(vdir / 'zoom.json') if (vdir / 'zoom.json').exists() else None},
        'mux': {'group': b['slug'].lower(), 'course': b['title']},
    }
    out = d / '00-ke-hoach' / 'handoff-v2e.json'
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'✔ {out.relative_to(d)} · {len(lessons)} bài dự kiến · {len(data["glossaryTerms"])} thuật ngữ')
    if videos:
        print(f'  Video: {videos[0].name}' + (f' · transcript: {subs[0].name}' if subs else ' · chưa có transcript (.vtt) → sẽ chép lời bằng Whisper'))
        print(f'  Tiếp: v2e init "{d / "video-elearning"}" --from-ebook "{d}"')
    else:
        print(f'  Chưa có video. Hướng dẫn giảng viên dán video vào: {vdir}  (xem HUONG-DAN-DAN-VIDEO.md)')


# ------------------------------------------------------------------ attach-video ← video-to-elearning / mux-publisher
def cmd_attach_video(a):
    """Gắn video đã đăng (Mux/YouTube) vào chương ebook: ghi videos.json, engine hiện khung 'Video bài học' đầu chương."""
    d = Path(a.dir).resolve()
    src = json.loads(Path(a.source).read_text(encoding='utf-8'))
    items = src.get('lessons', [])
    out = {}
    for l in items:
        code = str(l.get('code', ''))
        m = re.match(r'(\d+)(?:\.\d+)?$', code)
        chap = l.get('ebook', {}).get('id') if isinstance(l.get('ebook'), dict) else None
        chap = chap or (f'chap-{int(m.group(1)):02d}' if m else None)
        if not chap:
            continue
        mx = l.get('mux') or {}
        v = l.get('video') or {}
        signed = mx.get('policy') == 'signed'
        url = None if signed else (mx.get('playerUrl') or v.get('url') or l.get('url'))
        embed = mx.get('playbackId') if mx.get('policy') == 'public' else None
        if signed and not l.get('lmsUrl'):
            print(f'  ⚠ {code}: video Mux "signed" cần token để xem → chỉ gắn khi có lmsUrl (link bài trên LMS)')
            continue
        out.setdefault(chap, []).append({'code': code, 'title': l.get('title', ''), 'duration': l.get('duration', ''),
                                         'url': url, 'muxPlaybackId': embed, 'lmsUrl': l.get('lmsUrl', '')})
    (d / 'videos.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    n = sum(len(v) for v in out.values())
    print(f'✔ videos.json · {n} video gắn vào {len(out)} chương. Build lại: e2e build "{d}" web site  (HỎI trước khi đẩy lên mạng)')
    skipped = [str(l.get('code')) for l in items if not re.match(r'\d+(\.\d+)?$', str(l.get('code', ''))) and not isinstance(l.get('ebook'), dict)]
    if skipped:
        print(f'  ⚠ Không gắn được (mã không theo dạng <chương>.<n>): {", ".join(skipped)}')


def main():
    ap = argparse.ArgumentParser(prog='e2e', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('start'); p.add_argument('dir', nargs='?'); p.set_defaults(f=onboard.cmd_start)
    p = sp.add_parser('next'); p.add_argument('dir'); p.set_defaults(f=onboard.cmd_next)
    p = sp.add_parser('setup'); p.add_argument('--yes', action='store_true'); p.set_defaults(f=onboard.cmd_setup)
    sp.add_parser('doctor').set_defaults(f=cmd_doctor)
    p = sp.add_parser('new'); p.add_argument('dir'); p.add_argument('--title', required=True); p.add_argument('--slug')
    p.add_argument('--author'); p.add_argument('--mark'); p.add_argument('--force', action='store_true'); p.set_defaults(f=cmd_new)
    p = sp.add_parser('status'); p.add_argument('dir'); p.set_defaults(f=cmd_status)
    p = sp.add_parser('approve'); p.add_argument('dir'); p.add_argument('gate'); p.add_argument('--note')
    p.add_argument('--force', action='store_true'); p.set_defaults(f=cmd_approve)
    p = sp.add_parser('check'); p.add_argument('dir'); p.set_defaults(f=cmd_check)
    p = sp.add_parser('build'); p.add_argument('dir'); p.add_argument('targets', nargs='*'); p.set_defaults(f=cmd_build)
    p = sp.add_parser('cover'); p.add_argument('dir'); p.set_defaults(f=cmd_cover)
    p = sp.add_parser('sync-engine'); p.add_argument('dir'); p.set_defaults(f=cmd_sync)
    p = sp.add_parser('handoff'); p.add_argument('dir'); p.set_defaults(f=cmd_handoff)
    p = sp.add_parser('attach-video'); p.add_argument('dir'); p.add_argument('--from', dest='source', required=True); p.set_defaults(f=cmd_attach_video)
    p = sp.add_parser('free'); p.add_argument('dir'); p.add_argument('--config', required=True); p.add_argument('--out', required=True)
    p.add_argument('--force', action='store_true'); p.set_defaults(f=cmd_free)
    a = ap.parse_args()
    a.f(a)


if __name__ == '__main__':
    main()
