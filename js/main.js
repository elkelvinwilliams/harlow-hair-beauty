/* ─── Nav scroll effect ─────────────────────────────────────────────────── */
const nav = document.getElementById('site-nav');
if (nav) {
  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 60);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/* ─── Scroll progress bar ───────────────────────────────────────────────── */
(() => {
  const bar = document.createElement('div');
  bar.id = 'scroll-progress';
  document.body.appendChild(bar);
  const update = () => {
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  };
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update, { passive: true });
  update();
})();

/* ─── Mobile menu ───────────────────────────────────────────────────────── */
const menuBtn    = document.getElementById('menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const iconOpen   = document.getElementById('menu-icon-open');
const iconClose  = document.getElementById('menu-icon-close');

if (menuBtn && mobileMenu) {
  const close = () => {
    mobileMenu.classList.remove('open');
    iconOpen.classList.remove('hidden');
    iconClose.classList.add('hidden');
    menuBtn.setAttribute('aria-expanded', 'false');
  };

  menuBtn.addEventListener('click', () => {
    const isOpen = mobileMenu.classList.toggle('open');
    iconOpen.classList.toggle('hidden', isOpen);
    iconClose.classList.toggle('hidden', !isOpen);
    menuBtn.setAttribute('aria-expanded', String(isOpen));
  });

  mobileMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', close));

  // Close on outside click
  document.addEventListener('click', e => {
    if (!nav.contains(e.target)) close();
  });
}

/* ─── Active nav link ───────────────────────────────────────────────────── */
const page = window.location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('[data-nav-link]').forEach(link => {
  if (link.getAttribute('href') === page) {
    link.style.color = '#FAFAF8';
    link.style.opacity = '1';
  }
});

/* ─── Scroll reveal (Intersection Observer) ─────────────────────────────── */
const reveals = document.querySelectorAll('.reveal, .clip-reveal');
if (reveals.length) {
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  reveals.forEach(el => io.observe(el));
}

/* ─── Gallery filter ────────────────────────────────────────────────────── */
const filterBtns   = document.querySelectorAll('.filter-btn');
const galleryItems = document.querySelectorAll('.gallery-item[data-cat]');

if (filterBtns.length) {
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const cat = btn.dataset.filter;
      galleryItems.forEach(item => {
        const show = cat === 'all' || item.dataset.cat === cat;
        clearTimeout(item._filterTimer);
        item.style.transition = 'opacity 0.35s ease';
        item.style.pointerEvents = show ? '' : 'none';
        if (show) {
          item.style.display = '';
          requestAnimationFrame(() => { item.style.opacity = '1'; });
        } else {
          item.style.opacity = '0';
          // collapse the tile after the fade so the grid reflows cleanly
          item._filterTimer = setTimeout(() => { item.style.display = 'none'; }, 350);
        }
      });
    });
  });
}

/* ─── Animated stat counters ────────────────────────────────────────────── */
const counters = document.querySelectorAll('.stat-num[data-count]');
if (counters.length) {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const run = el => {
    const target = parseInt(el.dataset.count, 10) || 0;
    if (reduce) { el.textContent = target; return; }
    const duration = 1400;
    const start = performance.now();
    const tick = now => {
      const p = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased);
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const cio = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { run(entry.target); cio.unobserve(entry.target); }
    });
  }, { threshold: 0.6 });
  counters.forEach(c => cio.observe(c));
}

/* ─── Channel image trail (cursor-following preview) ────────────────────── */
(() => {
  const list = document.querySelector('.channel-list');
  const preview = document.getElementById('cr-preview');
  if (!list || !preview) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const thumb = preview.querySelector('.cr-thumb');
  let tx = 0, ty = 0, cx = 0, cy = 0, raf = null, active = false;
  const loop = () => {
    cx += (tx - cx) * 0.16;
    cy += (ty - cy) * 0.16;
    preview.style.left = cx + 'px';
    preview.style.top = cy + 'px';
    if (active || Math.abs(tx - cx) > 0.5 || Math.abs(ty - cy) > 0.5) {
      raf = requestAnimationFrame(loop);
    } else { raf = null; }
  };
  list.addEventListener('mousemove', e => { tx = e.clientX; ty = e.clientY; if (!raf) loop(); });
  list.querySelectorAll('.channel-row').forEach(row => {
    row.addEventListener('mouseenter', () => {
      active = true;
      thumb.className = 'cr-thumb ' + (row.dataset.preview || 'ph-hair-1');
      preview.classList.add('show');
      if (!raf) loop();
    });
    row.addEventListener('mouseleave', () => { active = false; preview.classList.remove('show'); });
  });
})();

/* ─── Floating live-chat launcher ───────────────────────────────────────── */
const chatWidget = document.getElementById('chat-widget');
if (chatWidget) {
  const toggle = document.getElementById('chat-toggle');
  const setOpen = open => {
    chatWidget.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
  };
  toggle.addEventListener('click', e => {
    e.stopPropagation();
    setOpen(!chatWidget.classList.contains('open'));
  });
  document.addEventListener('click', e => {
    if (!chatWidget.contains(e.target)) setOpen(false);
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });
}

/* ─── Contact form (demo) ───────────────────────────────────────────────── */
const form = document.getElementById('contact-form');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const btn = form.querySelector('[type="submit"]');
    const orig = btn.textContent;
    btn.textContent = 'Message Sent ✓';
    btn.style.background = '#4A7A5A';
    btn.style.borderColor = '#4A7A5A';
    btn.disabled = true;
    setTimeout(() => {
      btn.textContent = orig;
      btn.style.background = '';
      btn.style.borderColor = '';
      btn.disabled = false;
      form.reset();
    }, 3500);
  });
}
