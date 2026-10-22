"""Dựng thư mục site/ để xuất bản GitHub Pages, có form mật khẩu.

Nội dung ebook (HTML) và file tải về (PDF, EPUB) được MÃ HOÁ AES-GCM bằng khoá sinh từ mật khẩu
(PBKDF2-SHA256). Trên site chỉ có bản mã hoá: không có mật khẩu thì không đọc được chữ của sách.
Ảnh minh hoạ vẫn là file công khai (không chứa nội dung chữ của sách).

Mật khẩu lấy từ biến môi trường EBOOK_PASSWORD hoặc file .ebook-password (không đưa lên git).
"""
from __future__ import annotations

import base64
import json
import os
import re
import secrets
import shutil
from html import escape
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
ITER = 310_000


def password() -> str:
    pw = os.environ.get('EBOOK_PASSWORD') or ''
    f = ROOT / '.ebook-password'
    if not pw and f.exists():
        pw = f.read_text(encoding='utf-8').strip()
    if not pw:
        raise SystemExit('Thiếu mật khẩu: đặt EBOOK_PASSWORD hoặc tạo file .ebook-password')
    return pw


def derive(pw: str, salt: bytes) -> bytes:
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(pw.encode('utf-8'))


def enc(key: bytes, data: bytes) -> bytes:
    iv = secrets.token_bytes(12)
    return iv + AESGCM(key).encrypt(iv, data, None)


def build_public(book: dict):
    """Bản công khai (ví dụ bản free cho workshop): chép nguyên trang, không mật khẩu."""
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / '.nojekyll').write_text('')
    refs = set()
    for name in ['index.html', 'mindmap.html', 'prompt.html']:
        f = ROOT / name
        if f.exists():
            html = f.read_text(encoding='utf-8')
            (SITE / name).write_text(html, encoding='utf-8')
            refs |= set(re.findall(r'(?:src|href|poster)="(ebook-assets/[^"#?]+)"', html))
    shutil.copy2(SITE / 'index.html', SITE / '404.html')
    for r in refs:
        f = ROOT / r
        if f.is_file():
            (SITE / r).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, SITE / r)
    for d in ['ebook-assets/app', 'ebook-assets/fonts']:
        shutil.copytree(ROOT / d, SITE / d, dirs_exist_ok=True)
    if (ROOT / 'downloads').exists():
        shutil.copytree(ROOT / 'downloads', SITE / 'downloads', dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('_*'))
    size = sum(p.stat().st_size for p in SITE.rglob('*') if p.is_file())
    print(f'site: {len(list(SITE.rglob("*")))} file · {size/1e6:.1f} MB · bản CÔNG KHAI, không mật khẩu')


def build_site(book: dict):
    if book.get('public'):
        return build_public(book)
    pw = password()
    salt = secrets.token_bytes(16)
    key = derive(pw, salt)
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / '.nojekyll').write_text('')

    gate = (ROOT / 'build' / 'gate.html').read_text(encoding='utf-8')
    check = base64.b64encode(enc(key, b'ebook-ok')).decode()

    def gated(src: str, script: str) -> tuple[str, set]:
        html = (ROOT / src).read_text(encoding='utf-8')
        head = re.search(r'<head>(.*?)</head>', html, re.S).group(1)
        body = re.search(r'<body[^>]*>(.*)</body>', html, re.S).group(1)
        body = re.sub(r'<script src="[^"]*(?:reader|mindmap|prompt-kit)\.js"[^>]*></script>', '', body)
        refs = set(re.findall(r'(?:src|href|poster)="(ebook-assets/[^"#?]+)"', html))
        payload = {'v': 1, 'iter': ITER, 'salt': base64.b64encode(salt).decode(),
                   'data': base64.b64encode(enc(key, body.encode('utf-8'))).decode(), 'check': check}
        head_clean = re.sub(r'<script>.*?</script>', '', head, flags=re.S)
        page = (gate.replace('__HEAD__', head_clean)
                    .replace('__TITLE__', escape(book['title']))
                    .replace('__SUB__', escape(book['subtitle']))
                    .replace('__BRAND__', escape(book['brand_mark']))
                    .replace('__HELP__', escape(book['help']))
                    .replace('__STORE__', book['storage'])
                    .replace('ebook-assets/app/reader.js', script)
                    .replace('__PAYLOAD__', json.dumps(payload)))
        return page, refs

    page, refs = gated('index.html', 'ebook-assets/app/reader.js')
    pages = {'index.html': page, '404.html': page}
    for extra, script in [('mindmap.html', 'mindmap.js'), ('prompt.html', 'prompt-kit.js')]:
        if (ROOT / extra).exists():
            pg, pg_refs = gated(extra, 'ebook-assets/app/' + script)
            pages[extra] = pg
            refs |= pg_refs

    # tài nguyên cần chép: mọi src/href/poster trỏ vào ebook-assets/ + app + fonts
    for r in refs:
        f = ROOT / r
        if f.is_file():
            (SITE / r).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, SITE / r)
    for d in ['ebook-assets/app', 'ebook-assets/fonts']:
        shutil.copytree(ROOT / d, SITE / d, dirs_exist_ok=True)

    # file tải về: mã hoá
    (SITE / 'downloads').mkdir()
    for f in (ROOT / 'downloads').glob('*'):
        if f.suffix.lower() in ('.pdf', '.epub'):
            (SITE / 'downloads' / (f.name + '.enc')).write_bytes(enc(key, f.read_bytes()))

    for name, html in pages.items():
        (SITE / name).write_text(html, encoding='utf-8')
    (SITE / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
    size = sum(p.stat().st_size for p in SITE.rglob('*') if p.is_file())
    print(f'site: {len(list(SITE.rglob("*")))} file · {size/1e6:.1f} MB · nội dung + PDF/EPUB đã mã hoá')
