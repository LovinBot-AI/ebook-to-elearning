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
    if (n.c) h += `<a class="mm-read" href="index.html#/${n.c}" target="_blank" rel="noopener">Đọc chương trong ebook ↗</a>`;
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
  set(false);
})();
