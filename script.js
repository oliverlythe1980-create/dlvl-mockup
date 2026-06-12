// ── Header: transparent over hero, glass after scrolling ──
(function () {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 30);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();

// ── Toast helper ──
function dlvlToast(msg) {
  let t = document.querySelector('.toast');
  if (!t) {
    t = document.createElement('div');
    t.className = 'toast';
    t.setAttribute('role', 'status');
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.classList.add('toast--show');
  clearTimeout(t._hide);
  t._hide = setTimeout(() => t.classList.remove('toast--show'), 3200);
}

// ── Mobile: hamburger menu + sticky WhatsApp bar (injected) ──
(function () {
  const actions = document.querySelector('.header-actions');
  const nav = document.querySelector('.site-nav');
  if (actions && nav) {
    const btn = document.createElement('button');
    btn.className = 'nav-toggle';
    btn.setAttribute('aria-label', 'Open menu');
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = '<span></span><span></span><span></span>';
    actions.appendChild(btn);
    btn.addEventListener('click', () => {
      const open = document.body.classList.toggle('nav-open');
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    nav.addEventListener('click', (e) => {
      if (e.target.closest('a')) document.body.classList.remove('nav-open');
    });
  }

  const es = document.documentElement.lang === 'es';
  const bar = document.createElement('a');
  bar.className = 'mobile-wa';
  bar.href = 'https://wa.me/6282145538716';
  bar.textContent = es ? 'Escríbenos por WhatsApp, respondemos rápido' : 'Chat on WhatsApp, we answer fast';
  document.body.appendChild(bar);
})();

// ── WhatsApp glyph on every WhatsApp button ──
(function () {
  const ICO = '<svg class="wa-ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413"/></svg>';
  document.querySelectorAll('.pill-btn--whatsapp, .mobile-wa').forEach((b) => {
    b.insertAdjacentHTML('afterbegin', ICO);
  });
})();

// ── Contact form → pre-filled WhatsApp message ──
(function () {
  const form = document.getElementById('enquiry-form');
  if (!form) return;
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const es = document.documentElement.lang === 'es';
    const v = (id) => (document.getElementById(id)?.value || '').trim();
    const L = es
      ? { hi: 'Hola! Consulta desde la web:', name: 'Nombre', email: 'Email', course: 'Me interesa', dates: 'Fechas', msg: 'Mensaje', toast: 'Abriendo WhatsApp con tu consulta…' }
      : { hi: 'Hi! Enquiry from the website:', name: 'Name', email: 'Email', course: 'Interested in', dates: 'Dates', msg: 'Message', toast: 'Opening WhatsApp with your enquiry…' };
    const lines = [
      L.hi,
      v('f-name') && `${L.name}: ${v('f-name')}`,
      v('f-email') && `${L.email}: ${v('f-email')}`,
      `${L.course}: ${v('f-course')}`,
      v('f-dates') && `${L.dates}: ${v('f-dates')}`,
      v('f-msg') && `${L.msg}: ${v('f-msg')}`,
    ].filter(Boolean);
    window.open('https://wa.me/6282145538716?text=' + encodeURIComponent(lines.join('\n')), '_blank');
    dlvlToast(L.toast);
  });
})();

// ── Dive-sites carousel: arrow stepping, seamless loop, progress dots ──
(function () {
  const track = document.getElementById('sitesTrack');
  const prevBtn = document.querySelector('.carousel-arrow--prev');
  const nextBtn = document.querySelector('.carousel-arrow--next');
  if (!track || !prevBtn || !nextBtn) return;

  const cards = Array.from(track.children);
  const N = parseInt(track.dataset.uniqueCount || '0', 10) || cards.length / 2;
  let current = 0;
  let animating = false;

  // progress dots under the carousel
  const wrapper = document.querySelector('.sites-carousel-wrapper');
  const dotsWrap = document.createElement('div');
  dotsWrap.className = 'carousel-dots';
  dotsWrap.setAttribute('aria-hidden', 'true');
  const dots = [];
  for (let i = 0; i < N; i++) {
    const d = document.createElement('button');
    d.className = 'carousel-dot';
    d.type = 'button';
    d.tabIndex = -1;
    d.addEventListener('click', () => { if (!animating) { current = i; setTransform(true); } });
    dotsWrap.appendChild(d);
    dots.push(d);
  }
  wrapper.parentNode.insertBefore(dotsWrap, wrapper.nextSibling);

  function updateDots() {
    const idx = ((current % N) + N) % N;
    dots.forEach((d, i) => d.classList.toggle('carousel-dot--active', i === idx));
  }

  function cardStep() {
    const w = cards[0].getBoundingClientRect().width;
    const gap = parseFloat(getComputedStyle(track).gap) || 6;
    return w + gap;
  }

  function setTransform(animate) {
    track.style.transition = animate ? 'transform 0.45s cubic-bezier(0.16, 1, 0.3, 1)' : 'none';
    track.style.transform = `translateX(-${current * cardStep()}px)`;
    if (animate) animating = true;
    updateDots();
  }

  function goNext() { if (!animating) { current++; setTransform(true); } }
  function goPrev() {
    if (animating) return;
    if (current <= 0) {
      current = N;
      setTransform(false);
      void track.offsetHeight;
    }
    current--;
    setTransform(true);
  }

  track.addEventListener('transitionend', (e) => {
    if (e.target !== track) return;
    animating = false;
    if (current >= N) {
      current -= N;
      setTransform(false);
    }
  });

  nextBtn.addEventListener('click', goNext);
  prevBtn.addEventListener('click', goPrev);
  window.addEventListener('resize', () => setTransform(false), { passive: true });
  updateDots();
})();

// ── Count-up on the big stat numbers (trust bar + facts bars) ──
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!('IntersectionObserver' in window)) return;

  function countUp(el) {
    const orig = el.textContent;
    const m = orig.match(/^([^0-9]*)(\d+(?:\.\d)?)(.*)$/);
    if (!m) return;
    const target = parseFloat(m[2]);
    const dec = m[2].includes('.') ? 1 : 0;
    const dur = 1100;
    const t0 = performance.now();
    function tick(t) {
      const p = Math.min((t - t0) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = m[1] + (target * eased).toFixed(dec) + m[3];
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = orig;
    }
    requestAnimationFrame(tick);
  }

  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.isIntersecting) {
        countUp(e.target);
        io.unobserve(e.target);
      }
    }
  }, { threshold: 0.6 });
  document.querySelectorAll('.trust-item strong, .fact strong').forEach((el) => io.observe(el));
})();

