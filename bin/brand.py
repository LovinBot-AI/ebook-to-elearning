"""Thương hiệu (brand) cho ebook + thumbnail.

  e2e brand-colors <logo.png>            rút 5 màu chính từ logo (gợi ý khi người dùng không biết mã màu)
  e2e brand-preview <dir>                00-ke-hoach/brand-preview.html từ 00-ke-hoach/brand-options.json (2–3 phương án)
  e2e brand-apply <dir> --option A       ghi brand vào book.json, chép logo; --coachio để dùng brand Coachio mặc định

brand-options.json:
{"name": "Tên thương hiệu", "logo": "nguon/logo.png", "kicker": "BỘ VIDEO E-LEARNING",
 "options": [{"id": "A", "label": "Giữ màu logo", "ink": "#0f2547", "primary": "#2563eb", "accent": "#f1591f", "accent2": "#0e9f6e", "note": "…"}]}
Màu: ink = chữ đậm / nền tối · primary = màu chính · accent = màu nhấn (nút, chữ nổi bật) · accent2 = màu phụ.
"""
from __future__ import annotations

import json
import shutil
from html import escape
from pathlib import Path

COACHIO = {'coachio': True, 'name': 'Coachio Academy', 'ink': '#12305a', 'primary': '#1f4c86', 'accent': '#e2711d', 'accent2': '#1f7f79'}
PREVIEW = Path(__file__).resolve().parent.parent / 'design' / 'preview' / 'index.html'
# Mẫu trên trang chọn mẫu (design/preview): S1–S4 = phong cách, A/B/C = bố cục thumbnail.
# Màu cho EBOOK (nền sáng, chữ đủ tương phản); thumbnail dùng đúng bộ màu của mẫu trong Remotion.
STYLES = {
    'S1': {'label': 'Coachio', 'coachio': True, **{k: COACHIO[k] for k in ('ink', 'primary', 'accent', 'accent2')}},
    'S2': {'label': 'Studio Đêm', 'ink': '#181c22', 'primary': '#2b3440', 'accent': '#5f8f1f', 'accent2': '#3d4a59'},
    'S3': {'label': 'Rừng Xanh', 'ink': '#17362a', 'primary': '#2f6b4f', 'accent': '#b9800f', 'accent2': '#2f6b4f'},
    'S4': {'label': 'Cobalt', 'ink': '#0b1b3f', 'primary': '#1f4bff', 'accent': '#d9431f', 'accent2': '#1f4bff'},
}
LAYOUTS = {'A': 'Ảnh màn hình', 'B': 'Mascot / giảng viên', 'C': 'Số bài lớn'}


def cmd_templates(a):
    """Mở trang chọn mẫu trên trình duyệt của người dùng (macOS: open)."""
    import subprocess
    import sys
    print(f'Trang chọn mẫu: {PREVIEW}')
    for k, v in STYLES.items():
        print(f'  {k} · {v["label"]}')
    print('  Bố cục: ' + ' · '.join(f'{k} {v}' for k, v in LAYOUTS.items()) + '   → mã mẫu dạng S3-B')
    if sys.platform == 'darwin' and not a.no_open:
        subprocess.call(['open', str(PREVIEW)])


def cmd_colors(a):
    from PIL import Image
    im = Image.open(a.logo).convert('RGBA')
    im.thumbnail((200, 200))
    px = [(r, g, b) for r, g, b, al in im.getdata() if al > 200 and not (r > 235 and g > 235 and b > 235)]
    if not px:
        raise SystemExit('Logo không có màu rõ (toàn trắng/trong suốt).')
    q = Image.new('RGB', (len(px), 1))
    q.putdata(px)
    pal = q.quantize(colors=5, method=Image.Quantize.MEDIANCUT)
    counts = sorted(pal.getcolors(), reverse=True)
    p = pal.getpalette()
    out = []
    for n, i in counts:
        r, g, b = p[i * 3:i * 3 + 3]
        lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
        out.append({'hex': '#%02x%02x%02x' % (r, g, b), 'share': round(n / len(px), 2), 'dark': lum < 90})
    for c in out:
        print(f'  {c["hex"]}  {int(c["share"] * 100):>3}%  {"tối (hợp làm ink)" if c["dark"] else ""}')


