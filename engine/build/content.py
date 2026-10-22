"""Đọc Markdown → HTML đã làm giàu (callout, prompt, checklist, hình, bảng) cho 3 đầu ra: web, print, epub."""
from __future__ import annotations

import hashlib
import re
import subprocess
from dataclasses import dataclass, field
from html import escape
from pathlib import Path

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OPT = ROOT / 'ebook-assets' / '_opt'
md = MarkdownIt('commonmark', {'html': False, 'typographer': False}).enable('table').enable('strikethrough')

CONFIG = ROOT / 'book.json'


def _load_book():
    """Đọc book.json: thông tin sách + các phần. Xem templates/book.example.json trong repo skill."""
    import json
    cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
    book = cfg['book']
    book.setdefault('org', 'Coachio Academy')
    book.setdefault('org_url', '')
    book.setdefault('publisher', book['org'])
    book.setdefault('tagline', 'Ebook khoá e-learning')
    book.setdefault('storage', re.sub(r'[^a-z0-9]+', '-', book['slug'].lower()).strip('-')[:24] + '-')
    book.setdefault('uuid_seed', book['slug'])
    book.setdefault('resources', [])
    book.setdefault('keywords', '')
    book.setdefault('info', book.get('subtitle', ''))
    book.setdefault('cover_tag', book.get('audience', ''))
    book.setdefault('hero_title_html', escape(book['title']))
    book.setdefault('cover_title_html', escape(book['title']))
    book.setdefault('help', f"Chưa có mật khẩu? Xem trong trang khoá học hoặc nhắn đội hỗ trợ của {book['org']}.")
    book['resources'] = [tuple(r) for r in book['resources']]
    parts = []
    for p in cfg['parts']:
        p = dict(p)
        lo, hi = p.get('chapters', [0, -1])
        p['chapters'] = range(lo, hi + 1)
        p.setdefault('accent', False)
        p.setdefault('teacher', book.get('teacher', ''))
        parts.append(p)
    parts.append({'id': 'part-app', 'label': 'Phụ lục', 'title': cfg.get('appendix_title', 'Tra cứu và tài nguyên'),
                  'chapters': range(0), 'accent': False, 'teacher': book.get('teacher', ''),
                  'desc': cfg.get('appendix_desc', 'Thuật ngữ, bộ prompt, giáo án, checklist và mindmap.')})
    if 'second_cta' in book:
        book['second_cta'] = tuple(book['second_cta'])
    else:
        book['second_cta'] = ('Xem phần 2', parts[1]['id'] if len(parts) > 2 else parts[0]['id'])
    return book, parts


BOOK, PARTS = _load_book()

COACHIO = {'name': 'Coachio Academy', 'coachio': True, 'ink': '#12305a', 'primary': '#1f4c86', 'accent': '#e2711d', 'accent2': '#1f7f79'}


def brand() -> dict:
    """Brand đang dùng: book.json → brand (mặc định Coachio). Khoá: ink (chữ đậm, nền tối), primary, accent (cam), accent2 (xanh phụ), logo."""
    return {**COACHIO, **(BOOK.get('brand') or {})}


def _mix(hex_color: str, t: float) -> str:
    h = hex_color.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return '#%02x%02x%02x' % tuple(round(c + (255 - c) * t) for c in (r, g, b))


def theme_css() -> str:
    """<style> ghi đè biến màu theo brand (rỗng nếu là Coachio mặc định)."""
    b = brand()
    if b.get('coachio') and not BOOK.get('brand'):
        return ''
    return ('<style>:root{' f"--navy:{b['ink']};--navy-2:{b['primary']};--navy-soft:{_mix(b['primary'], .9)};"
            f"--orange:{b['accent']};--orange-soft:{_mix(b['accent'], .9)};--teal:{b['accent2']};--teal-soft:{_mix(b['accent2'], .9)};"
            f"--prompt-bg:{b['ink']};" '}</style>')



def part_of(n: int) -> str:
    return next((p['id'] for p in PARTS if n in p['chapters']), PARTS[-2]['id'])


