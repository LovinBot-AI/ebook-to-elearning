(() => {
  const root = document.documentElement;
  const KEY = document.body.dataset.storage || 'ebook-';
  const store = {
    get(k, d) { try { const v = localStorage.getItem(KEY + k); return v === null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(KEY + k, JSON.stringify(v)); } catch {} },
  };
  const ids = ['cover', ...[...document.querySelectorAll('.chapter')].map(s => s.id)];
  const titles = Object.fromEntries([...document.querySelectorAll('.chapter')].map(s => [s.id, s.dataset.title]));
  let current = 'cover';
  let read = new Set(store.get('read', []));

  /* ---------- theme & font ---------- */
  const prefs = Object.assign({ theme: 'light', fs: 18, width: 760 }, store.get('prefs', {}));
  function applyPrefs() {
    if (prefs.theme === 'light') delete root.dataset.theme; else root.dataset.theme = prefs.theme;
    root.style.setProperty('--fs', prefs.fs + 'px');
    root.style.setProperty('--measure', prefs.width + 'px');
    document.querySelectorAll('[data-theme-set]').forEach(b => b.classList.toggle('on', b.dataset.themeSet === prefs.theme));
    document.querySelectorAll('[data-fs]').forEach(b => b.classList.toggle('on', +b.dataset.fs === prefs.fs));
    document.querySelectorAll('[data-width]').forEach(b => b.classList.toggle('on', +b.dataset.width === prefs.width));
    store.set('prefs', prefs);
  }
  applyPrefs();

  /* ---------- routing ---------- */
  function show(id, opts = {}) {
    if (!ids.includes(id)) id = 'cover';
    current = id;
    document.querySelectorAll('.chapter,.cover').forEach(el => el.classList.toggle('active', el.id === id));
    document.querySelectorAll('.toc-link').forEach(el => el.classList.toggle('active', el.dataset.target === id));
    document.getElementById('topChapter').textContent = id === 'cover' ? 'Trang bìa' : titles[id];
    document.title = (id === 'cover' ? '' : titles[id] + ' · ') + document.body.dataset.book;
    if (opts.push !== false) history.replaceState(null, '', '#/' + id);
    buildRail();
    updateNav();
    closeAll();
    if (opts.scroll) {
      const t = document.getElementById(opts.scroll);
      if (t) setTimeout(() => t.scrollIntoView({ block: 'start' }), 30);
    } else if (opts.restore && store.get('pos', {})[id]) {
      setTimeout(() => scrollTo(0, store.get('pos', {})[id]), 30);
    } else {
      scrollTo(0, 0);
    }
    store.set('last', id);
    const active = document.querySelector('.toc-link.active'), toc = document.getElementById('toc');
    if (active && toc) { const top = active.offsetTop - toc.clientHeight / 2; toc.scrollTop = Math.max(0, top); }
  }
  function step(d) {
    const i = ids.indexOf(current);
    const n = ids[Math.max(0, Math.min(ids.length - 1, i + d))];
    if (n !== current) show(n);
  }
  function updateNav() {
    const i = ids.indexOf(current);
    const prev = document.getElementById('navPrev'), next = document.getElementById('navNext');
    if (prev) prev.disabled = i <= 0;
    if (next) next.disabled = i >= ids.length - 1;
    document.querySelectorAll('.toc-link').forEach(el => el.classList.toggle('read', read.has(el.dataset.target)));
    const total = ids.length - 1;
    const done = [...read].filter(x => ids.includes(x)).length;
    document.querySelectorAll('[data-read-count]').forEach(el => el.textContent = `${done}/${total}`);
    document.querySelectorAll('[data-read-bar]').forEach(el => el.style.width = (done / total * 100) + '%');
    const last = store.get('last', null);
    const cont = document.getElementById('continueBtn');
    if (cont) { cont.hidden = !last || last === 'cover'; if (last && titles[last]) cont.querySelector('span').textContent = 'Đọc tiếp: ' + titles[last].split(' — ')[0]; cont.dataset.target = last || ''; }
  }

  /* ---------- right rail + progress ---------- */
  let railLinks = [];
  function buildRail() {
    const rail = document.getElementById('rail');
    if (!rail) return;
    const sec = document.getElementById(current);
    rail.innerHTML = '';
    if (current === 'cover' || !sec) return;
    const hs = [...sec.querySelectorAll('.prose h2')];
    if (!hs.length) return;
    rail.insertAdjacentHTML('beforeend', '<b>Trong chương</b>');
    railLinks = hs.map(h => {
      const a = document.createElement('a');
      a.href = '#/' + current; a.dataset.scroll = h.id; a.textContent = h.textContent.trim();
      rail.appendChild(a); return [h, a];
    });
  }
  let ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      const max = document.documentElement.scrollHeight - innerHeight;
      const pct = max > 0 ? Math.min(1, scrollY / max) : 0;
      document.getElementById('progressBar').style.width = (current === 'cover' ? 0 : pct * 100) + '%';
      if (current !== 'cover') {
        const pos = store.get('pos', {}); pos[current] = Math.round(scrollY); store.set('pos', pos);
        if (pct > .92 && !read.has(current)) { read.add(current); store.set('read', [...read]); updateNav(); }
      }
      let on = null;
      for (const [h, a] of railLinks) { if (h.getBoundingClientRect().top < 140) on = a; }
      railLinks.forEach(([, a]) => a.classList.toggle('on', a === on));
    });
  }
  addEventListener('scroll', onScroll, { passive: true });

  /* ---------- drawers ---------- */
  function closeAll() {
    document.body.classList.remove('toc-open', 'sheet-open');
    document.querySelectorAll('.sheet').forEach(s => s.classList.remove('open'));
  }
  function toggleSheet(id) {
    const s = document.getElementById(id);
    const open = !s.classList.contains('open');
    closeAll();
    if (open) { s.classList.add('open'); document.body.classList.add('sheet-open'); }
  }

  /* ---------- toast ---------- */
  let tt;
  function toast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('show');
    clearTimeout(tt); tt = setTimeout(() => t.classList.remove('show'), 1600);
  }

  /* ---------- checklist persistence ---------- */
  const checks = store.get('checks', {});
  document.querySelectorAll('.chapter').forEach(sec => {
    sec.querySelectorAll('.task-box').forEach((box, i) => {
      const k = sec.id + ':' + i;
      box.checked = !!checks[k];
      box.addEventListener('change', () => { checks[k] = box.checked; store.set('checks', checks); });
    });
  });

  /* ---------- events ---------- */
  document.addEventListener('click', e => {
    const t = e.target;
    const sc = t.closest('[data-scroll]');
    if (sc) { e.preventDefault(); const el = document.getElementById(sc.dataset.scroll); if (el) { el.scrollIntoView({ block: 'start' }); history.replaceState(null, '', '#/' + sc.dataset.scroll); } closeAll(); return; }
    const go = t.closest('[data-target]');
    if (go && go.dataset.target) { e.preventDefault(); show(go.dataset.target, { restore: go.id === 'continueBtn' }); return; }
    if (t.closest('#menuBtn') || t.closest('#navToc')) { const open = !document.body.classList.contains('toc-open'); closeAll(); document.body.classList.toggle('toc-open', open); return; }
    if (t.closest('#navPrev') || t.closest('.pager .prev')) return step(-1);
    if (t.closest('#navNext') || t.closest('.pager .next')) return step(1);
    if (t.closest('#fontBtn') || t.closest('#navFont')) return toggleSheet('fontSheet');
    if (t.closest('#dlBtn')) return toggleSheet('dlSheet');
    if (t.closest('.scrim')) return closeAll();
    const th = t.closest('[data-theme-set]'); if (th) { prefs.theme = th.dataset.themeSet; applyPrefs(); return; }
    const fs = t.closest('[data-fs]'); if (fs) { prefs.fs = +fs.dataset.fs; applyPrefs(); return; }
    const w = t.closest('[data-width]'); if (w) { prefs.width = +w.dataset.width; applyPrefs(); return; }
    if (t.closest('#themeBtn')) { prefs.theme = prefs.theme === 'dark' ? 'light' : 'dark'; applyPrefs(); return; }
    const cp = t.closest('.copy-btn');
    if (cp) {
      const text = cp.closest('.prompt').querySelector('.prompt-body').innerText.trim();
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(() => toast('Đã sao chép prompt')).catch(() => toast('Không sao chép được, hãy bôi đen để copy'));
      return;
    }
    const img = t.closest('.prose img[role=button]');
    if (img) {
      const d = document.getElementById('zoom');
      d.querySelector('img').src = img.currentSrc || img.src;
      d.querySelector('img').alt = img.alt;
      d.querySelector('p').textContent = img.closest('figure')?.querySelector('figcaption')?.textContent || img.alt;
      d.showModal();
      return;
    }
    if (t.closest('#zoomClose') || t.id === 'zoom') document.getElementById('zoom').close();
  });
  document.addEventListener('keydown', e => {
    if (e.target.matches('input,textarea')) return;
    if (e.key === 'ArrowRight' && !e.metaKey && !e.altKey) step(1);
    if (e.key === 'ArrowLeft' && !e.metaKey && !e.altKey) step(-1);
    if (e.key === 'Escape') closeAll();
    if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('.prose img[role=button]')) { e.preventDefault(); e.target.click(); }
  });
  /* vuốt trái/phải trên điện thoại để chuyển chương */
  let sx = 0, sy = 0, st = 0;
  document.addEventListener('touchstart', e => { const p = e.touches[0]; sx = p.clientX; sy = p.clientY; st = Date.now(); }, { passive: true });
  document.addEventListener('touchend', e => {
    const p = e.changedTouches[0]; const dx = p.clientX - sx, dy = p.clientY - sy;
    if (Date.now() - st < 500 && Math.abs(dx) > 90 && Math.abs(dy) < 40 && !e.target.closest('.table-wrap,pre,.toc,dialog')) step(dx < 0 ? 1 : -1);
  }, { passive: true });
  /* ---------- link chia sẻ: #/chap-09 (chương) hoặc #/chap-09--9-2-... (đúng mục) ---------- */
  function route(h, first) {
    const id = decodeURIComponent(h.replace(/^#\/?/, ''));
    if (!id) return first && show('cover', { push: true, restore: true });
    const chap = id.includes('--') ? id.split('--')[0] : id;
    if (!ids.includes(chap)) return first && show('cover', { push: true, restore: true });
    if (id !== chap) { show(chap, { push: false, scroll: id }); history.replaceState(null, '', '#/' + id); }
    else if (chap !== current || first) show(chap, { push: !first, restore: first });
  }
  const linkOf = (id) => location.href.split('#')[0] + '#/' + id;
  function copyLink(id, what) {
    const url = linkOf(id);
    (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(() => toast('Đã sao chép link ' + what)).catch(() => prompt('Sao chép link:', url));
  }
  // nút sao chép link cho mỗi chương và mỗi mục
  document.querySelectorAll('.chapter').forEach((sec) => {
    const h = sec.querySelector('.ch-meta');
    if (h) { const b = document.createElement('button'); b.type = 'button'; b.className = 'link-btn'; b.dataset.link = sec.id; b.dataset.what = 'bài'; b.textContent = 'Sao chép link bài'; h.appendChild(b); }
    sec.querySelectorAll('.article h2[id]').forEach((h2) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'h-link'; b.dataset.link = h2.id; b.dataset.what = 'mục';
      b.setAttribute('aria-label', 'Sao chép link mục này'); b.title = 'Sao chép link mục này'; b.textContent = '#'; h2.appendChild(b);
    });
  });
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-link]');
    if (b) { e.preventDefault(); e.stopPropagation(); copyLink(b.dataset.link, b.dataset.what || ''); }
  }, true);
  addEventListener('hashchange', () => route(location.hash, false));
  // mỗi loại trang một tab cố định: mindmap / Bộ prompt mở "Xem chi tiết" sẽ dùng lại tab này
  try { window.name = KEY + 'ebook'; } catch (e) {}
  route(location.hash, true);
  addEventListener('load', () => { if (!(store.get('pos', {})[current] > 0)) scrollTo(0, 0); });
})();