def _card(o: dict, name: str, kicker: str, logo_uri: str | None) -> str:
    logo = f'<img class="lg" src="{logo_uri}" alt="">' if logo_uri else f'<b class="lgt">{escape(name)}</b>'
    return f'''<section class="opt" style="--ink:{o['ink']};--primary:{o['primary']};--accent:{o['accent']};--accent2:{o['accent2']}">
<h2>Phương án {escape(o['id'])} · {escape(o.get('label', ''))}</h2>
<p class="note">{escape(o.get('note', ''))}</p>
<div class="sw">{''.join(f'<span style="background:{o[k]}"><i>{k}</i>{o[k]}</span>' for k in ('ink', 'primary', 'accent', 'accent2'))}</div>
<div class="row">
 <div class="thumb">{logo}<span class="kick">{escape(kicker)}</span><h3>Viết <em>PRD</em> cùng AI</h3><span class="chip">Bài 9.1</span></div>
 <div class="cover"><span class="ctag">Dành cho người mới</span><h3>Tên khoá học<span>dòng phụ</span></h3><div class="flow"><i>Bước 1</i><i>Bước 2</i><i>Bước 3</i></div></div>
 <div class="page"><div class="bar"><b>{escape(name)}</b><span class="tab">Mindmap</span><span class="tab">Bộ prompt</span></div>
  <p class="k">Chương 9</p><h4>Viết PRD và chọn MVP</h4><div class="pr"><small>PROMPT MẪU</small>Đừng viết code vội, hỏi tôi 5 câu…</div><span class="btn">Bắt đầu đọc →</span></div>
</div></section>'''


CSS = '''body{margin:0;background:#f4f3ef;font-family:"Be Vietnam Pro",system-ui,sans-serif;color:#1e2833;padding:28px}
h1{margin:0 0 6px}.lead{color:#555;margin:0 0 24px}
.opt{background:#fff;border:1px solid #e2e5e8;border-radius:18px;padding:22px;margin:0 0 24px}
.opt h2{margin:0 0 4px;color:var(--ink)}.note{margin:0 0 14px;color:#666}
.sw{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px}.sw span{color:#fff;font:600 13px monospace;padding:12px 14px;border-radius:10px;min-width:120px;text-shadow:0 1px 2px rgba(0,0,0,.4)}.sw i{display:block;font-style:normal;opacity:.8}
.row{display:grid;grid-template-columns:1.4fr .8fr 1.2fr;gap:16px;align-items:start}
.thumb{position:relative;aspect-ratio:16/9;border-radius:14px;overflow:hidden;padding:18px;box-sizing:border-box;color:#fff;background:linear-gradient(135deg,var(--ink),var(--primary))}
.thumb .lg{height:28px}.thumb .lgt{font-size:14px}.kick{display:block;margin-top:14px;font-size:11px;letter-spacing:.14em;opacity:.85}
.thumb h3{margin:6px 0 0;font-size:30px;line-height:1.05}.thumb em{font-style:normal;color:var(--accent)}
.chip{position:absolute;right:16px;bottom:14px;background:var(--accent);padding:6px 12px;border-radius:999px;font-weight:800;font-size:13px}
.cover{aspect-ratio:3/4;border-radius:14px;padding:16px;box-sizing:border-box;color:#fff;background:radial-gradient(circle at 90% 5%,color-mix(in srgb,var(--accent) 55%,transparent),transparent 55%),radial-gradient(circle at 0 100%,color-mix(in srgb,var(--accent2) 60%,transparent),transparent 60%),var(--ink)}
.ctag{font-size:10px;font-weight:800;padding:4px 8px;border-radius:99px;background:color-mix(in srgb,var(--accent2) 30%,transparent)}
.cover h3{font-size:26px;margin:14px 0}.cover h3 span{display:block;font-size:15px;color:color-mix(in srgb,var(--accent) 60%,#fff)}
.flow{display:flex;gap:4px}.flow i{flex:1;font-style:normal;font-size:10px;text-align:center;padding:5px 2px;border-radius:6px;border:1px solid color-mix(in srgb,var(--accent2) 50%,transparent)}
.page{border:1px solid #e2e5e8;border-radius:14px;overflow:hidden;font-size:13px}
.bar{display:flex;gap:6px;align-items:center;padding:10px;border-bottom:1px solid #eee}.bar b{flex:1;color:var(--ink)}
.tab{background:color-mix(in srgb,var(--primary) 12%,#fff);color:var(--primary);font-weight:800;padding:4px 8px;border-radius:7px}
.k{margin:12px 12px 0;color:var(--accent);font-weight:800}.page h4{margin:2px 12px 10px;color:var(--ink);font-size:18px}
.pr{margin:0 12px 12px;background:var(--ink);color:#e7eef7;border-radius:10px;padding:10px}.pr small{display:block;color:var(--accent);font-weight:800;margin-bottom:4px}
.btn{display:inline-block;margin:0 12px 14px;background:var(--ink);color:#fff;padding:8px 12px;border-radius:9px;font-weight:700}
@media(max-width:900px){.row{grid-template-columns:1fr}}'''