@dataclass
class Chapter:
    id: str
    num: str            # '01'…'16' hoặc 'A'…'C'
    kind: str           # 'chapter' | 'appendix'
    part: str
    title: str          # tiêu đề đầy đủ (h1)
    short: str          # phần sau dấu —
    label: str          # 'Chương 12' | 'Phụ lục C'
    path: Path
    raw: str
    words: int = 0
    sections: list = field(default_factory=list)   # [(id, text)]

    @property
    def minutes(self):
        return max(3, round(self.words / 200))


def load_chapters():
    out = []
    for p in sorted(ROOT.glob('chuong-[0-9][0-9]-*.md')):
        raw = p.read_text(encoding='utf-8')
        title = re.search(r'^# (.+)$', raw, re.M).group(1).strip()
        n = int(re.match(r'chuong-(\d+)', p.name).group(1))
        out.append(Chapter(f'chap-{n:02d}', f'{n:02d}', 'chapter', part_of(n),
                           title, title.split(' — ', 1)[-1], f'Chương {n}', p, raw))
    for p in sorted(ROOT.glob('phu-luc-[a-z]-*.md')):
        raw = p.read_text(encoding='utf-8')
        title = re.search(r'^# (.+)$', raw, re.M).group(1).strip()
        letter = re.match(r'phu-luc-([a-z])', p.name).group(1).upper()
        out.append(Chapter(f'phu-luc-{letter.lower()}', letter, 'appendix', 'part-app',
                           title, title.split(' — ', 1)[-1], f'Phụ lục {letter}', p, raw))
    for c in out:
        c.words = len(re.sub(r'[#>*|`\-\[\]()!]', ' ', c.raw).split())
    return out


# ---------------------------------------------------------------- media
def _key(src: str) -> str:
    return hashlib.sha1(src.encode()).hexdigest()[:10] + '-' + Path(src).stem[:40]


def media(src: str, mode: str) -> dict:
    """Trả về {'kind': img|video, 'src', 'poster'?} đã tối ưu theo đầu ra."""
    f = ROOT / src
    if not f.exists() or src.startswith('http'):
        return {'kind': 'img', 'src': src}
    ext = f.suffix.lower()
    if ext == '.svg':
        return {'kind': 'img', 'src': src}
    k = _key(src)
    (OPT / 'web').mkdir(parents=True, exist_ok=True)
    (OPT / 'print').mkdir(parents=True, exist_ok=True)
    if ext == '.gif':
        still = OPT / 'print' / f'{k}.jpg'
        if not still.exists():
            with Image.open(f) as im:
                im.seek(0)
                fr = im.convert('RGB')
                fr.thumbnail((1400, 1400))
                fr.save(still, 'JPEG', quality=82, optimize=True, progressive=True)
        if mode != 'web':
            return {'kind': 'img', 'src': _rel(still)}
        mp4 = OPT / 'web' / f'{k}.mp4'
        poster = OPT / 'web' / f'{k}-poster.webp'
        if not mp4.exists():
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(f), '-movflags', 'faststart', '-pix_fmt', 'yuv420p',
                            '-vf', 'scale=min(960\\,iw):-2:flags=lanczos,scale=trunc(iw/2)*2:trunc(ih/2)*2', '-c:v', 'libx264', '-crf', '27', '-an', str(mp4)], check=True)
        if not poster.exists():
            with Image.open(still) as im:
                im.save(poster, 'WEBP', quality=80)
        return {'kind': 'video', 'src': _rel(mp4), 'poster': _rel(poster)}
    if mode == 'web':
        out = OPT / 'web' / f'{k}.webp'
        if not out.exists() or out.stat().st_mtime < f.stat().st_mtime:
            with Image.open(f) as im:
                im = im.convert('RGBA') if im.mode in ('P', 'LA', 'RGBA') else im.convert('RGB')
                im.thumbnail((1600, 1600))
                im.save(out, 'WEBP', quality=82, method=5)
        return {'kind': 'img', 'src': _rel(out)}
    out = OPT / 'print' / f'{k}.jpg'
    if not out.exists() or out.stat().st_mtime < f.stat().st_mtime:
        with Image.open(f) as im:
            if im.mode in ('P', 'LA', 'RGBA'):
                bg = Image.new('RGB', im.size, (255, 255, 255))
                rgba = im.convert('RGBA')
                bg.paste(rgba, mask=rgba.split()[-1])
                im = bg
            else:
                im = im.convert('RGB')
            im.thumbnail((1500, 1500))
            im.save(out, 'JPEG', quality=80, optimize=True, progressive=True)
    return {'kind': 'img', 'src': _rel(out)}