// ── FAQ: opening one answer closes the others ──
(function () {
  document.querySelectorAll('.faq').forEach((faq) => {
    faq.addEventListener('toggle', (e) => {
      if (e.target.open) {
        faq.querySelectorAll('details[open]').forEach((d) => {
          if (d !== e.target) d.open = false;
        });
      }
    }, true);
  });
})();

// ── Nav: mark the current page ──
(function () {
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.site-nav a').forEach((a) => {
    const href = (a.getAttribute('href') || '').split('#')[0];
    if (href && href === page) a.setAttribute('aria-current', 'page');
  });
})();


// ── Coast map: postcard preview anchored beside the hovered pin ──
(function () {
  const map = document.querySelector('.coast-map');
  if (!map) return;
  const card = document.createElement('div');
  card.className = 'map-card';
  map.appendChild(card);

  map.querySelectorAll('a[data-name]').forEach((a) => {
    a.addEventListener('mouseenter', () => {
      const img = a.dataset.img ? '<img src="' + a.dataset.img + '" alt="">' : '';
      card.innerHTML = img +
        '<div class="map-card-b">' +
        '<strong>' + a.dataset.name + '</strong>' +
        '<span>' + a.dataset.meta + '</span>' +
        '<em>' + a.dataset.desc + '</em>' +
        '</div>';
      card.classList.add('map-card--show');
      const r = map.getBoundingClientRect();
      const sr = map.querySelector('.coast-svg').getBoundingClientRect();
      const c = a.querySelector('circle');
      // pin centre in map coordinates, measured against the SVG itself
      const px = parseFloat(c.getAttribute('cx')) / 1200 * sr.width + (sr.left - r.left);
      const py = parseFloat(c.getAttribute('cy')) / 460 * sr.height + (sr.top - r.top);
      const w = card.offsetWidth;
      const h = card.offsetHeight;
      // sit above the pin row so neither pin nor label is covered; fall below if no room
      let left = px + 24;
      if (left + w > r.width - 8) left = px - w - 24;
      left = Math.max(8, left);
      let top = py - h - 16;
      if (top < 8) top = py + 24;
      if (top + h > r.height - 8) top = r.height - h - 8;
      card.style.left = left + 'px';
      card.style.top = top + 'px';
    });
    a.addEventListener('mouseleave', () => card.classList.remove('map-card--show'));
  });
})();

// ── Scroll-reveal ──
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!('IntersectionObserver' in window)) return;

  const els = document.querySelectorAll(
    '.course-card, .site-card, .eco-card, .review-card, .team-card, ' +
    '.section-hed, .section-sub, .stay-card, .google-badge, .day, ' +
    '.quote-text, .quote-attribution, .booking-card'
  );

  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.isIntersecting) {
        e.target.classList.add('in-view');
        io.unobserve(e.target);
      }
    }
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  els.forEach((el, i) => {
    el.classList.add('reveal');
    el.style.setProperty('--d', `${(i % 3) * 110}ms`);
    io.observe(el);
  });
})();
