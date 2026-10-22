"""Dựng ebook: web reader (index.html), PDF (A4) và EPUB 3 từ cùng bộ Markdown.

    python3 build_ebook.py            # web + pdf + epub
    python3 build_ebook.py web        # chỉ web
    python3 build_ebook.py pdf epub   # chọn đầu ra
"""
from __future__ import annotations

import datetime as dt
import json
import re
import shutil
import sys
import uuid
import zipfile
from html import escape
from urllib.parse import quote
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'build'))
from content import BOOK, PARTS, ROOT, load_chapters, render, theme_css, to_xhtml  # noqa: E402

DIST = ROOT / 'downloads'
APP = 'ebook-assets/app'
COVER_IMG = 'ebook-assets/cover.png'
TODAY = dt.date.today()
ACCENT = {p['id'] for p in PARTS if p.get('accent')}


def parts_with(chs):
    return [(p, [c for c in chs if c.part == p['id']]) for p in PARTS]


def toc_num(c):
    return c.num


# ============================================================== WEB
def build_web(chs):
    vids = json.loads((ROOT / 'videos.json').read_text(encoding='utf-8')) if (ROOT / 'videos.json').exists() else {}

    def video_box(cid):
        items = vids.get(cid) or []
        if not items:
            return ''
        out = []
        for v in items:
            head = f'<p class="vb-title"><b>{escape(v["code"])}</b> {escape(v["title"])}' + (f' <small>{escape(v["duration"])}</small>' if v.get('duration') else '') + '</p>'
            if v.get('muxPlaybackId'):
                src = f'https://player.mux.com/{v["muxPlaybackId"]}?metadata-video-title={quote(v["title"])}&metadata-video-id={quote(v["code"])}'
                out.append(head + f'<div class="vb-frame"><iframe src="{src}" loading="lazy" allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture;" allowfullscreen title="{escape(v["title"])}"></iframe></div>')
            else:
                link = v.get('lmsUrl') or v.get('url')
                if link:
                    out.append(head + f'<a class="btn" href="{escape(link)}" target="_blank" rel="noopener">▶ Xem video bài này</a>')
        return f'<aside class="video-box"><span class="vb-k">🎬 Video bài học</span>{"".join(out)}</aside>' if out else ''

    top_tabs = ''.join(f'<a href="{h}">{t}</a>' for f, h, t in
                       [('mindmap.json', 'mindmap.html', 'Mindmap'), ('prompts.json', 'prompt.html', 'Bộ prompt')] if (ROOT / f).exists())
    top_tabs = f'<nav class="top-tabs" aria-label="Tài nguyên">{top_tabs}</nav>' if top_tabs else ''
    cta = BOOK.get('cta')
    cta_btn = f'<a class="btn cta" href="{escape(cta["url"])}" target="_blank" rel="noopener">{escape(cta["label"])}</a>' if cta else ''
    cta_box = (f'<aside class="cta-box"><p>{escape(cta.get("text", ""))}</p><a class="btn cta" href="{escape(cta["url"])}" target="_blank" rel="noopener">{escape(cta["label"])}</a></aside>') if cta else ''
    bodies = {c.id: render(c, 'web') for c in chs}
    toc = []
    for p, items in parts_with(chs):
        toc.append(f'<div class="toc-part"><div class="toc-part-head"><b>{p["label"]}</b>{escape(p["title"].split(":")[0])}</div>')
        for c in items:
            toc.append(f'<a class="toc-link" href="#/{c.id}" data-target="{c.id}"><span class="toc-num">{c.num}</span>'
                       f'<span class="toc-title">{escape(c.short)}</span><span class="toc-done" aria-label="đã đọc">✓</span></a>')
        toc.append('</div>')

    order = [c.id for c in chs]
    sections = []
    for i, c in enumerate(chs):
        part = next(p for p in PARTS if p['id'] == c.part)
        prev_c = chs[i - 1] if i > 0 else None
        next_c = chs[i + 1] if i + 1 < len(chs) else None
        chips = f'<span class="chip{" adv" if c.part in ACCENT else (" app" if c.kind == "appendix" else "")}">{part["label"]}</span>'
        outline = ''.join(f'<li><a href="#/{c.id}" data-scroll="{hid}">{escape(t)}</a></li>' for hid, t in c.sections
                          if not re.match(r'^(Trước khi|Kết thúc)', t))
        head = (f'<header class="ch-head{" adv" if c.part in ACCENT else ""}"><div class="ch-kicker">{chips}</div>'
                f'<h1><span>{escape(c.label)}</span>{escape(c.short)}</h1>'
                f'<div class="ch-meta"><span>⏱ khoảng {c.minutes} phút đọc</span><span>§ {len(c.sections)} mục</span></div>'
                + (f'<nav class="ch-outline" aria-label="Trong chương này"><b>Trong chương này</b><ul>{outline}</ul></nav>' if outline else '')
                + '</header>')
        pager = ('<nav class="pager">'
                 + (f'<button class="prev" type="button"><small>← Trước</small><span>{escape(prev_c.label)} · {escape(prev_c.short)}</span></button>' if prev_c else '<button class="prev" type="button" hidden></button>')
                 + (f'<button class="next" type="button"><small>Tiếp →</small><span>{escape(next_c.label)} · {escape(next_c.short)}</span></button>' if next_c else '<button class="next" type="button" hidden></button>')
                 + '</nav>')
        sections.append(f'<section class="chapter" id="{c.id}" data-title="{escape(c.label)} — {escape(c.short)}">{head}'
                        f'<article class="article prose">{video_box(c.id)}{bodies[c.id]}{cta_box}</article>{pager}</section>')

    part_cards = []
    for p, items in parts_with(chs):
        lis = ''.join(f'<li><button type="button" data-target="{c.id}"><b>{c.num}</b>{escape(c.short)}</button></li>' for c in items)
        part_cards.append(f'<div class="part-card{" adv" if p["id"] in ACCENT else ""}"><span class="lbl">{p["label"]}</span>'
                          f'<h3>{escape(p["title"])}</h3><p>{escape(p["desc"])}</p><p class="part-teacher">Giảng viên: <b>{escape(p["teacher"])}</b></p><ol>{lis}</ol></div>')
    n_ch = sum(1 for c in chs if c.kind == 'chapter')
    n_ap = sum(1 for c in chs if c.kind == 'appendix')
    n_fig = sum(bodies[c.id].count('<figure') for c in chs)
    n_prompt = sum(bodies[c.id].count('class="prompt"') for c in chs)
    first_adv = next(c.id for c in chs if c.part == BOOK['second_cta'][1])
    pdf_name, epub_name = f'{BOOK["slug"]}.pdf', f'{BOOK["slug"]}.epub'
    dl = BOOK.get('downloads', ['pdf', 'epub'])
    dl_sheet = (f'<a href="downloads/{pdf_name}" download>Ebook PDF · in, đọc trên máy tính <small>A4</small></a>' if 'pdf' in dl else '') + (f'<a href="downloads/{epub_name}" download>Ebook EPUB · Apple Books, Google Play Sách <small>EPUB 3</small></a>' if 'epub' in dl else '')
    dl_btns = (f'<a class="btn" href="downloads/{pdf_name}" download>⬇ PDF</a>' if 'pdf' in dl else '') + (f'<a class="btn ghost" href="downloads/{epub_name}" download>⬇ EPUB</a>' if 'epub' in dl else '')
    res_btns = ''.join(f'<a class="btn ghost" href="{u}"{" target=_blank rel=noopener" if u.startswith("http") else ""}>{escape(l)}</a>' for l, u, _ in BOOK['resources'])
    res_list = ''.join(f'<a href="{u}"{" target=_blank rel=noopener" if u.startswith("http") else ""}>{escape(l)} <small>{escape(n)}</small></a>' for l, u, n in BOOK['resources'])

    cover = f'''<section class="cover" id="cover">
<div class="hero"><div>
<span class="hero-tag">📘 {escape(BOOK["edition"])}</span>
<h1>{BOOK["hero_title_html"]}</h1>
<p class="hero-sub">{escape(BOOK["subtitle"])}.</p>
<p class="hero-author">{escape(BOOK["author"])}</p>
<div class="hero-actions">
{cta_btn}<button class="btn primary" type="button" data-target="chap-01">Bắt đầu đọc →</button>
<button class="btn teal" type="button" data-target="{first_adv}">{BOOK["second_cta"][0]}</button>
<button class="btn" type="button" id="continueBtn" hidden><span>Đọc tiếp</span></button>
</div></div>
<div class="hero-cover"><img src="{COVER_IMG}" alt="Bìa ebook {escape(BOOK["title"])}"></div></div>
<div class="stats"><div class="stat"><b>{n_ch}</b><span>chương thực hành</span></div><div class="stat"><b>{n_ap}</b><span>phụ lục tra cứu</span></div>
<div class="stat"><b>{n_fig}</b><span>hình, sơ đồ, ảnh thật</span></div><div class="stat"><b>{n_prompt}</b><span>prompt mẫu sao chép được</span></div></div>
<div class="parts">{"".join(part_cards)}</div>
<div class="dl-card"><div><h3>Tài nguyên tải về</h3><p>Ebook PDF để in, EPUB cho Apple Books, Google Play Sách, Kindle; mindmap tương tác và các repo dùng trong khoá.</p></div>
<div class="hero-actions">{dl_btns}{res_btns}</div></div>
</section>'''

    html = f'''<!doctype html>
<html lang="vi"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{escape(BOOK["title"])} · Ebook khoá e-learning</title>
<meta name="description" content="{escape(BOOK["subtitle"])}">
<meta name="theme-color" content="#12305a"><meta name="color-scheme" content="light dark">
<meta property="og:title" content="{escape(BOOK["title"])}"><meta property="og:image" content="{COVER_IMG}">
<link rel="icon" href="{COVER_IMG}">
<link rel="stylesheet" href="{APP}/fonts.css"><link rel="stylesheet" href="{APP}/prose.css"><link rel="stylesheet" href="{APP}/reader.css">{theme_css()}
<script>try{{const p=JSON.parse(localStorage.getItem('{BOOK["storage"]}prefs')||'{{}}');if(p.theme&&p.theme!=='light')document.documentElement.dataset.theme=p.theme}}catch(e){{}}</script>
</head>
<body data-book="{escape(BOOK["title"])}" data-storage="{BOOK["storage"]}">
<header class="topbar">
<button class="icon-btn menu-btn" id="menuBtn" type="button" aria-label="Mục lục">☰</button>
<button class="brand" type="button" data-target="cover"><span class="brand-mark">{BOOK["brand_mark"]}</span><span>{escape(BOOK["title"])}<small>Ebook khoá e-learning</small></span></button>
<div class="top-chapter" id="topChapter">Trang bìa</div>
{top_tabs}
<div class="top-actions">
<button class="icon-btn" id="fontBtn" type="button" aria-label="Cỡ chữ và giao diện">Aa</button>
<button class="icon-btn hide-m" id="themeBtn" type="button" aria-label="Chế độ sáng tối">◐</button>
<button class="icon-btn primary" id="dlBtn" type="button">⬇<span class="hide-m">&nbsp;Tải</span></button>
</div>
<div class="progress"><span id="progressBar"></span></div>
</header>
<div class="layout">
<aside class="toc" id="toc" aria-label="Mục lục">
<div class="toc-progress"><div class="toc-progress-top"><span>Tiến độ đọc</span><span data-read-count>0</span></div><div class="toc-progress-bar"><span data-read-bar></span></div></div>
<a class="toc-link" href="#/cover" data-target="cover"><span class="toc-num">◎</span><span class="toc-title">Trang bìa</span></a>
{"".join(toc)}
<div class="toc-foot">{escape(BOOK["edition"])}<br>{escape(BOOK["author"])}</div>
</aside>
<main class="main"><div class="page">
{cover}
{"".join(sections)}
</div></main>
<aside class="rail" id="rail" aria-label="Trong chương"></aside>
</div>
<nav class="bottom-nav" aria-label="Điều hướng">
<button type="button" id="navPrev"><i>‹</i>Trước</button>
<button type="button" id="navToc"><i>☰</i>Mục lục</button>
<button type="button" id="navFont"><i>Aa</i>Giao diện</button>
<button type="button" id="navNext"><i>›</i>Tiếp</button>
</nav>
<div class="scrim"></div>
<div class="sheet" id="fontSheet" role="dialog" aria-label="Giao diện đọc">
<h4>Giao diện</h4><div class="seg"><button type="button" data-theme-set="light">Sáng</button><button type="button" data-theme-set="sepia">Giấy</button><button type="button" data-theme-set="dark">Tối</button><button type="button" data-theme-set="light" aria-hidden="true" style="visibility:hidden"></button></div>
<label>Cỡ chữ</label><div class="seg"><button type="button" data-fs="16">A−</button><button type="button" data-fs="18">A</button><button type="button" data-fs="20">A+</button><button type="button" data-fs="22">A++</button></div>
<label>Độ rộng dòng</label><div class="seg"><button type="button" data-width="660">Hẹp</button><button type="button" data-width="760">Vừa</button><button type="button" data-width="880">Rộng</button><button type="button" data-width="1000">Rất rộng</button></div>
</div>
<div class="sheet" id="dlSheet" role="dialog" aria-label="Tài nguyên tải về"><h4>Tài nguyên tải về</h4><div class="dl-list">
{dl_sheet}
{res_list}</div></div>
<dialog class="zoom" id="zoom"><button class="icon-btn" id="zoomClose" type="button">Đóng ✕</button><img alt=""><p></p></dialog>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="{APP}/reader.js" defer></script>
</body></html>'''
    (ROOT / 'index.html').write_text(html, encoding='utf-8')
    (ROOT / 'ebook-reader.html').write_text(html, encoding='utf-8')
    print(f'web: index.html {len(html)//1024} KB · {len(chs)} phần · {n_fig} hình · {n_prompt} prompt')


