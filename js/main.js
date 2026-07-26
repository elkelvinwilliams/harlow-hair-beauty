/* Hagiazo Hair — shared behaviour. Vanilla JS, no dependencies.
   All motion is transform/opacity only, driven by rAF / IntersectionObserver,
   and fully disabled when the visitor prefers reduced motion. */
(() => {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer   = window.matchMedia('(hover: hover) and (pointer: fine)');

  /* ─── Unified scroll pipeline (single passive listener + rAF tick) ────── */
  const nav = document.getElementById('site-nav');

  const progressBar = document.createElement('div');
  progressBar.id = 'scroll-progress';
  progressBar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(progressBar);

  const parallaxEls    = Array.from(document.querySelectorAll('[data-parallax]'));
  const scrollHint     = document.querySelector('.scroll-indicator');
  let ticking = false;

  const onFrame = () => {
    ticking = false;
    const doc = document.documentElement;
    const y   = window.scrollY || doc.scrollTop;

    if (nav) nav.classList.toggle('scrolled', y > 60);

    const max = doc.scrollHeight - doc.clientHeight;
    progressBar.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';

    if (!reducedMotion.matches) {
      // Gentle hero parallax — only while the hero is on screen.
      const vh = window.innerHeight;
      if (y < vh) {
        for (const el of parallaxEls) {
          const factor = parseFloat(el.dataset.parallax) || 0;
          el.style.transform = 'translate3d(0,' + (y * factor).toFixed(1) + 'px,0)';
        }
        if (scrollHint) scrollHint.style.opacity = Math.max(0, 1 - y / 240).toFixed(2);
      }
    }
  };

  const requestFrame = () => {
    if (!ticking) { ticking = true; requestAnimationFrame(onFrame); }
  };
  window.addEventListener('scroll', requestFrame, { passive: true });
  window.addEventListener('resize', requestFrame, { passive: true });
  onFrame();

  /* ─── Mobile menu ─────────────────────────────────────────────────────── */
  const menuBtn    = document.getElementById('menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const iconOpen   = document.getElementById('menu-icon-open');
  const iconClose  = document.getElementById('menu-icon-close');

  if (menuBtn && mobileMenu) {
    const setMenu = open => {
      mobileMenu.classList.toggle('open', open);
      if (nav) nav.classList.toggle('menu-open', open);
      if (iconOpen)  iconOpen.classList.toggle('hidden', open);
      if (iconClose) iconClose.classList.toggle('hidden', !open);
      menuBtn.setAttribute('aria-expanded', String(open));
      menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };

    menuBtn.addEventListener('click', () => setMenu(!mobileMenu.classList.contains('open')));
    mobileMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
    document.addEventListener('click', e => {
      if (nav && !nav.contains(e.target) && mobileMenu.classList.contains('open')) setMenu(false);
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
        setMenu(false);
        menuBtn.focus();
      }
    });
  }

  /* ─── Active nav link (class + aria, no inline styles) ────────────────── */
  const page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('[data-nav-link]').forEach(link => {
    if (link.getAttribute('href') === page) link.setAttribute('aria-current', 'page');
  });

  /* ─── Scroll reveal (IntersectionObserver, reduced-motion aware) ──────── */
  const reveals = document.querySelectorAll('.reveal, .clip-reveal');
  if (reveals.length) {
    const showAll = () => reveals.forEach(el => el.classList.add('visible'));
    if (reducedMotion.matches || !('IntersectionObserver' in window)) {
      showAll();
    } else {
      const io = new IntersectionObserver(entries => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            io.unobserve(entry.target);
          }
        }
      }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
      reveals.forEach(el => io.observe(el));
      // If the preference flips mid-visit, finish everything instantly.
      reducedMotion.addEventListener('change', e => { if (e.matches) { showAll(); io.disconnect(); } });
    }
  }

  /* ─── Magnetic pull on primary CTAs (fine pointers only) ──────────────── */
  if (finePointer.matches && !reducedMotion.matches) {
    const MAX = 4; // px — a whisper, not a gimmick
    document.querySelectorAll('.btn-cream, .btn-primary').forEach(btn => {
      btn.addEventListener('pointermove', e => {
        const r  = btn.getBoundingClientRect();
        const dx = (e.clientX - (r.left + r.width / 2)) / (r.width / 2);
        const dy = (e.clientY - (r.top + r.height / 2)) / (r.height / 2);
        btn.style.transform = 'translate(' + (dx * MAX).toFixed(1) + 'px,' + (dy * MAX).toFixed(1) + 'px)';
      });
      btn.addEventListener('pointerleave', () => { btn.style.transform = ''; });
      btn.addEventListener('blur', () => { btn.style.transform = ''; });
    });
  }

  /* ─── Gallery filter ──────────────────────────────────────────────────── */
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

  /* ─── Animated stat counters ──────────────────────────────────────────── */
  const counters = document.querySelectorAll('.stat-num[data-count]');
  if (counters.length) {
    const run = el => {
      const target = parseInt(el.dataset.count, 10) || 0;
      if (reducedMotion.matches) { el.textContent = target; return; }
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
    if ('IntersectionObserver' in window) {
      const cio = new IntersectionObserver(entries => {
        for (const entry of entries) {
          if (entry.isIntersecting) { run(entry.target); cio.unobserve(entry.target); }
        }
      }, { threshold: 0.6 });
      counters.forEach(c => cio.observe(c));
    } else {
      counters.forEach(run);
    }
  }

  /* ─── Floating live-chat launcher ─────────────────────────────────────── */
  const chatWidget = document.getElementById('chat-widget');
  const chatToggle = document.getElementById('chat-toggle');
  if (chatWidget && chatToggle) {
    const setOpen = open => {
      chatWidget.classList.toggle('open', open);
      chatToggle.setAttribute('aria-expanded', String(open));
    };
    chatToggle.addEventListener('click', e => {
      e.stopPropagation();
      setOpen(!chatWidget.classList.contains('open'));
    });
    document.addEventListener('click', e => {
      if (!chatWidget.contains(e.target)) setOpen(false);
    });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });
  }

  /* ─── Contact form (demo) ─────────────────────────────────────────────── */
  const form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const btn = form.querySelector('[type="submit"]');
      if (!btn) return;
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
})();
