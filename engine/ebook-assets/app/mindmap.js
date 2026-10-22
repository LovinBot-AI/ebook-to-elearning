(() => {
  const raw = JSON.parse(document.getElementById('mmData').textContent);
  const data = raw.nodes || raw;
  const content = raw.content || {};
  const KEY = document.body.dataset.storage || 'ebook-';
  const panel = document.getElementById('mmPanel');
  const scrim = document.getElementById('mmScrim');
  const toastEl = document.getElementById('pkToast');
  const openBtn = document.getElementById('mmOpen');
  const foot = document.getElementById('mmF');
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fill = s => esc(s).replace(/\[([^\]]+)\]/g, '<mark>[$1]</mark>').replace(/\n/g, '<br>');
  const ebookUrl = id => new URL('index.html#/' + id, location.href).href;
  // mỗi loại trang một tab cố định → "Xem chi tiết" luôn mở lại đúng 1 tab ebook, không sinh thêm tab
  try { window.name = KEY + 'mindmap'; } catch (e) {}

  const set = open => document.querySelectorAll('.br').forEach(b => {
    b.classList.toggle('closed', !open);
    b.querySelector(':scope>.br-head>.tog').setAttribute('aria-expanded', String(open));
  });

  function toast(msg) {
    toastEl.textContent = msg; toastEl.classList.add('show');
    clearTimeout(toast.t); toast.t = setTimeout(() => toastEl.classList.remove('show'), 1700);
  }
  function copy(text, ok) {
    (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(() => toast(ok)).catch(() => {
      const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); toast(ok); } catch (e) { toast('Không sao chép được, hãy bôi đen để copy'); }
      ta.remove();
    });
  }

  let current = null, node = null;
  function show(i, from) {
    const n = data[i];
    node = n;
    document.querySelectorAll('.sel').forEach(x => x.classList.remove('sel'));
    if (from) { from.classList.add('sel'); current = from; }
    document.getElementById('mmT').textContent = n.t;
    const body = content[n.k] || '';
    let h = n.d ? `<p class="mm-d">${esc(n.d)}</p>` : '';
    if (body) h += `<div class="prose mm-prose">${body}</div>`;
    // prompt gắn với ý này (bỏ qua prompt đã có sẵn trong nội dung chương)
    const plainBody = body.replace(/<[^>]+>/g, ' ');
    const extra = n.p.filter(p => !plainBody.includes(p.x.slice(0, 40)));
    if (extra.length) {
      h += `<h4 class="mm-sub">Prompt cho bước này</h4>`;
      extra.forEach(p => {
        h += `<div class="pk-card"><header><h3>${esc(p.t)}</h3><button type="button" class="pk-copy" data-x="${esc(p.x)}">Sao chép</button></header>` +
             `<p class="pk-when"><b>Dùng khi:</b> ${esc(p.w)}</p><div class="pk-text">${fill(p.x)}</div></div>`;
      });
    }
    if (!h) h = '<p class="mm-d">Mở chương trong ebook để đọc chi tiết.</p>';
    const b = document.getElementById('mmB');
    b.innerHTML = h; b.scrollTop = 0;
    b.querySelectorAll('.prose a[href^="#/"]').forEach(a => { a.href = 'index.html' + a.getAttribute('href'); a.target = KEY + 'ebook'; });
    if (n.u) { openBtn.href = 'index.html#/' + n.u; foot.hidden = false; } else foot.hidden = true;
    panel.classList.add('open'); panel.setAttribute('aria-hidden', 'false'); scrim.hidden = false;
    document.body.classList.add('panel-open');
    if (matchMedia('(max-width:999px)').matches) document.getElementById('mmX').focus({ preventScroll: true });
    if (from && matchMedia('(min-width:1000px)').matches) from.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }
  function hide() {
    panel.classList.remove('open'); panel.setAttribute('aria-hidden', 'true'); scrim.hidden = true;
    document.body.classList.remove('panel-open');
    if (current) current.focus({ preventScroll: true });
  }

  document.addEventListener('click', e => {
    const pc = e.target.closest('.pk-copy');
    if (pc) { copy(pc.dataset.x, 'Đã sao chép prompt'); pc.textContent = 'Đã chép ✓'; setTimeout(() => (pc.textContent = 'Sao chép'), 1600); return; }
    const cb = e.target.closest('.copy-btn');
    if (cb) { copy(cb.closest('.prompt').querySelector('.prompt-body').innerText.trim(), 'Đã sao chép prompt'); return; }
    if (e.target.closest('#mmCopy')) { if (node && node.u) copy(ebookUrl(node.u), 'Đã sao chép link bài trong ebook'); return; }
    const leaf = e.target.closest('.leaf, .info');
    if (leaf) { show(+leaf.dataset.i, leaf); return; }
    const t = e.target.closest('.tog');
    if (t) {
      const li = t.closest('.br'); const closed = li.classList.toggle('closed'); t.setAttribute('aria-expanded', String(!closed));
      // bảng đọc đang mở → bấm nhánh khác có nội dung thì đổi luôn nội dung bảng
      const info = li.querySelector(':scope>.br-head>.info');
      if (!closed && info && data[+info.dataset.i].k && panel.classList.contains('open')) show(+info.dataset.i, info);
      return;
    }
    if (e.target.closest('#mmX') || e.target === scrim) { hide(); return; }
    if (e.target.closest('#mmAll')) set(true);
    if (e.target.closest('#mmNone')) set(false);
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && panel.classList.contains('open')) hide(); });

  // nhớ nhánh đang mở + vị trí cuộn
  const SKEY = KEY + 'mm-state';
  const brs = [...document.querySelectorAll('.br')];
  function save() {
    try { sessionStorage.setItem(SKEY, JSON.stringify({ open: brs.map((b, i) => (b.classList.contains('closed') ? -1 : i)).filter(i => i >= 0), y: scrollY })); } catch (e) {}
  }
  let st = null;
  try { st = JSON.parse(sessionStorage.getItem(SKEY) || 'null'); } catch (e) {}
  set(false);
  if (st) {
    st.open.forEach(i => { if (brs[i]) { brs[i].classList.remove('closed'); brs[i].querySelector(':scope>.br-head>.tog').setAttribute('aria-expanded', 'true'); } });
    requestAnimationFrame(() => scrollTo(0, st.y || 0));
  }
  addEventListener('pagehide', save);
  document.addEventListener('click', e => { if (e.target.closest('a')) save(); });

  // "← Ebook" → về đúng chương đang đọc dở
  try {
    const last = JSON.parse(localStorage.getItem(KEY + 'last') || 'null');
    const a = document.querySelector('.mm-tabs a[href="index.html"]');
    if (a && last && last !== 'cover') a.href = 'index.html#/' + last;
  } catch (e) {}
})();
