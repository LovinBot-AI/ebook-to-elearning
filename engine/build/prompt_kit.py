"""Nguồn duy nhất cho bộ prompt: prompts.json → prompt.html, prompt trong mindmap, và phụ lục prompt (book.prompt_appendix).

prompts.json:
{
  "flows":  {"A": ["Luồng A · Đầy đủ", "mô tả một dòng"], ...},
  "steps":  [{"id", "name", "flows": "AB", "chap": "chap-07", "intro", "prompts": [[id, tên, dùng khi, nội dung], ...]}],
  "templates": [[id, tên, dùng khi, nội dung có \\n], ...]
}
Phần trong [ ] là chỗ học viên tự điền (được tô vàng trên trang).
"""
import json

from content import BOOK, ROOT

_cfg = json.loads((ROOT / 'prompts.json').read_text(encoding='utf-8')) if (ROOT / 'prompts.json').exists() else {}
FLOWS = {k: tuple(v) for k, v in _cfg.get('flows', {}).items()}
STEPS = [dict(s, prompts=[tuple(p) for p in s['prompts']]) for s in _cfg.get('steps', [])]
TEMPLATES = [tuple(t) for t in _cfg.get('templates', [])]


def all_prompts():
    for s in STEPS:
        for p in s['prompts']:
            yield s, p


def by_id():
    out = {}
    for s, p in all_prompts():
        if p[0] in out:
            raise KeyError(f'prompts.json: trùng id prompt "{p[0]}"')
        out[p[0]] = (s, p)
    return out | {t[0]: (None, t) for t in TEMPLATES}


def lc(s: str) -> str:
    """Viết thường chữ đầu, trừ khi từ đầu viết hoa toàn bộ hoặc là tên riêng khai báo trong book.proper_nouns."""
    first = s.split()[0] if s.split() else ''
    keep = first.isupper() or first in BOOK.get('proper_nouns', [])
    return s if keep else s[:1].lower() + s[1:]


def flow_label(flows: str) -> str:
    names = [FLOWS[k][0].split(' · ')[0] if k in FLOWS else k for k in flows]
    return ', '.join(names)


def appendix_md() -> str:
    """Sinh phụ lục prompt (Markdown) từ prompts.json."""
    letter = BOOK['prompt_appendix'].split('-')[2].upper()
    out = [f'# Phụ lục {letter} — Bộ prompt sao chép theo từng bước', '',
           'Thay phần trong ngoặc vuông `[ ]` bằng nội dung của bạn. Trên bản đọc web, mỗi prompt có nút **Sao chép**. '
           'Bản tra nhanh có ô tìm kiếm và bộ lọc nằm ở **[trang Bộ prompt](prompt.html)**.', '',
           '**Sau phụ lục này, bạn làm được:** có ngay câu lệnh đúng cho mọi bước trong khoá.', '']
    if FLOWS:
        out += ['| Nhóm | Các bước |', '|---|---|']
        for k, (name, _) in FLOWS.items():
            out.append(f'| {name} | ' + ' → '.join(s['name'] for s in STEPS if k in s['flows']) + ' |')
        out.append('')
    for i, s in enumerate(STEPS, 1):
        out += [f'## {letter}.{i}. {s["name"]}', '', f'*{flow_label(s["flows"])}.* {s.get("intro", "")}', '']
        for _, title, when, text in s['prompts']:
            out += [f'**{title}** · dùng khi: {lc(when)}.', '', f'> {text}'.replace('\n', '  \n> '), '']
    if TEMPLATES:
        out += [f'## {letter}.{len(STEPS) + 1}. Mẫu điền sẵn', '']
        for _, title, when, text in TEMPLATES:
            out += [f'**{title}** · {lc(when)}.', '', '> ' + text.replace('\n', '  \n> '), '']
    return '\n'.join(out).rstrip() + '\n'
