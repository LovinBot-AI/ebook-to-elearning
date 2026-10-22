(() => {
  const KEY = (document.body.dataset.storage || 'ebook-') + 'pk-flow';
  const q = document.getElementById('pkQ');
  const count = document.getElementById('pkCount');
  const empty = document.getElementById('pkEmpty');
  const toastEl = document.getElementById('pkToast');
  let flow = 'all';
  try { flow = localStorage.getItem(KEY) || 'all'; } catch (e) {}
  if (!document.querySelector(`.pk-chip[data-f="${flow}"]`)) flow = 'all';

  const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd');

  function apply() {
    const words = norm(q.value.trim()).split(/\s+/).filter(Boolean);
    let shown = 0;
    document.querySelectorAll('.pk-sec').forEach(sec => {
      const inFlow = flow === 'all' || sec.dataset.flows.includes(flow);
      let any = false;
      sec.querySelectorAll('.pk-card').forEach(c => {
        const hay = c._q || (c._q = norm(c.dataset.q));
        const ok = inFlow && words.every(w => hay.includes(w));
        c.hidden = !ok; if (ok) { any = true; shown++; }
      });
      sec.hidden = !any;
    });
    document.querySelectorAll('.pk-chip').forEach(b => b.classList.toggle('on', b.dataset.f === flow));
    document.querySelectorAll('.pk-rail').forEach(r => { r.hidden = r.dataset.f !== flow; });
    count.textContent = `Đang hiện ${shown} prompt`;
    empty.hidden = shown > 0;
  }

  function toast(msg) {
    toastEl.textContent = msg; toastEl.classList.add('show');
    clearTimeout(toast.t); toast.t = setTimeout(() => toastEl.classList.remove('show'), 1600);
  }

  document.addEventListener('click', e => {
    const chip = e.target.closest('.pk-chip');
    if (chip) { flow = chip.dataset.f; try { localStorage.setItem(KEY, flow); } catch (err) {} apply(); return; }
    const btn = e.target.closest('.pk-copy');
    if (btn) {
      const text = btn.closest('.pk-card').querySelector('textarea').value;
      const done = () => { btn.textContent = 'Đã chép ✓'; btn.classList.add('ok'); toast('Đã sao chép. Dán cho agent và điền chỗ [ ]'); setTimeout(() => { btn.textContent = 'Sao chép'; btn.classList.remove('ok'); }, 1800); };
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(done).catch(() => {
        const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); done(); } catch (err) { toast('Không sao chép được, hãy bôi đen để copy'); }
        ta.remove();
      });
    }
  });
  q.addEventListener('input', apply);
  apply();
  const PK = KEY + '-y';
  try { const y = +sessionStorage.getItem(PK); if (y) requestAnimationFrame(() => scrollTo(0, y)); } catch (e) {}
  addEventListener('pagehide', () => { try { sessionStorage.setItem(PK, String(scrollY)); } catch (e) {} });
  // "← Ebook" → về đúng chương đang đọc dở
  try {
    const last = JSON.parse(localStorage.getItem((document.body.dataset.storage || 'ebook-') + 'last') || 'null');
    const a = document.querySelector('.mm-tabs a[href="index.html"]');
    if (a && last && last !== 'cover') a.href = 'index.html#/' + last;
  } catch (e) {}
})();