def _rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


# ---------------------------------------------------------------- render
CALLOUTS = [
    ('video', re.compile(r'^(Video khớp|Video)', re.I), '🎬', 'Video bài giảng'),
    ('warn', re.compile(r'^(Cảnh báo|Quan trọng|Tuyệt đối|Lỗi hay gặp|Chưa làm|Không)', re.I), '⚠️', 'Lưu ý quan trọng'),
    ('tip', re.compile(r'^(Mẹo|Gợi ý)', re.I), '💡', 'Mẹo'),
    ('rule', re.compile(r'^(Nguyên tắc|Điều đáng nhớ|Điểm cần nhớ|Vai trò)', re.I), '🧭', 'Nguyên tắc'),
    ('note', re.compile(r'^(Lưu ý|Nhớ|Vì sao|Tại sao)', re.I), '📌', 'Ghi chú'),
]


PROMPT_RX = re.compile(r'^(Hãy|Tôi |Đây là|Đẩy |Kiểm tra|Chuẩn bị|Thêm |Game Mira|Khởi động|Soạn|Dự án này|Đã thấy|Làm |Tạo |Viết |Sửa |Dựa |Bạn là|Từ |Mở |Đọc |Giúp |Phân tích|Cho tôi|Nhân vật|Mira|Với |Prompt|Thiết kế|Chúng ta|Trong game|Mong muốn|Xây )', re.I)
PROMPT_LEAD = re.compile(r'^(Mong muốn)')
NOTE_RX = re.compile(r'^(Bạn không|Khi |Nếu |Lưu ý)')


def slug(text: str) -> str:
    t = text.lower()
    t = re.sub(r'[đĐ]', 'd', t)
    import unicodedata
    t = unicodedata.normalize('NFD', t)
    t = ''.join(ch for ch in t if unicodedata.category(ch) != 'Mn')
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return t[:60] or 'muc'


