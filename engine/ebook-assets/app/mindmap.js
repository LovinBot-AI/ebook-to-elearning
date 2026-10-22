(() => {
  const data = JSON.parse(document.getElementById('mmData').textContent);
  const panel = document.getElementById('mmPanel');
  const scrim = document.getElementById('mmScrim');
  const toastEl = document.getElementById('pkToast');
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fill = s => esc(s).replace(/\[([^\]]+)\]/g, '<mark>[$1]</mark>').replace(/\n/g, '<br>');

  const set = open => document.querySelectorAll('.br').forEach(b => {
    b.classList.toggle('closed', !open);
    b.querySelector(':scope>.br-head>.tog').setAttribute('aria-expanded', String(open));
  });

  function toast(msg) {
    toastEl.textContent = msg; toastEl.classList.add('show');
    clearTimeout(toast.t); toast.t = setTimeout(() => toastEl.classList.remove('show'), 1600);
  }

  let current = null;
  function show(i, from) {
    const n = data[i];
    document.querySelectorAll('.sel').forEach(x => x.classList.remove('sel'));
    if (from) { from.classList.add('sel'); current = from; }
    document.getElementById('mmT').textContent = n.t;
    let h = n.d ? `<p class="mm-d">${esc(n.d)}</p>` : '';
    n.p.forEach((p, k) => {
      h += `<div class="pk-card"><header><h3>${esc(p.t)}</h3><button type="button" class="pk-copy" data-k="${k}">Sao chép</button></header>` +
           `<p class="pk-when"><b>Dùng khi:</b> ${esc(p.w)}</p><div class="pk-text">${fill(p.x)}</div></div>`;
    });
    if (n.c) h += `<a class="mm-read" href="index.html#/${n.c}">Đọc chương trong ebook →</a>`;
    const body = document.getElementById('mmB');
    body.innerHTML = h; body.scrollTop = 0; body._n = n;
    panel.classList.add('open'); panel.setAttribute('aria-hidden', 'false'); scrim.hidden = false;
    document.getElementById('mmX').focus({ preventScroll: true });
  }
  function hide() {
    panel.classList.remove('open'); panel.setAttribute('aria-hidden', 'true'); scrim.hidden = true;
    if (current) current.focus({ preventScroll: true });
  }

  function copy(text, btn) {
    const done = () => { btn.textContent = 'Đã chép ✓'; btn.classList.add('ok'); toast('Đã sao chép. Dán cho agent và điền chỗ [ ]'); setTimeout(() => { btn.textContent = 'Sao chép'; btn.classList.remove('ok'); }, 1800); };
    (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(done).catch(() => {
      const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { toast('Không sao chép được, hãy bôi đen để copy'); }
      ta.remove();
    });
  }

  document.addEventListener('click', e => {
    const cp = e.target.closest('.pk-copy');
    if (cp) { copy(document.getElementById('mmB')._n.p[+cp.dataset.k].x, cp); return; }
    const leaf = e.target.closest('.leaf, .info');
    if (leaf) { show(+leaf.dataset.i, leaf); return; }
    const t = e.target.closest('.tog');
    if (t) { const li = t.closest('.br'); const closed = li.classList.toggle('closed'); t.setAttribute('aria-expanded', String(!closed)); return; }
    if (e.target.closest('#mmX') || e.target === scrim) { hide(); return; }
    if (e.target.closest('#mmAll')) set(true);
    if (e.target.closest('#mmNone')) set(false);
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && panel.classList.contains('open')) hide(); });

  // Nhớ nhánh đang mở + vị trí cuộn khi sang ebook rồi quay lại (cùng tab, không mở tab mới)
  const KEY = (document.body.dataset.storage || 'ebook-') + 'mm-state';
  const brs = [...document.querySelectorAll('.br')];
  function save() {
    try { sessionStorage.setItem(KEY, JSON.stringify({ open: brs.map((b, i) => (b.classList.contains('closed') ? -1 : i)).filter(i => i >= 0), y: scrollY })); } catch (e) {}
  }
  let st = null;
  try { st = JSON.parse(sessionStorage.getItem(KEY) || 'null'); } catch (e) {}
  set(false);
  if (st) {
    st.open.forEach(i => { if (brs[i]) { brs[i].classList.remove('closed'); brs[i].querySelector(':scope>.br-head>.tog').setAttribute('aria-expanded', 'true'); } });
    requestAnimationFrame(() => scrollTo(0, st.y || 0));
  }
  addEventListener('pagehide', save);
  document.addEventListener('click', e => { if (e.target.closest('a')) save(); });
  // "← Ebook" → về đúng chương đang đọc dở
  try {
    const last = JSON.parse(localStorage.getItem((document.body.dataset.storage || 'ebook-') + 'last') || 'null');
    const a = document.querySelector('.mm-tabs a[href="index.html"]');
    if (a && last && last !== 'cover') a.href = 'index.html#/' + last;
  } catch (e) {}
})();
