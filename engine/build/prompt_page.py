"""Dựng prompt.html: bộ prompt sao chép cho học viên, lọc theo nhóm/luồng, có ô tìm kiếm."""
import re
from html import escape

from content import BOOK
from mindmap import tabs
from prompt_kit import FLOWS, ROOT, STEPS, TEMPLATES


def fill(text: str) -> str:
    """Tô sáng chỗ cần tự điền [ ... ]."""
    return re.sub(r'\[([^\]]+)\]', r'<mark>[\1]</mark>', escape(text)).replace('\n', '<br>')


def card(pid, title, when, text, chap=None):
    link = f'<a class="pk-ch" href="index.html#/{chap}" target="_blank" rel="noopener">Đọc chương ↗</a>' if chap else ''
    return (f'<article class="pk-card" id="p-{pid}" data-q="{escape((title + " " + when + " " + text).lower())}">'
            f'<header><h3>{escape(title)}</h3><button type="button" class="pk-copy" aria-label="Sao chép prompt {escape(title)}">Sao chép</button></header>'
            f'<p class="pk-when"><b>Dùng khi:</b> {escape(when)}</p>'
            f'<div class="pk-text">{fill(text)}</div><textarea hidden>{escape(text)}</textarea>{link}</article>')


def build():
    chips = '<button type="button" class="pk-chip on" data-f="all">Tất cả</button>' + ''.join(
        f'<button type="button" class="pk-chip" data-f="{k}">{escape(n)}</button>' for k, (n, _) in FLOWS.items())
    rails = ''.join(
        f'<ol class="pk-rail" data-f="{k}" hidden>' + ''.join(
            f'<li><a href="#s-{s["id"]}">{escape(s["name"])}</a></li>' for s in STEPS if k in s['flows']) +
        '</ol>' for k in FLOWS)
    secs, n = [], 0
    for i, s in enumerate(STEPS, 1):
        tags = ''.join(f'<span class="pk-tag">{escape(FLOWS[k][0].split(" · ")[0] if k in FLOWS else k)}</span>' for k in s['flows'])
        cards = ''.join(card(*p, chap=s.get('chap')) for p in s['prompts'])
        n += len(s['prompts'])
        secs.append(f'<section class="pk-sec" id="s-{s["id"]}" data-flows="{s["flows"]}">'
                    f'<h2><span class="pk-n">{i}</span>{escape(s["name"])} {tags}</h2>'
                    f'<p class="pk-intro">{escape(s.get("intro", ""))}</p><div class="pk-grid">{cards}</div></section>')
    if TEMPLATES:
        tpl = ''.join(card(*t) for t in TEMPLATES)
        secs.append(f'<section class="pk-sec" id="s-mau" data-flows="{"".join(FLOWS)}"><h2><span class="pk-n">+</span>Mẫu điền sẵn</h2>'
                    f'<p class="pk-intro">Sao chép, điền vào chỗ tô vàng, rồi dán cho AI.</p><div class="pk-grid">{tpl}</div></section>')
    flows_help = ''.join(f'<li><b>{escape(nm)}:</b> {escape(d)}</li>' for nm, d in FLOWS.values())
    teacher = f'<p class="pk-teacher">{BOOK["prompt_teachers"]}</p>' if BOOK.get('prompt_teachers') else ''
    chips_html = f'<div class="pk-chips">{chips}</div>{rails}' if FLOWS else ''

    body = f'''<header class="mm-top pk-top">{tabs('prompt')}</header>
<main class="pk-wrap">
<div class="pk-hero"><h1>Bộ prompt sao chép · {escape(BOOK["title"])}</h1>
<p>{n} prompt theo từng bước của khoá. Chọn nhóm, tìm bước, bấm <b>Sao chép</b>, thay chỗ <mark>[tô vàng]</mark> bằng nội dung của bạn rồi dán cho AI.</p>
<ul class="pk-flows">{flows_help}</ul>{teacher}</div>
<div class="pk-bar"><input type="search" id="pkQ" placeholder="Tìm prompt theo từ khoá…" aria-label="Tìm prompt">
{chips_html}<p class="pk-count" id="pkCount"></p></div>
{''.join(secs)}
<p class="pk-empty" id="pkEmpty" hidden>Không có prompt nào khớp. Thử từ khác, hoặc chọn "Tất cả".</p>
</main><div class="pk-toast" id="pkToast" role="status"></div>'''
    html = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bộ prompt · {escape(BOOK["title"])}</title>
<link rel="stylesheet" href="ebook-assets/app/fonts.css"><link rel="stylesheet" href="ebook-assets/app/prose.css"><link rel="stylesheet" href="ebook-assets/app/mindmap.css"><link rel="stylesheet" href="ebook-assets/app/prompt-kit.css">
</head><body data-book="Prompt" data-storage="{BOOK["storage"]}">{body}<script src="ebook-assets/app/prompt-kit.js"></script></body></html>'''
    (ROOT / 'prompt.html').write_text(html, encoding='utf-8')
    print(f'prompt: prompt.html · {n} prompt + {len(TEMPLATES)} mẫu')


if __name__ == '__main__':
    build()