def render(ch: Chapter, mode: str) -> str:
    """mode: web | print | epub"""
    body_md = re.sub(r'^# .+\n', '', ch.raw, count=1)
    soup = BeautifulSoup(md.render(body_md), 'html.parser')

    # Hình + chú thích
    for img in list(soup.select('p > img')):
        para = img.parent
        if len([c for c in para.contents if not (isinstance(c, str) and not c.strip())]) != 1:
            continue
        fig = soup.new_tag('figure')
        img.extract()
        fig.append(img)
        nxt = para.find_next_sibling()
        if nxt and nxt.name == 'p' and nxt.find('em') and len(nxt.contents) == 1:
            cap = soup.new_tag('figcaption')
            text = re.sub(r'\s+([,.;:!?])', r'\1', nxt.get_text(' ', strip=True))
            m = re.match(r'^((?:Hình|Video)\s+[0-9A-Z]+(?:\.[0-9]+)?)\s*[—-]\s*(.*)$', text)
            if m:
                b = soup.new_tag('b'); b.string = m.group(1)
                cap.append(b); cap.append(' ' + m.group(2))
            else:
                cap.string = text
            fig.append(cap)
            nxt.decompose()
        para.replace_with(fig)

    # Liên kết tới ảnh trong đoạn văn → thêm hình bên dưới
    for a in list(soup.select('a[href]')):
        href = a.get('href', '')
        if href.startswith('http') or not re.search(r'\.(png|jpe?g|webp|gif)$', href, re.I):
            continue
        para = a.find_parent(['p', 'li'])
        if not para:
            continue
        fig = soup.new_tag('figure', attrs={'class': 'linked-figure'})
        im = soup.new_tag('img', src=href, alt=a.get_text(' ', strip=True))
        fig.append(im)
        cap = soup.new_tag('figcaption'); cap.string = a.get_text(' ', strip=True)
        fig.append(cap)
        para.insert_after(fig)
        a['href'] = media(href, mode)['src']

    # YouTube
    for a in list(soup.select('p > a[href]')):
        href = a.get('href', '')
        m = re.fullmatch(r'https?://(?:youtu\.be/|(?:www\.)?youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})(?:[&?].*)?', href)
        para = a.parent
        if not m or len(para.contents) != 1:
            continue
        label = a.get_text(' ', strip=True)
        if mode == 'web':
            html = (f'<figure class="video-figure"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/{m.group(1)}" '
                    f'title="{escape(label)}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
                    f'allowfullscreen=""></iframe></div><figcaption><b>{escape(label)}</b> · <a href="{href}" target="_blank" rel="noopener">Mở trên YouTube</a></figcaption></figure>')
        else:
            html = (f'<aside class="callout video"><p class="callout-title">🎬 {escape(label)}</p>'
                    f'<p>Xem video tại: <a href="{href}">{escape(href)}</a></p></aside>')
        para.replace_with(BeautifulSoup(html, 'html.parser'))

    # Đổi ảnh sang bản tối ưu
    for img in soup.select('img'):
        src = img.get('src', '')
        mm = media(src, mode)
        if mm['kind'] == 'video':
            v = soup.new_tag('video', attrs={'autoplay': '', 'loop': '', 'muted': '', 'playsinline': '', 'preload': 'metadata',
                                            'poster': mm['poster'], 'aria-label': img.get('alt', '')})
            s = soup.new_tag('source', src=mm['src'], type='video/mp4')
            v.append(s)
            img.replace_with(v)
            continue
        img['src'] = mm['src']
        if mm['src'].endswith('.svg') and img.parent and img.parent.name == 'figure':
            img.parent['class'] = (img.parent.get('class') or []) + ['diagram']
        if mode == 'web':
            img['loading'] = 'lazy'; img['decoding'] = 'async'
            img['tabindex'] = '0'; img['role'] = 'button'
            img['aria-label'] = 'Phóng to hình: ' + img.get('alt', 'minh họa')
        if not img.get('alt'):
            img['alt'] = 'Hình minh họa'

    # Callout & prompt
    for bq in list(soup.select('blockquote')):
        first = bq.find(['p', 'ul', 'ol'])
        strong = first.find('strong') if first and first.name == 'p' else None
        lead = strong.get_text(' ', strip=True) if strong and first.contents and first.contents[0] == strong else ''
        kind = None
        force_prompt = False
        if lead and PROMPT_LEAD.match(lead):
            lead = ''
            force_prompt = True
        for k, rx, icon, name in CALLOUTS:
            if lead and rx.search(lead):
                kind, ic = k, icon
                break
        aside = soup.new_tag('aside')
        if kind:
            aside['class'] = ['callout', kind]
            badge = soup.new_tag('span', attrs={'class': 'callout-icon', 'aria-hidden': 'true'}); badge.string = ic
            aside.append(badge)
            inner = soup.new_tag('div', attrs={'class': 'callout-body'})
            for c in list(bq.contents):
                inner.append(c.extract())
            aside.append(inner)
        elif lead:
            aside['class'] = ['callout', 'note']
            badge = soup.new_tag('span', attrs={'class': 'callout-icon', 'aria-hidden': 'true'}); badge.string = '📌'
            aside.append(badge)
            inner = soup.new_tag('div', attrs={'class': 'callout-body'})
            for c in list(bq.contents):
                inner.append(c.extract())
            aside.append(inner)
        elif not force_prompt and NOTE_RX.match(bq.get_text(' ', strip=True)):
            aside['class'] = ['callout', 'note']
            badge = soup.new_tag('span', attrs={'class': 'callout-icon', 'aria-hidden': 'true'}); badge.string = '📌'
            aside.append(badge)
            inner = soup.new_tag('div', attrs={'class': 'callout-body'})
            for c in list(bq.contents):
                inner.append(c.extract())
            aside.append(inner)
        else:
            aside['class'] = ['prompt']
            head = soup.new_tag('div', attrs={'class': 'prompt-head'})
            lab = soup.new_tag('span', attrs={'class': 'prompt-label'}); lab.string = 'PROMPT MẪU'
            head.append(lab)
            if mode == 'web':
                btn = soup.new_tag('button', attrs={'class': 'copy-btn', 'type': 'button'}); btn.string = 'Sao chép'
                head.append(btn)
            aside.append(head)
            inner = soup.new_tag('div', attrs={'class': 'prompt-body'})
            for c in list(bq.contents):
                inner.append(c.extract())
            aside.append(inner)
        bq.replace_with(aside)

    # Đoạn mục tiêu chương
    for p in soup.select('p'):
        st = p.find('strong')
        if st and p.contents and p.contents[0] == st and re.match(r'Sau (chương|phụ lục) này', st.get_text(strip=True)):
            p['class'] = ['goal']

    # Checklist "- [ ]"
    for li in soup.select('li'):
        txt = li.decode_contents()
        m = re.match(r'^\s*(?:<p>)?\s*\[( |x|X)\]\s*', txt)
        if not m:
            continue
        done = m.group(1).lower() == 'x'
        rest = txt[m.end():]
        if mode == 'web':
            box = f'<input type="checkbox" class="task-box"{" checked" if done else ""} aria-label="Đánh dấu đã làm">'
        else:
            box = f'<span class="task-box-print">{"☑" if done else "☐"}</span>'
        li.clear()
        li.append(BeautifulSoup(box + '<span class="task-text">' + rest + '</span>', 'html.parser'))
        li['class'] = ['task']
        parent = li.find_parent(['ul', 'ol'])
        if parent:
            parent['class'] = ['tasks']

    # Bảng cuộn ngang
    for t in list(soup.select('table')):
        wrap = soup.new_tag('div', attrs={'class': 'table-wrap'})
        t.wrap(wrap)

    # h2/h3: id + số mục
    ch.sections = []
    for h in soup.select('h2, h3'):
        text = h.get_text(' ', strip=True)
        hid = f'{ch.id}--{slug(text)}'
        h['id'] = hid
        m = re.match(r'^((?:\d+|[A-C])\.\d+\.?(?:\d+\.?)?)\s+(.*)$', text)
        if m:
            h.clear()
            n = soup.new_tag('span', attrs={'class': 'h-num'}); n.string = m.group(1).rstrip('.')
            h.append(n); h.append(' ' + m.group(2))
        if h.name == 'h2':
            ch.sections.append((hid, text))
        if re.match(r'^Trước khi sang|^Kết thúc|^Trước khi', text):
            h['class'] = ['h-checkpoint']

    for a in soup.select('a[href]'):
        if a['href'].startswith('http'):
            a['target'] = '_blank'; a['rel'] = 'noopener noreferrer'
    return str(soup)


def to_xhtml(html: str) -> str:
    """HTML5 fragment → XHTML hợp lệ cho EPUB."""
    soup = BeautifulSoup(html, 'html.parser')
    for t in soup.select('iframe, video, script, button, input'):
        t.decompose()
    for tag in soup.find_all(True):
        for att in ('loading', 'decoding', 'role', 'tabindex', 'target', 'rel'):
            if att in tag.attrs:
                del tag[att]
    out = str(soup)
    out = re.sub(r'<(img|br|hr|col|source|meta|link)([^>]*?)\s*/?>', r'<\1\2/>', out)
    out = out.replace('&nbsp;', '&#160;')
    return out
