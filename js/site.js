/* Hagiazo Hair — shared behaviour. Vanilla JS, no dependencies.
   Motion is transform/opacity only, driven by rAF / IntersectionObserver,
   and switched off when the visitor prefers reduced motion. */
(() => {
  'use strict';

  /* ─── Site settings ───────────────────────────────────────────────────── */
  // The external booking system. Leave empty until the link exists: every
  // "Book" button then goes to booking.html, which explains how to book today.
  const BOOKING_URL = '';
  const WHATSAPP    = 'https://wa.me/447000000000'; // placeholder — replace with the studio number

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  /* ─── Booking links ───────────────────────────────────────────────────── */
  $$('[data-book]').forEach(a => {
    if (BOOKING_URL) {
      a.href = BOOKING_URL + (a.dataset.book ? (BOOKING_URL.includes('?') ? '&' : '?') + 'service=' + encodeURIComponent(a.dataset.book) : '');
      a.target = '_blank'; a.rel = 'noopener noreferrer';
    } else if (a.dataset.book) {
      a.href = 'booking.html?service=' + encodeURIComponent(a.dataset.book);
    }
  });
  $$('[data-whatsapp]').forEach(a => { a.href = WHATSAPP + (a.dataset.whatsapp ? '?text=' + encodeURIComponent(a.dataset.whatsapp) : ''); });

  /* ─── Scroll pipeline (one passive listener + rAF) ────────────────────── */
  const header = $('#site-header');
  const bar = document.createElement('div');
  bar.id = 'scroll-progress'; bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  const parallax = $$('[data-parallax]');
  let ticking = false;
  const onFrame = () => {
    ticking = false;
    const doc = document.documentElement;
    const y = window.scrollY || doc.scrollTop;
    if (header) header.classList.toggle('scrolled', y > 20);
    const max = doc.scrollHeight - doc.clientHeight;
    bar.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';
    if (!reducedMotion.matches && y < window.innerHeight) {
      for (const el of parallax) {
        const f = parseFloat(el.dataset.parallax) || 0;
        el.style.transform = 'translate3d(0,' + (y * f).toFixed(1) + 'px,0)';
      }
    }
  };
  const tick = () => { if (!ticking) { ticking = true; requestAnimationFrame(onFrame); } };
  window.addEventListener('scroll', tick, { passive: true });
  window.addEventListener('resize', tick, { passive: true });
  onFrame();

  /* ─── Mobile nav ──────────────────────────────────────────────────────── */
  const menuBtn = $('#menu-btn'), mobileNav = $('#mobile-nav');
  if (menuBtn && mobileNav) {
    const set = open => {
      mobileNav.classList.toggle('open', open);
      header && header.classList.toggle('menu-open', open);
      menuBtn.setAttribute('aria-expanded', String(open));
      menuBtn.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
      document.body.style.overflow = open ? 'hidden' : '';
    };
    menuBtn.addEventListener('click', () => set(!mobileNav.classList.contains('open')));
    $$('a', mobileNav).forEach(a => a.addEventListener('click', () => set(false)));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && mobileNav.classList.contains('open')) { set(false); menuBtn.focus(); } });
  }

  /* ─── Active nav link ─────────────────────────────────────────────────── */
  const page = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  $$('[data-nav]').forEach(a => { if ((a.getAttribute('href') || '').toLowerCase() === page) a.setAttribute('aria-current', 'page'); });

  /* ─── Reveal on scroll ────────────────────────────────────────────────── */
  const reveals = $$('.reveal');
  if (reveals.length) {
    const showAll = () => reveals.forEach(el => el.classList.add('visible'));
    if (reducedMotion.matches || !('IntersectionObserver' in window)) showAll();
    else {
      const io = new IntersectionObserver(entries => {
        for (const en of entries) if (en.isIntersecting) { en.target.classList.add('visible'); io.unobserve(en.target); }
      }, { threshold: 0.08, rootMargin: '0px 0px -32px 0px' });
      reveals.forEach(el => io.observe(el));
      reducedMotion.addEventListener('change', e => { if (e.matches) { showAll(); io.disconnect(); } });
    }
  }

  /* ─── Count-up stats ──────────────────────────────────────────────────── */
  const counters = $$('.stat-num[data-count]');
  if (counters.length) {
    const run = el => {
      const target = parseFloat(el.dataset.count) || 0;
      const dec = (el.dataset.count.split('.')[1] || '').length;
      if (reducedMotion.matches) { el.textContent = target.toFixed(dec); return; }
      const start = performance.now(), dur = 1400;
      const step = now => {
        const p = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - p, 3);
        el.textContent = (target * e).toFixed(dec);
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    if ('IntersectionObserver' in window) {
      const cio = new IntersectionObserver(en => { for (const e of en) if (e.isIntersecting) { run(e.target); cio.unobserve(e.target); } }, { threshold: 0.5 });
      counters.forEach(c => cio.observe(c));
    } else counters.forEach(run);
  }

  /* ─── Marquee: duplicate the row once so the loop is seamless ─────────── */
  $$('.marquee .track').forEach(t => { t.innerHTML += t.innerHTML; });

  /* ─── Gallery filter + lightbox ───────────────────────────────────────── */
  const filters = $$('.filters button'), tiles = $$('.tile[data-cat]');
  if (filters.length && tiles.length) {
    filters.forEach(b => {
      const cat = b.dataset.filter;
      const n = cat === 'all' ? tiles.length : tiles.filter(t => t.dataset.cat === cat).length;
      const sup = document.createElement('sup'); sup.textContent = n; b.appendChild(sup);
      b.addEventListener('click', () => {
        filters.forEach(x => x.classList.remove('active')); b.classList.add('active');
        tiles.forEach(t => {
          const show = cat === 'all' || t.dataset.cat === cat;
          t.classList.toggle('hidden', !show);
          t.classList.remove('fade-in'); void t.offsetWidth; if (show) t.classList.add('fade-in');
        });
      });
    });
  }
  const lb = $('#lightbox');
  if (lb && tiles.length) {
    const frame = $('.frame', lb), cat = $('[data-lb-cat]', lb), title = $('[data-lb-title]', lb), desc = $('[data-lb-desc]', lb), book = $('[data-lb-book]', lb);
    let last = null;
    const open = t => {
      last = t;
      frame.innerHTML = ''; const ph = $('.media', t).cloneNode(true); ph.className = 'ph-clone'; ph.style.cssText = 'position:absolute;inset:0;'; $$('.media-cap, .slot-tag', ph).forEach(x => x.remove()); frame.appendChild(ph);
      cat.textContent = t.dataset.catLabel || ''; title.textContent = t.dataset.title || ''; desc.textContent = t.dataset.desc || '';
      if (book) book.href = BOOKING_URL || ('booking.html?service=' + encodeURIComponent(t.dataset.service || ''));
      lb.classList.add('open'); requestAnimationFrame(() => lb.classList.add('show'));
      document.body.style.overflow = 'hidden'; $('.close', lb).focus();
    };
    const close = () => { lb.classList.remove('show'); setTimeout(() => { lb.classList.remove('open'); document.body.style.overflow = ''; last && last.focus(); }, 200); };
    tiles.forEach(t => t.addEventListener('click', () => open(t)));
    $('.close', lb).addEventListener('click', close);
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && lb.classList.contains('open')) close(); });
  }

  /* ─── Testimonial carousel ────────────────────────────────────────────── */
  const car = $('.carousel[data-carousel]');
  if (car) {
    const items = JSON.parse(car.dataset.carousel), q = $('.big-q', car), who = $('.foot b', car), sub = $('.foot span', car), count = $('.count', car);
    let i = 0;
    const render = () => { q.textContent = items[i].q; who.textContent = items[i].n; sub.textContent = items[i].s; count.textContent = (i + 1) + ' / ' + items.length; };
    const go = d => { i = (i + d + items.length) % items.length; if (reducedMotion.matches) return render(); q.classList.add('swap'); setTimeout(() => { render(); q.classList.remove('swap'); }, 250); };
    $('[data-prev]', car).addEventListener('click', () => go(-1));
    $('[data-next]', car).addEventListener('click', () => go(1));
    render();
  }

  /* ─── Accordion (one open at a time) ──────────────────────────────────── */
  const acc = $$('.acc-item');
  acc.forEach(item => {
    const btn = $('.acc-btn', item);
    btn.addEventListener('click', () => {
      const open = item.classList.contains('open');
      acc.forEach(x => { x.classList.remove('open'); $('.acc-btn', x).setAttribute('aria-expanded', 'false'); });
      if (!open) { item.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
    });
  });

  /* ─── Booking page: choose a style, see the estimate, then book ───────── */
  const bk = $('#booking-app');
  if (bk) {
    const SERVICES = JSON.parse($('#booking-data').textContent);
    const opts = $('[data-options]', bk), lenWrap = $('[data-lengths]', bk), sizeWrap = $('[data-sizes]', bk);
    const sStyle = $('[data-s-style]', bk), sLen = $('[data-s-len]', bk), sSize = $('[data-s-size]', bk), sTotal = $('[data-s-total]', bk), sNote = $('[data-s-note]', bk);
    const goBtn = $('[data-go]', bk), waBtn = $('[data-wa]', bk);
    let sel = { s: null, l: null, z: null };
    const money = v => v == null ? '—' : '£' + v;
    const chips = (wrap, list, key, labelFn) => {
      wrap.innerHTML = '';
      list.forEach(it => {
        const b = document.createElement('button'); b.type = 'button'; b.className = 'chip' + (sel[key] === it.id ? ' selected' : '');
        b.innerHTML = labelFn(it); b.addEventListener('click', () => { sel[key] = it.id; if (key === 'l') sel.z = null; update(); });
        wrap.appendChild(b);
      });
    };
    const update = () => {
      const s = SERVICES.find(x => x.id === sel.s);
      $$('.opt', opts).forEach(o => o.classList.toggle('selected', o.dataset.id === sel.s));
      lenWrap.parentElement.hidden = !s; sizeWrap.parentElement.hidden = !s;
      let price = null, len = null, size = null;
      if (s) {
        chips(lenWrap, s.lengths, 'l', it => it.name);
        len = s.lengths.find(x => x.id === sel.l);
        const sizes = len ? len.sizes : [];
        chips(sizeWrap, sizes, 'z', it => it.name + '<small>' + money(it.price) + '</small>');
        sizeWrap.parentElement.hidden = !len;
        size = sizes.find(x => x.id === sel.z);
        if (size) price = size.price;
      }
      sStyle.textContent = s ? s.name : '—'; sLen.textContent = len ? len.name : '—'; sSize.textContent = size ? size.name : '—';
      sTotal.textContent = money(price); sNote.textContent = s ? s.note : 'Choose a style to see the price.';
      const ready = !!size;
      goBtn.classList.toggle('disabled', !ready); goBtn.setAttribute('aria-disabled', String(!ready));
      const text = ready ? `Hi Ruvimbo — I'd like to book ${s.name} · ${len.name} · ${size.name} (${money(price)}). When do you have availability?` : "Hi Ruvimbo — I'd like to book an appointment.";
      waBtn.href = WHATSAPP + '?text=' + encodeURIComponent(text);
      if (BOOKING_URL) { goBtn.href = BOOKING_URL + (s ? (BOOKING_URL.includes('?') ? '&' : '?') + 'service=' + encodeURIComponent(s.id) : ''); goBtn.target = '_blank'; }
      else goBtn.href = '#how-to-book';
    };
    SERVICES.forEach((s, n) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'opt'; b.dataset.id = s.id;
      b.innerHTML = `<div class="top"><span class="i">${String(n + 1).padStart(2, '0')}</span><span class="from">from ${money(s.from)}</span></div><h3>${s.name}</h3><p>${s.desc}</p>`;
      b.addEventListener('click', () => { sel = { s: s.id, l: null, z: null }; update(); });
      opts.appendChild(b);
    });
    const pre = new URLSearchParams(location.search).get('service');
    if (pre && SERVICES.some(s => s.id === pre)) sel.s = pre;
    update();
  }

  /* ─── Contact form (client-side only until a backend is chosen) ───────── */
  const form = $('#contact-form');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      let ok = true;
      $$('[required]', form).forEach(f => {
        const msg = f.parentElement.querySelector('.msg');
        const bad = !f.value.trim() || (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        if (msg) msg.textContent = bad ? 'Please complete this field.' : '';
        if (bad) ok = false;
      });
      if (!ok) return;
      const btn = $('[type="submit"]', form), orig = btn.innerHTML;
      btn.innerHTML = 'Message received ✓'; btn.setAttribute('disabled', '');
      setTimeout(() => { btn.innerHTML = orig; btn.removeAttribute('disabled'); form.reset(); }, 3500);
    });
  }

  /* ─── Chat launcher ───────────────────────────────────────────────────── */
  const chat = $('#chat-widget'), chatBtn = $('#chat-toggle');
  if (chat && chatBtn) {
    const set = o => { chat.classList.toggle('open', o); chatBtn.setAttribute('aria-expanded', String(o)); };
    chatBtn.addEventListener('click', e => { e.stopPropagation(); set(!chat.classList.contains('open')); });
    document.addEventListener('click', e => { if (!chat.contains(e.target)) set(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
  }

  /* ─── Back to top ─────────────────────────────────────────────────────── */
  const top = $('#to-top');
  if (top) top.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reducedMotion.matches ? 'auto' : 'smooth' }));
})();