def cmd_preview(a):
    d = Path(a.dir).resolve()
    f = d / '00-ke-hoach' / 'brand-options.json'
    if not f.exists():
        raise SystemExit(f'Chưa có {f}. Claude viết file này từ câu trả lời của người dùng (xem docs/THUONG-HIEU.md).')
    cfg = json.loads(f.read_text(encoding='utf-8'))
    logo = d / cfg['logo'] if cfg.get('logo') else None
    uri = logo.as_uri() if logo and logo.exists() else None
    cards = ''.join(_card(o, cfg.get('name', ''), cfg.get('kicker', 'BỘ VIDEO E-LEARNING'), uri) for o in cfg['options'])
    fonts = (Path(__file__).resolve().parent.parent / 'engine' / 'ebook-assets' / 'app' / 'fonts.css')
    html = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Xem trước thương hiệu · {escape(cfg.get('name', ''))}</title><link rel="stylesheet" href="{fonts.as_uri()}"><style>{CSS}</style></head><body>
<h1>Xem trước thương hiệu: {escape(cfg.get('name', ''))}</h1>
<p class="lead">Mỗi phương án gồm: thumbnail bài học, bìa ebook, trang ebook. Chọn một phương án (hoặc nói chỗ muốn đổi).</p>{cards}</body></html>'''
    out = d / '00-ke-hoach' / 'brand-preview.html'
    out.write_text(html, encoding='utf-8')
    print(f'✔ {out}\n  Mở trên trình duyệt, chụp màn hình gửi người dùng chọn A/B/C. CHƯA áp dụng gì.')


def cmd_apply(a):
    d = Path(a.dir).resolve()
    bj = d / 'book.json'
    cfg = json.loads(bj.read_text(encoding='utf-8'))
    if a.template:
        code = a.template.upper()
        sid, _, lay = code.partition('-')
        if sid not in STYLES or (lay and lay not in LAYOUTS):
            raise SystemExit(f'Mã mẫu không hợp lệ: {a.template} (ví dụ S1-A, S3-B)')
        st = STYLES[sid]
        prev = cfg['book'].get('brand') or {}
        br = {'coachio': st.get('coachio', False), 'name': a.name or prev.get('name') or ('Coachio Academy' if st.get('coachio') else ''),
              **{k: st[k] for k in ('ink', 'primary', 'accent', 'accent2')}, 'template': code if lay else f'{sid}-A',
              'teacher': a.teacher or prev.get('teacher') or cfg['book'].get('teacher', ''), 'kicker': a.kicker or prev.get('kicker', '')}
        for k in ('logo', 'mascot'):
            v = getattr(a, k) or prev.get(k)
            if v and (d / v).exists():
                dst = d / 'ebook-assets' / 'brand' / (k + Path(v).suffix.lower())
                dst.parent.mkdir(parents=True, exist_ok=True)
                if (d / v).resolve() != dst.resolve():
                    shutil.copy2(d / v, dst)
                br[k] = str(dst.relative_to(d))
        cfg['book']['brand'] = br
        if br['name'] and not st.get('coachio'):
            cfg['book']['org'] = br['name']
        msg = f'mẫu {br["template"]} ({st["label"]} · {LAYOUTS[br["template"][-1]]})'
    elif a.coachio:
        cfg['book']['brand'] = dict(COACHIO)
        msg = 'brand Coachio (giữ nguyên bộ nhận diện hiện có)'
    else:
        opts = json.loads((d / '00-ke-hoach' / 'brand-options.json').read_text(encoding='utf-8'))
        o = next((x for x in opts['options'] if x['id'].upper() == a.option.upper()), None)
        if not o:
            raise SystemExit(f'Không có phương án {a.option}')
        br = {'coachio': False, 'name': opts.get('name', ''), 'kicker': opts.get('kicker', ''),
              **{k: o[k] for k in ('ink', 'primary', 'accent', 'accent2')}, 'approvedOption': o['id']}
        if opts.get('logo') and (d / opts['logo']).exists():
            dst = d / 'ebook-assets' / 'brand' / ('logo' + Path(opts['logo']).suffix.lower())
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(d / opts['logo'], dst)
            br['logo'] = str(dst.relative_to(d))
        cfg['book']['brand'] = br
        if br['name']:
            cfg['book']['org'] = br['name']
        msg = f'phương án {o["id"]} ({o.get("label", "")})'
    bj.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'✔ book.json → {msg}\n  Tiếp: e2e cover <dir> && e2e build <dir> web — thumbnail video dùng brand này khi tới bước video (handoff).')
