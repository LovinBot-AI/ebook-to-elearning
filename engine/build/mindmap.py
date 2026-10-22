"""Dựng mindmap.html (mindmap tương tác) từ mindmap.json.

mindmap.json: {"label": "...", "kids": [ {"label", "chap", "d", "p": [prompt ids], "kids": [...]}, ... ],
               "teachers": "chú thích giảng viên (tuỳ chọn)", "glossary_branch": true}
- Bấm nhánh: mở/thu gọn. Bấm ý (lá) hoặc nút i: bảng chi tiết gồm giải thích, prompt sao chép, link chương (mở tab mới).
- "p" là id prompt trong prompts.json. "glossary_branch": thêm nhánh Thuật ngữ đọc từ file book.glossary_file.
"""
import json
import re
from html import escape

from content import BOOK, ROOT
from prompt_kit import by_id

COLORS = ['#e2711d', '#1f4c86', '#1f7f79', '#12305a', '#5b47b6', '#b45309', '#2e7d32', '#a23b72', '#66727d', '#8a5a00', '#0e7490']
DATA = []


def N(label, chap=None, kids=(), d='', p=()):
    return {'label': label, 'chap': chap, 'kids': list(kids), 'd': d, 'p': list(p)}


def from_json(n):
    return N(n['label'], n.get('chap'), [from_json(k) for k in n.get('kids', [])], n.get('d', ''), n.get('p', []))


def terms_branch(label, glossary_file):
    """Nhánh thuật ngữ: mỗi bảng (## ...) trong file từ điển là một nhánh con; cột 1 = từ, cột 2 = nghĩa, cột 3 = ví dụ."""
    f = ROOT / glossary_file
    if not f.exists():
        return None
    chap = 'phu-luc-' + re.match(r'phu-luc-([a-z])', f.name).group(1) if f.name.startswith('phu-luc-') else None
    groups = []
    for sec in re.split(r'^## ', f.read_text(encoding='utf-8'), flags=re.M)[1:]:
        title = re.sub(r'^[A-Z0-9]+\.\d+\.\s*', '', sec.splitlines()[0]).strip()
        rows = [r for r in sec.splitlines() if r.startswith('|') and not r.startswith('|---')][1:]
        kids = []
        for r in rows:
            cells = [c.strip() for c in r.strip('|').split('|')]
            if len(cells) >= 2:
                d = cells[1] + (f'. Ví dụ: {cells[2]}' if len(cells) > 2 and cells[2] else '')
                kids.append(N(cells[0].replace('`', ''), chap, d=re.sub(r'[*`]', '', d)))
        if kids:
            groups.append(N(title, chap, kids))
    return N(label, chap, groups, d='Từ điển cho người học: mỗi từ một dòng giải thích và một ví dụ.') if groups else None


def node(n, P, depth=0, color=None):
    lab = f'<span class="lbl">{escape(n["label"])}</span>'
    if depth == 0:
        inner = ''.join(node(k, P, 1, COLORS[i % len(COLORS)]) for i, k in enumerate(n['kids']))
        return f'<li><div class="nd root">{lab}</div><ul>{inner}</ul></li>'
    missing = [i for i in n['p'] if i not in P]
    if missing:
        raise KeyError(f'mindmap.json: prompt không có trong prompts.json: {missing}')
    idx = len(DATA)
    DATA.append({'t': n['label'], 'c': n['chap'], 'd': n['d'],
                 'p': [{'t': P[i][1][1], 'w': P[i][1][2], 'x': P[i][1][3]} for i in n['p']]})
    badge = f'<span class="np">{len(n["p"])} prompt</span>' if n['p'] else ''
    if not n['kids']:
        return (f'<li><button type="button" class="nd leaf{" has-p" if n["p"] else ""}" data-i="{idx}" style="--c:{color}">'
                f'{lab}{badge}</button></li>')
    inner = ''.join(node(k, P, depth + 1, color) for k in n['kids'])
    info = f'<button type="button" class="info" data-i="{idx}" style="--c:{color}" aria-label="Xem chi tiết {escape(n["label"])}">i</button>'
    return (f'<li class="br closed"><span class="br-head"><button class="nd tog" type="button" style="--c:{color}" aria-expanded="false">'
            f'<span class="car">▾</span>{lab}{badge}</button>{info}</span><ul>{inner}</ul></li>')


def tabs(active: str) -> str:
    """Thanh tab dùng chung cho mindmap.html và prompt.html."""
    items = [('ebook', 'index.html', '← Ebook')]
    if (ROOT / 'mindmap.json').exists():
        items.append(('mindmap', 'mindmap.html', 'Mindmap'))
    if (ROOT / 'prompts.json').exists():
        items.append(('prompt', 'prompt.html', 'Bộ prompt'))
    return '<nav class="mm-tabs" aria-label="Chuyển trang">' + ''.join(
        f'<a href="{h}"{" class=on aria-current=page" if k == active else ""}>{t}</a>' for k, h, t in items) + '</nav>'


def build():
    cfg = json.loads((ROOT / 'mindmap.json').read_text(encoding='utf-8'))
    tree = from_json(cfg)
    if cfg.get('glossary_branch') and BOOK.get('glossary_file'):
        g = terms_branch(f'{len(tree["kids"]) + 1} · Thuật ngữ', BOOK['glossary_file'])
        if g:
            tree['kids'].append(g)
    P = by_id() if (ROOT / 'prompts.json').exists() else {}
    DATA.clear()
    html_tree = node(tree, P)
    teachers = f'<br>{cfg["teachers"]}' if cfg.get('teachers') else ''
    body = f'''<header class="mm-top">{tabs('mindmap')}
<div class="mm-act"><button type="button" id="mmAll">Mở hết</button><button type="button" id="mmNone">Thu gọn</button></div></header>
<main class="mm-wrap"><ul class="tree">{html_tree}</ul>
<p class="mm-hint">Bấm một nhánh để mở hoặc thu gọn, bấm <b>i</b> để xem giải thích. Bấm một ý để xem giải thích và prompt sao chép; ý có nhãn <span class="np">prompt</span> là có câu lệnh mẫu.{teachers}</p></main>
<div class="mm-scrim" id="mmScrim" hidden></div>
<aside class="mm-panel" id="mmPanel" aria-hidden="true" role="dialog" aria-label="Chi tiết">
<div class="mm-ph"><b id="mmT"></b><button type="button" id="mmX" aria-label="Đóng">✕</button></div><div class="mm-pb" id="mmB"></div></aside>
<div class="pk-toast" id="pkToast" role="status"></div>
<script id="mmData" type="application/json">{json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")}</script>'''
    html = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mindmap · {escape(BOOK["title"])}</title>
<link rel="stylesheet" href="ebook-assets/app/fonts.css"><link rel="stylesheet" href="ebook-assets/app/prose.css"><link rel="stylesheet" href="ebook-assets/app/mindmap.css"><link rel="stylesheet" href="ebook-assets/app/prompt-kit.css">
</head><body data-book="Mindmap" data-storage="{BOOK["storage"]}">{body}<script src="ebook-assets/app/mindmap.js"></script></body></html>'''
    (ROOT / 'mindmap.html').write_text(html, encoding='utf-8')
    print(f'mindmap: mindmap.html · {len(DATA)} ý · {sum(len(d["p"]) for d in DATA)} lượt prompt')


if __name__ == '__main__':
    build()