# ============================================================== PRINT / PDF
def print_html(chs, pages=None):
    pages = pages or {}
    bodies = {c.id: render(c, 'print') for c in chs}
    toc = ['<section class="pdf-toc"><h2>Mục lục</h2>']
    for p, items in parts_with(chs):
        toc.append(f'<div class="tp">{p["label"]}<b>{escape(p["title"])}</b></div>')
        for c in items:
            pg = pages.get(c.id, '')
            toc.append(f'<a class="row" href="#{c.id}"><span class="n">{c.num}</span><span class="t">{escape(c.short)}</span><span class="p">{pg}</span></a>')
    toc.append('</section>')
    out = []
    for p, items in parts_with(chs):
        lis = ''.join(f'<li><b>{c.num}</b>{escape(c.short)}</li>' for c in items)
        out.append(f'<section class="pdf-part{" adv" if p["id"] in ACCENT else ""}"><span class="pdf-marker" style="color:transparent">@@{p["id"]}@@</span><div class="pl">{p["label"]}</div><h2>{escape(p["title"])}</h2>'
                   f'<p>{escape(p["desc"])}</p><p class="part-teacher">Giảng viên: <b>{escape(p["teacher"])}</b></p><ol>{lis}</ol></section>')
        for c in items:
            outline = ''.join(f'<li>{escape(t)}</li>' for _, t in c.sections if not re.match(r'^(Trước khi|Kết thúc)', t))
            out.append(f'<section class="pdf-chapter" id="{c.id}"><span class="pdf-marker">@@{c.id}@@</span>'
                       f'<header class="pdf-ch-head"><div class="k">{escape(c.label)}<i>· {escape(next(p["label"] for p in PARTS if p["id"] == c.part))}</i></div>'
                       f'<h1>{escape(c.short)}</h1><div class="m">Khoảng {c.minutes} phút đọc</div>'
                       + (f'<ol>{outline}</ol>' if outline else '') + f'</header><div class="prose">{bodies[c.id]}</div></section>')
    cover = f'''<section class="pdf-cover"><div class="c-top"><span>{escape(BOOK["org"])}</span><span>{escape(BOOK["edition"])}</span></div>
<img class="c-img" src="{COVER_IMG}" alt="">
<div class="c-text"><span class="c-tag">{escape(BOOK["cover_tag"])}</span><h1>{BOOK["cover_title_html"]}</h1>
<p class="c-sub">{escape(BOOK["subtitle"])}.</p><p class="c-author">{escape(BOOK["author"])}</p></div>
<div class="c-foot"><span>{escape(BOOK["tagline"])}</span><span>{escape(BOOK["org_url"])}</span></div></section>'''
    info = f'''<section class="pdf-info"><h2>{escape(BOOK["title"])}</h2>
<p><b>{escape(BOOK["subtitle"])}.</b></p>
<p>{escape(BOOK["edition"])}. Tác giả: {escape(BOOK["author"])}.</p>
<p>{escape(BOOK['info'])}</p>
<div class="box"><b>Cách đọc:</b> khung <b>PROMPT MẪU</b> là câu lệnh bạn sao chép và chỉnh theo dự án của mình. Khung màu là mẹo, lưu ý và cảnh báo. Mỗi chương kết thúc bằng một checklist để tự kiểm trước khi sang chương sau.</div>
<div class="box"><b>Lưu ý:</b> giao diện các dịch vụ (GitHub, Supabase, Vercel, Tripo) thay đổi theo thời gian; hãy bám theo tên mục hơn là vị trí nút. Khoá bí mật trong ảnh minh họa đã được làm mờ. Giá các gói trả phí xem trên trang chính thức.</div>
<p style="margin-top:10mm;font-size:8.5pt;color:#7a8692">© {TODAY.year} {escape(BOOK["org"])}. Phông chữ Be Vietnam Pro và JetBrains Mono theo giấy phép SIL Open Font License.</p></section>'''
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>{escape(BOOK["title"])}</title>
<link rel="stylesheet" href="{APP}/fonts.css"><link rel="stylesheet" href="{APP}/prose.css"><link rel="stylesheet" href="{APP}/print.css">{theme_css()}</head>
<body>{cover}{info}{"".join(toc)}{"".join(out)}</body></html>'''


def build_pdf(chs):
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter
    DIST.mkdir(exist_ok=True)
    tmp_html = ROOT / 'print.html'
    footer = ('<div style="width:100%;font-family:Arial,sans-serif;font-size:7.5px;color:#7a8692;padding:0 18mm;display:flex;justify-content:space-between">'
              f'<span>{escape(BOOK["title"])} · {escape(BOOK["org"])}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')

    def render_pdf(html, out, with_footer=True):
        tmp_html.write_text(html, encoding='utf-8')
        with sync_playwright() as p:
            br = p.chromium.launch(channel='chrome')
            pg = br.new_page()
            pg.goto(tmp_html.as_uri(), wait_until='networkidle')
            pg.evaluate('document.fonts.ready')
            kw = dict(path=str(out), format='A4', print_background=True, prefer_css_page_size=True,
                      display_header_footer=with_footer, header_template='<div></div>', footer_template=footer,
                      margin={'top': '20mm', 'bottom': '22mm', 'left': '18mm', 'right': '18mm'})
            try:
                pg.pdf(outline=True, tagged=True, **kw)
            except TypeError:
                pg.pdf(**kw)
            br.close()

    out = DIST / f'{BOOK["slug"]}.pdf'
    # lượt 1: tìm số trang của từng chương
    render_pdf(print_html(chs), out)
    reader = PdfReader(str(out))
    pages = {}
    for i, page in enumerate(reader.pages):
        txt = page.extract_text() or ''
        for m in re.findall(r'@@([a-z0-9-]+)@@', txt):
            pages.setdefault(m, i + 1)
    # lượt 2: mục lục có số trang
    render_pdf(print_html(chs, pages), out)
    # bìa và trang phần: thay bằng bản không có chân trang; thêm bookmark + metadata
    import fitz
    bare = DIST / '_bare.pdf'
    render_pdf(print_html(chs, pages), bare, with_footer=False)
    doc, nb = fitz.open(out), fitz.open(bare)
    special = [0] + [i for i in range(doc.page_count) if re.search(r'@@part-\d@@', doc[i].get_text())]
    for i in special:
        doc.delete_page(i)
        doc.insert_pdf(nb, from_page=i, to_page=i, start_at=i)
    nb.close()
    toc = [[1, 'Bìa', 1], [1, 'Mục lục', 3]]
    pp = {p['id']: next((i + 1 for i in range(doc.page_count) if f'@@{p["id"]}@@' in doc[i].get_text()), None) for p in PARTS}
    for p, items in parts_with(chs):
        if pp.get(p['id']):
            toc.append([1, f'{p["label"]} · {p["title"]}', pp[p['id']]])
        for c in items:
            if pages.get(c.id):
                toc.append([2, f'{c.label} · {c.short}', pages[c.id]])
    doc.set_toc(toc)
    doc.set_metadata({'title': BOOK['title'], 'author': BOOK['author'], 'subject': BOOK['subtitle'], 'creator': BOOK['org'], 'producer': BOOK['org'], 'keywords': BOOK['keywords']})
    final = DIST / '_final.pdf'
    doc.save(final, garbage=4, deflate=True)
    doc.close()
    final.replace(out)
    bare.unlink(missing_ok=True)
    reader = PdfReader(str(out))
    tmp_html.unlink(missing_ok=True)
    print(f'pdf: {out.name} · {len(reader.pages)} trang · {out.stat().st_size/1e6:.1f} MB · TOC: {len(pages)}/{len(chs)} chương có số trang')


# ============================================================== EPUB
EPUB_CSS = '''
@font-face{font-family:"Be Vietnam Pro";src:url(fonts/BeVietnamPro-Regular.ttf);font-weight:400;font-style:normal}
@font-face{font-family:"Be Vietnam Pro";src:url(fonts/BeVietnamPro-Italic.ttf);font-weight:400;font-style:italic}
@font-face{font-family:"Be Vietnam Pro";src:url(fonts/BeVietnamPro-Bold.ttf);font-weight:700;font-style:normal}
@font-face{font-family:"Be Vietnam Pro";src:url(fonts/BeVietnamPro-ExtraBold.ttf);font-weight:800;font-style:normal}
@font-face{font-family:"JetBrains Mono";src:url(fonts/JetBrainsMono.ttf)}
body{margin:0 4%;font-family:"Be Vietnam Pro",sans-serif;color:#1e2833;line-height:1.6}
h1{font-family:"Be Vietnam Pro",sans-serif;color:#12305a}
nav#toc a{color:#12305a;text-decoration:none}
nav#toc>ol>li>a{font-weight:700}
.ch-k{font-family:"Be Vietnam Pro",sans-serif;font-size:.75em;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#e2711d;margin:1.5em 0 .3em}
h1.ch-t{font-family:"Be Vietnam Pro",sans-serif;font-size:1.7em;line-height:1.2;color:#12305a;margin:0 0 .6em}
.ch-ol{list-style:none;font-size:.85em;line-height:1.55;color:#3a4754;background:#f6f7f9;padding:.7em 1em;border-radius:8px;margin:0 0 1.4em}
.part-page{text-align:left;padding-top:20%}
.part-page .pl{font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:#e2711d}
.part-page h1{font-size:2em;color:#12305a;line-height:1.15}
.cover-page{text-align:center;margin:0;padding:0}
.cover-page img{max-width:100%;max-height:100%}
.prose .table-wrap{overflow:visible;border:0}
.prose table{font-size:.8em}
.prose figure img{box-shadow:none;max-height:80vh}
.prose .callout{display:block}
.prose .callout-icon{float:left;margin-right:.5em}
.prose li.task{display:block}
.prose .task-box-print{margin-right:.4em}
nav#toc ol{list-style:none;padding-left:0}
nav#toc li{margin:.35em 0}
nav#toc ol ol{padding-left:1.2em}
'''


def build_epub(chs):
    DIST.mkdir(exist_ok=True)
    out = DIST / f'{BOOK["slug"]}.epub'
    prose_css = (ROOT / APP / 'prose.css').read_text(encoding='utf-8')
    uid = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL, BOOK['uuid_seed']))
    modified = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    files = {}      # path in OEBPS → bytes|str
    media = {}      # src rel → OEBPS path

    def xhtml(title, body, cls=''):
        return (f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="vi" xml:lang="vi">'
                f'<head><meta charset="utf-8"/><title>{escape(title)}</title><link rel="stylesheet" type="text/css" href="css/book.css"/></head>'
                f'<body class="{cls}">{body}</body></html>')

    def collect(html):
        def rep(m):
            src = m.group(2)
            if src.startswith('http'):
                return m.group(0)
            f = ROOT / src
            if not f.exists():
                return m.group(0)
            if src not in media:
                media[src] = f'images/{len(media):03d}-{f.name}'
                files[media[src]] = f.read_bytes()
            return f'{m.group(1)}"{media[src]}"'
        return re.sub(r'(src=)"([^"]+)"', rep, html)

    spine = []
    # bìa
    cov_path = 'images/cover' + Path(COVER_IMG).suffix
    files[cov_path] = (ROOT / COVER_IMG).read_bytes()
    files['cover.xhtml'] = xhtml('Bìa', f'<div class="cover-page"><img src="{cov_path}" alt="{escape(BOOK["title"])}"/></div>', 'cover-page')
    spine.append(('cover.xhtml', 'Bìa'))
    files['info.xhtml'] = xhtml('Giới thiệu', f'<div class="prose"><h1 class="ch-t">{escape(BOOK["title"])}</h1><p><b>{escape(BOOK["subtitle"])}.</b></p>'
                                f'<p>{escape(BOOK["edition"])}<br/>{escape(BOOK["author"])}</p>'
                                '<p>Khung <b>PROMPT MẪU</b> là câu lệnh để sao chép và chỉnh theo dự án của bạn. Khung màu là mẹo, lưu ý và cảnh báo. Mỗi chương kết thúc bằng một checklist tự kiểm.</p></div>')
    spine.append(('info.xhtml', 'Giới thiệu'))
    nav_parts = []
    for p, items in parts_with(chs):
        pf = f'{p["id"]}.xhtml'
        lis = ''.join(f'<li>{c.num} · {escape(c.short)}</li>' for c in items)
        files[pf] = xhtml(p['label'], f'<div class="part-page"><div class="pl">{p["label"]}</div><h1>{escape(p["title"])}</h1><p>{escape(p["desc"])}</p><p class="part-teacher">Giảng viên: <b>{escape(p["teacher"])}</b></p><ol>{lis}</ol></div>')
        spine.append((pf, p['label']))
        sub = []
        for c in items:
            body = to_xhtml(render(c, 'epub'))
            body = collect(body)
            outline = ''.join(f'<li>{escape(t)}</li>' for _, t in c.sections if not re.match(r'^(Trước khi|Kết thúc)', t))
            cf = f'{c.id}.xhtml'
            files[cf] = xhtml(c.title, f'<section epub:type="chapter"><div class="ch-k">{escape(c.label)}</div><h1 class="ch-t">{escape(c.short)}</h1>'
                              + (f'<ol class="ch-ol">{outline}</ol>' if outline else '') + f'<div class="prose">{body}</div></section>')
            spine.append((cf, c.title))
            sub.append(f'<li><a href="{cf}">{escape(c.label)} · {escape(c.short)}</a></li>')
        nav_parts.append(f'<li><a href="{pf}">{p["label"]} · {escape(p["title"])}</a><ol>{"".join(sub)}</ol></li>')
    files['nav.xhtml'] = xhtml('Mục lục', f'<nav epub:type="toc" id="toc"><h1>Mục lục</h1><ol><li><a href="info.xhtml">Giới thiệu</a></li>{"".join(nav_parts)}</ol></nav>')
    files['css/book.css'] = prose_css + EPUB_CSS + re.sub(r'</?style>', '', theme_css())
    for fnt in ['BeVietnamPro-Regular.ttf', 'BeVietnamPro-Italic.ttf', 'BeVietnamPro-Bold.ttf', 'BeVietnamPro-ExtraBold.ttf', 'JetBrainsMono.ttf']:
        files[f'fonts/{fnt}'] = (ROOT / 'ebook-assets/fonts' / fnt).read_bytes()

    def mt(path):
        ext = path.rsplit('.', 1)[-1].lower()
        return {'xhtml': 'application/xhtml+xml', 'css': 'text/css', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png',
                'gif': 'image/gif', 'svg': 'image/svg+xml', 'webp': 'image/webp', 'ttf': 'font/ttf'}[ext]
    manifest, ids = [], {}
    for i, path in enumerate(sorted(files)):
        iid = 'nav' if path == 'nav.xhtml' else f'i{i}'
        ids[path] = iid
        props = []
        if path == 'nav.xhtml':
            props.append('nav')
        if path == cov_path:
            props.append('cover-image')
        manifest.append(f'<item id="{iid}" href="{path}" media-type="{mt(path)}"{(" properties=%s" % chr(34) + " ".join(props) + chr(34)) if props else ""}/>')
    spine_xml = ''.join(f'<itemref idref="{ids[f]}"/>' for f, _ in spine)
    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="vi">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{uid}</dc:identifier><dc:title>{escape(BOOK["title"])}</dc:title><dc:creator>{escape(BOOK["author"])}</dc:creator>
<dc:language>vi</dc:language><dc:publisher>{escape(BOOK["publisher"])}</dc:publisher><dc:description>{escape(BOOK["subtitle"])}</dc:description>
<meta property="dcterms:modified">{modified}</meta><meta name="cover" content="{ids[cov_path]}"/>
</metadata><manifest>{"".join(manifest)}</manifest><spine>{spine_xml}</spine></package>'''
    container = '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'
    with zipfile.ZipFile(out, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml', container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/content.opf', opf, compress_type=zipfile.ZIP_DEFLATED)
        for path, data in files.items():
            z.writestr('OEBPS/' + path, data, compress_type=zipfile.ZIP_DEFLATED)
    print(f'epub: {out.name} · {len(spine)} trang nội dung · {len(media)} hình · {out.stat().st_size/1e6:.1f} MB')


if __name__ == '__main__':
    want = set(sys.argv[1:]) or {'web', 'pdf', 'epub', 'site'}
    if (ROOT / 'prompts.json').exists() and BOOK.get('prompt_appendix'):
        from prompt_kit import appendix_md
        (ROOT / BOOK['prompt_appendix']).write_text(appendix_md(), encoding='utf-8')
    chapters = load_chapters()
    if 'web' in want:
        build_web(chapters)
    if 'pdf' in want:
        build_pdf(chapters)
    if 'epub' in want:
        build_epub(chapters)
    if 'web' in want or 'site' in want:
        if (ROOT / 'mindmap.json').exists():
            from mindmap import build as build_mindmap
            build_mindmap()
        if (ROOT / 'prompts.json').exists():
            from prompt_page import build as build_prompt_page
            build_prompt_page()
    if 'site' in want:
        from ebook_site import build_site
        build_site(BOOK)
