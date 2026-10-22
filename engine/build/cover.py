"""Sinh ebook-assets/cover.png từ build/cover/cover.html + mục "cover" trong book.json.

book.json → "cover": {"title": "VIBE CODE", "title2": "phần mềm cho người mới", "tag": "...", "sub": "...",
  "q": "câu học viên hỏi", "a": "câu AI/giảng viên trả lời", "a_who": "Agent", "flow": ["Bước 1", ...], "pills": ["Công cụ", ...]}
Chạy: python3 build/cover.py   (cần Playwright + Chrome)
"""
import datetime as dt
from html import escape
from pathlib import Path

from content import BOOK, ROOT, brand

TPL = Path(__file__).parent / 'cover' / 'cover.html'


def build():
    c = BOOK.get('cover', {})
    br = brand()
    title = c.get('title', BOOK['title'])
    h1 = 186 if len(title) <= 10 else 150 if len(title) <= 14 else 120 if len(title) <= 24 else 96
    html = (TPL.read_text(encoding='utf-8')
            .replace('{{H1_SIZE}}', str(h1))
            .replace('{{INK}}', br['ink']).replace('{{ACCENT}}', br['accent']).replace('{{ACCENT2}}', br['accent2'])
            .replace('{{LOGO}}', f'<img src="{(ROOT / br["logo"]).as_uri()}" alt="">' if br.get('logo') and (ROOT / br['logo']).exists() else escape(BOOK['org'])).replace('{{TAGLINE}}', escape(BOOK['tagline']))
            .replace('{{TAG}}', escape(c.get('tag', BOOK.get('cover_tag', ''))))
            .replace('{{TITLE}}', escape(title)).replace('{{TITLE2}}', escape(c.get('title2', '')))
            .replace('{{SUB}}', escape(c.get('sub', BOOK['subtitle'])))
            .replace('{{Q}}', escape(c.get('q', ''))).replace('{{A_WHO}}', escape(c.get('a_who', 'AI')))
            .replace('{{A}}', escape(c.get('a', '')))
            .replace('{{FLOW}}', ''.join(f'<div>{escape(x)}</div>' for x in c.get('flow', [])))
            .replace('{{PILLS}}', ''.join(f'<div>{escape(x)}</div>' for x in c.get('pills', [])))
            .replace('{{AUTHOR}}', escape(BOOK['author'])).replace('{{YEAR}}', str(dt.date.today().year)))
    tmp = TPL.parent / '_cover.html'
    tmp.write_text(html, encoding='utf-8')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel='chrome')
        pg = b.new_page(viewport={'width': 1200, 'height': 1600})
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(600)
        out = ROOT / 'ebook-assets' / 'cover.png'
        pg.screenshot(path=str(out))
        b.close()
    tmp.unlink()
    print('cover:', out.relative_to(ROOT))


if __name__ == '__main__':
    build()
