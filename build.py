#!/usr/bin/env python3
"""Generates the inner pages of the DLVL mockup from shared templates."""
import os

import html as _html, json as _json, re as _re

BASE = "https://divinglavidaloca.com/"

def _clean(s):
    return _html.unescape(_re.sub(r"<[^>]+>", "", s)).strip()

def _faq_schema(body):
    pairs = _re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", body, _re.S)
    if not pairs:
        return ""
    items = [{"@type": "Question", "name": _clean(q),
              "acceptedAnswer": {"@type": "Answer", "text": _clean(a)}} for q, a in pairs]
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + "</script>\n"

def _course_schema(title, desc, url):
    name = title.split("|")[0].split("\u00b7")[0].strip()
    data = {"@context": "https://schema.org", "@type": "Course", "name": name, "description": desc,
            "provider": {"@type": "LocalBusiness", "name": "Diving La Vida Loca", "url": BASE},
            "url": url}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + "</script>\n"

OUT = os.path.dirname(os.path.abspath(__file__))
WP = "https://divinglavidaloca.com/wp-content/uploads"
WA = "https://wa.me/6282145538716"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,700;1,800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/webp" href="https://divinglavidaloca.com/wp-content/uploads/2022/08/DivingLaVidaLoca-150x150.webp">\n<meta name="google" content="notranslate">
<link rel="canonical" href="{{SELF}}">
<link rel="alternate" hreflang="en" href="{{EN_ABS}}">
<link rel="alternate" hreflang="es" href="{{ES_ABS}}">
<link rel="alternate" hreflang="x-default" href="{{EN_ABS}}">
<meta property="og:type" content="website">
<meta property="og:title" content="{{TITLE}}">
<meta property="og:description" content="{{DESC}}">
<meta property="og:url" content="{{SELF}}">
<meta property="og:image" content="https://divinglavidaloca.com/wp-content/uploads/2022/09/Open_water_padi.webp">
<meta property="og:site_name" content="Diving La Vida Loca">
<meta name="twitter:card" content="summary_large_image">
{{SCHEMA}}<link rel="stylesheet" href="styles.css?v=54">
</head>
<body>

<header class="site-header">
  <div class="header-inner">
    <a href="index.html" class="brand">
      <img class="brand-logo" src="WPURL/2022/08/DivingLaVidaLoca-215x214.webp" alt="Diving La Vida Loca logo" width="46" height="46">
      <span class="brand-name">Diving La Vida Loca<small>PADI Dive Center &middot; Amed &middot; Bali</small></span>
    </a>
    <nav class="site-nav" aria-label="Main">
      <a href="index.html#courses">Courses</a>
      <a href="dive-sites.html">Dive Sites</a>
      <a href="fun-dives.html">Fun Dives</a>
      <a href="stay-and-dive.html">Stay &amp; Dive</a>
      <a href="blog.html">Blog</a>
      <a href="about.html">About</a>
      <a href="contact.html">Contact</a>
    </nav>
    <div class="header-actions">
      <span class="lang-toggle"><strong>EN</strong> / <a class="lang-es" href="{{ES_URL}}">ES</a></span>
      <div class="header-social">
        <a class="social-icon" href="https://www.instagram.com/diving.lavidaloca" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="2.5" y="2.5" width="19" height="19" rx="5.4"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.15" fill="currentColor" stroke="none"/></svg></a>
        <a class="social-icon" href="https://www.facebook.com/Divinglavidaloca" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0 0 22 12z"/></svg></a>
        <a class="social-icon social-icon--whatsapp" href="WAURL" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M19.05 4.91A9.82 9.82 0 0 0 12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.91-7.02zM12.05 20.15h-.01a8.2 8.2 0 0 1-4.18-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.18 8.18 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.24-8.23a8.2 8.2 0 0 1 8.23 8.24c0 4.54-3.7 8.23-8.23 8.23zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.16.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.51.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43-.14 0-.31-.01-.48-.01-.17 0-.43.06-.66.31-.23.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.24 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.28z"/></svg></a>
      </div>
    </div>
  </div>
</header>
""".replace("WPURL", WP).replace("WAURL", WA)

FOOT = """
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">
          <img src="WPURL/2022/08/DivingLaVidaLoca-215x214.webp" alt="" width="56" height="56">
          <span>Diving La Vida Loca</span>
        </div>
        <p class="footer-tag">Boutique PADI dive center between the rice fields of Amed, Bali, 500 m from Melasti beach. Never more than four divers per trip.</p>
      </div>
      <div>
        <h4>Dive</h4>
        <ul>
          <li><a href="index.html#courses">PADI Courses</a></li>
          <li><a href="dive-sites.html">Dive Sites</a></li>
          <li><a href="fun-dives.html">Fun Dives &amp; Prices</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="plan-your-trip.html">Tailor Your Trip</a></li>
          <li><a href="stay-and-dive.html">Stay &amp; Dive</a></li>
        </ul>
      </div>
      <div>
        <h4>About</h4>
        <ul>
          <li><a href="about.html">The Team</a></li>
          <li><a href="conservation.html">Conservation</a></li>
          <li><a href="index.html#reviews">Reviews</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="WAURL">WhatsApp +62 821 4553 8716</a></li>
          <li><a href="https://www.instagram.com/diving.lavidaloca">Instagram</a></li>
          <li><a href="https://www.facebook.com/Divinglavidaloca">Facebook</a></li>
          <li>Amed, Karangasem &middot; Bali</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Diving La Vida Loca &middot; PADI Dive Center</span>
      <span>English &middot; <a href="{{ES_URL}}">Espa&ntilde;ol</a></span>
    </div>
  </div>
</footer>

<script src="script.js?v=7" defer></script>
</body>
</html>
""".replace("WPURL", WP).replace("WAURL", WA)



def coast_map(lang):
    en = lang == "en"
    guide = "amed-diving-guide.html" if en else "amed-diving-guide-es.html"
    T = (lambda a, b: a) if en else (lambda a, b: b)
    pins = [
        (1,  "boga",            95, 158, T("Boga Wreck", "Pecio Boga"), "r",
              "16&ndash;40 m &middot; " + T("Wreck &middot; Advanced", "Pecio &middot; Avanzado"),
              T("Purpose-sunk in 2012; statues and a sunken car on deck.", "Hundido a prop&oacute;sito en 2012; estatuas y un coche en cubierta."), ""),
        (2,  "liberty",        162, 192, T("USAT Liberty", "USAT Liberty"), "r",
              "5&ndash;30 m &middot; " + T("Wreck &middot; All levels", "Pecio &middot; Todos los niveles"),
              T("120 m WWII wreck; bumpheads at dawn.", "Pecio de 120 m de la II GM; cabezones al amanecer."), "2022/09/Advanced_open_water.webp"),
        (3,  "coral-garden",   218, 200, "Coral Garden", "r",
              "2&ndash;12 m &middot; " + T("Reef &middot; All levels", "Arrecife &middot; Todos los niveles"),
              T("Statues and soft coral; long, easy dives.", "Estatuas y coral blando; inmersiones largas y f&aacute;ciles."), "2022/09/Nitrox.webp"),
        (4,  "coral-garden",   274, 184, "Drop-Off", "r",
              "10&ndash;40 m &middot; " + T("Wall &middot; Advanced", "Pared &middot; Avanzado"),
              T("Volcanic wall, giant gorgonians.", "Pared volc&aacute;nica, gorgonias gigantes."), "2022/09/Advanced_open_water.webp"),
        (5,  "batu-kelebit",   332, 166, "Batu Kelebit", "r",
              "15&ndash;40 m &middot; " + T("Ridges &middot; Advanced", "Crestas &middot; Avanzado"),
              T("Deep ridges with real pelagic chances.", "Crestas profundas con opciones pel&aacute;gicas de verdad."), ""),
        (6,  "seraya",         402, 188, "Seraya Secrets", "r",
              "5&ndash;20 m &middot; Muck &middot; " + T("All levels", "Todos los niveles"),
              T("Frogfish, harlequin shrimp: macro heaven.", "Peces sapo, gambas arlequ&iacute;n: para&iacute;so macro."), "2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp"),
        (7,  "pyramids",       640, 250, T("Melasti Reef", "Arrecife de Melasti"), "r",
              "4&ndash;20 m &middot; " + T("Reef &middot; All levels", "Arrecife &middot; Todos los niveles"),
              T("Resident turtles, 500 m from our door.", "Tortugas residentes, a 500 m de la puerta."), "2022/09/Rescue_diver-1.webp"),
        (8,  "pyramids",       692, 258, T("The Pyramids", "Las Pir\u00e1mides"), "r",
              "5&ndash;22 m &middot; " + T("Artificial reef", "Arrecife artificial"),
              T("Glassfish swarms; our navigation classroom.", "Enjambres de peces cristal; nuestra aula de navegaci\u00f3n."), "2022/09/DiveMasterw.webp"),
        (9,  "jemeluk",        748, 280, T("Jemeluk Bay", "Bah\u00eda de Jemeluk"), "r",
              "3&ndash;25 m &middot; " + T("Reef &middot; All levels", "Arrecife &middot; Todos los niveles"),
              T("Our house reef and training bay.", "Nuestro arrecife de casa y bah\u00eda de pr\u00e1cticas."), "2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp"),
        (10, "bunutan",        846, 284, "Bunutan", "r",
              "10&ndash;30 m &middot; " + T("Point &middot; All levels", "Punta &middot; Todos los niveles"),
              T("Garden eels and a gentle drift.", "Anguilas jard&iacute;n y una deriva suave."), ""),
        (11, "lipah",          906, 302, T("Lipah Bay", "Bah\u00eda de Lipah"), "r",
              "3&ndash;20 m &middot; " + T("Bay &middot; All levels", "Bah&iacute;a &middot; Todos los niveles"),
              T("Coral bommies; easy diving and snorkelling.", "Bommies de coral; buceo f&aacute;cil y esn&oacute;rquel."), ""),
        (12, "japanese-wreck", 966, 320, T("Japanese Wreck", "Pecio Japon\u00e9s"), "r",
              "2&ndash;12 m &middot; " + T("Wreck &middot; All levels", "Pecio &middot; Todos los niveles"),
              T("Soft-coral-covered and snorkelable.", "Forrado de coral blando, visible con esn&oacute;rquel."), "2022/09/Open_water_padi.webp"),
        (13, "gili-selang",   1150, 392, "Gili Selang", "r",
              "5&ndash;30 m &middot; " + T("Currents &middot; Advanced only", "Corrientes &middot; Solo avanzados"),
              T("Pristine coral at Bali&rsquo;s eastern tip. Ask us.", "Coral intacto en la punta este de Bali. Preg&uacute;ntanos."), ""),
    ]
    pin_html = ""
    # absolute label positions: two flat rows per cluster, language-tuned for longer ES names
    LPOS = {
        1: (95, 126), 2: (162, 100), 3: (T(214, 214), 126), 4: (274, 100), 5: (T(340, 340), 126), 6: (402, 100),
        7: (T(640, 622), 190), 8: (692, 216), 9: (T(748, 770), 190), 10: (846, 216), 11: (T(906, 920), 190), 12: (966, 216),
        13: (1132, 366),
    }
    for i, (n, anchor, x, y, label, side, meta, desc, img) in enumerate(pins):
        lx, ly = LPOS[n]
        plain = label.replace("&middot;", "\u00b7")
        imgattr = f' data-img="{WP}/{img}"' if img else ""
        site_slug = {"Drop-Off":"drop-off","Melasti Reef":"melasti","Arrecife de Melasti":"melasti"}.get(plain, anchor)
        pin_html += f"""
      <a href="site-{site_slug}.html" data-name="{plain}" data-meta="{meta}" data-desc="{desc}"{imgattr}>
        <circle class="pin-c" cx="{x}" cy="{y}" r="11" fill="#91131b" stroke="#c9a227" stroke-width="1.5"/>
        <text x="{x}" y="{y + 4}" text-anchor="middle" style="font: 700 10px Inter, sans-serif; fill: #fff;">{n}</text>
        <line x1="{x}" y1="{y - 12}" x2="{lx}" y2="{ly + 5}" stroke="#c9a227" stroke-width="1" opacity="0.45"/>
        <text x="{lx}" y="{ly}" text-anchor="middle" style="font: 600 11px Inter, sans-serif; letter-spacing: 1.2px; text-transform: uppercase; fill: #2a1d18;">{label}</text>
      </a>"""
    sea = "Bali Sea" if en else "Mar de Bali"
    note = "Hand-drawn &middot; not to scale" if en else "Dibujado a mano &middot; sin escala"
    shop = "Diving La Vida Loca"
    title = ("The Coast at a Glance" if en else "La Costa de un Vistazo")
    sub = ("Thirteen sites along one volcanic shoreline, from the Boga Wreck at Kubu to Gili Selang at Bali&rsquo;s eastern tip. Tap a pin to read its chapter in the guide."
           if en else
           "Trece puntos en una misma costa volc\u00e1nica, del pecio Boga en Kubu hasta Gili Selang en la punta este de Bali. Toca un pin para leer su cap\u00edtulo en la gu\u00eda.")
    COAST = "M -4,170 C 60,163 115,162 140,172 C 165,198 245,206 280,182 C 305,162 318,160 340,168 C 365,180 385,184 405,190 C 470,212 545,228 612,244 C 648,252 668,256 700,262 C 722,288 766,292 794,272 C 838,282 890,298 940,312 C 990,328 1040,348 1078,366 C 1106,380 1116,404 1108,430 C 1102,446 1098,452 1096,460"
    return f"""
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">{title}</h2></div>
    <p class="section-sub">{sub}</p>
    <div class="coast-map">
      <svg class="coast-svg" viewBox="0 0 1200 460" role="img" aria-label="{title}">
        <rect width="1200" height="460" fill="#f9f3e8"/>
        <path d="{COAST} L 1096,460 L -4,460 Z" fill="#ead9c0"/>
        <path d="{COAST}" fill="none" stroke="#c9a227" stroke-width="3" stroke-linecap="round"/>
        <path d="M 250,420 L 310,326 L 370,420" fill="none" stroke="#2a1d18" stroke-width="2" stroke-linejoin="round" opacity="0.5"/>
        <path d="M 285,372 L 308,344 L 328,374" fill="none" stroke="#2a1d18" stroke-width="1.3" opacity="0.35"/>
        <text x="310" y="442" text-anchor="middle" style="font: 600 10px Inter, sans-serif; letter-spacing: 2px; text-transform: uppercase; fill: #75655c;">Gunung Agung</text>
        <text x="960" y="84" style="font: italic 700 24px 'Playfair Display', serif; fill: #c9a227;">{sea}</text>
        <g stroke="#c9a227" stroke-width="1.4" fill="none" opacity="0.45">
          <path d="M 520,90 q7,-7 14,0 q7,7 14,0"/><path d="M 700,120 q7,-7 14,0 q7,7 14,0"/>
          <path d="M 860,160 q7,-7 14,0 q7,7 14,0"/><path d="M 1020,210 q7,-7 14,0 q7,7 14,0"/>
          <path d="M 420,70 q7,-7 14,0 q7,7 14,0"/><path d="M 600,60 q7,-7 14,0 q7,7 14,0"/>
        </g>
        <g transform="translate(1150,52)"><line x1="0" y1="14" x2="0" y2="-12" stroke="#91131b" stroke-width="2"/><path d="M0,-12 L-5,-3 L5,-3 Z" fill="#91131b"/><text x="0" y="30" text-anchor="middle" style="font: 700 11px Inter, sans-serif; fill: #91131b;">N</text></g>
        <ellipse cx="1150" cy="392" rx="20" ry="12" fill="#ead9c0" stroke="#c9a227" stroke-width="2"/>
        <g>
          <circle cx="622" cy="300" r="13" fill="#91131b" stroke="#c9a227" stroke-width="2"/>
          <text x="622" y="305" text-anchor="middle" style="font: 700 12px Inter, sans-serif; fill: #e6c45c;">&#9733;</text>
          <text x="622" y="332" text-anchor="middle" style="font: 700 10px Inter, sans-serif; letter-spacing: 1.4px; text-transform: uppercase; fill: #91131b;">{shop}</text>
        </g>{pin_html}
        <text x="36" y="442" style="font: italic 500 12px 'Playfair Display', serif; fill: #75655c;">{note}</text>
        <rect x="1.5" y="1.5" width="1197" height="457" fill="none" stroke="#c9a227" stroke-width="3"/>
      </svg>
    </div>
"""

def hero(img, crumb, title, lede, pos=None):
    style = f' style="object-position: {pos};"' if pos else ""
    return f"""
<section class="course-hero">
  <img class="bg" src="{img}"{style} alt="" aria-hidden="true" fetchpriority="high">
  <div class="container course-hero-body">
    <p class="breadcrumb">{crumb}</p>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>
"""


def facts(items):
    cells = "\n".join(f'    <div class="fact"><strong>{a}</strong><span>{b}</span></div>' for a, b in items)
    return f'<section class="facts-bar" aria-label="Key facts">\n  <div class="facts-inner">\n{cells}\n  </div>\n</section>\n'


def booking(price, sub, options, wa_text, trust):
    opts = "\n".join(f'      <li><span>{a}</span><span>{b}</span></li>' for a, b in options)
    ticks = "\n".join(f'      <li>{t}</li>' for t in trust)
    return f"""
  <aside class="booking-card" aria-label="Book">
    <p class="booking-price">{price}<small>{sub}</small></p>
    <ul class="booking-options">
{opts}
    </ul>
    <a class="pill-btn" href="plan-your-trip.html">Tailor your trip &rarr;</a>
    <p class="booking-note">No deposit needed to ask: tell us your dates and we&rsquo;ll confirm availability.</p>
    <ul class="booking-trust">
{ticks}
    </ul>
  </aside>
"""


TRUST_DEFAULT = [
    "5.0 &#9733; from 508 Google reviews",
    "Max 4 divers per instructor",
    "Taught in EN &middot; ES &middot; CA &middot; FR &middot; ID",
    "Free pickup in the Amed area",
]

QUOTE = """
<section class="hp-quote">
  <div class="container">
    <p class="quote-text">&ldquo;{{Q}}&rdquo;</p>
    <span class="quote-attribution">{{A}}</span>
  </div>
</section>
"""


def quote(q, a):
    return QUOTE.replace("{{Q}}", q).replace("{{A}}", a)


pages = {}

# ─────────────────────────── DISCOVER SCUBA ───────────────────────────
pages["course-discover-scuba.html"] = (
    "Discover Scuba Diving in Amed, Bali · No Experience Needed | Diving La Vida Loca",
    "Try scuba diving for the first time in Amed, Bali. Half-day Discover Scuba experience with private pool practice and a guided reef dive. From IDR 1.050.000, all equipment included.",
    hero(f"{WP}/2024/07/GOPR9425-scaled.webp",
         '<a href="index.html">Home</a> / <a href="index.html#courses">Courses</a> / Discover Scuba',
         "Discover Scuba Diving",
         "Your first breath underwater, taken gently. A morning in our private pool, then a guided reef dive with an instructor beside you the whole way. No experience, no certification, no pressure.")
    + facts([("Half day", "duration"), ("12 m", "max depth"), ("Age 10+", "minimum age"), ("1&ndash;2", "reef dives"), ("Max 4", "per instructor")])
    + f"""
<div class="container course-layout">
  <div class="course-content">
    <h2>How the morning unfolds</h2>
    <div class="day-plan">
      <div class="day"><h3>1 · Coffee &amp; briefing</h3><p>We talk through how breathing underwater actually works, what you&rsquo;ll feel, and the three simple skills you&rsquo;ll practise. Questions encouraged, this is a conversation, not a lecture.</p></div>
      <div class="day"><h3>2 · The pool</h3><p>Standing-depth water, your instructor at arm&rsquo;s length. You&rsquo;ll breathe, clear your mask, and get comfortable at exactly your own pace. Nobody leaves the pool until they&rsquo;re smiling.</p></div>
      <div class="day"><h3>3 · The reef</h3><p>A calm shore entry at Jemeluk Bay, our house reef. Forty-five minutes among the coral with your instructor guiding, most people are too busy looking at fish to remember being nervous.</p></div>
    </div>
    <h2>What&rsquo;s included</h2>
    <ul>
      <li>All equipment, fitted to you before you get wet</li>
      <li>Private pool session, never a crowded hotel pool</li>
      <li>Guided reef dive(s) with transport in the Amed area</li>
      <li>Coffee, tea, water and snacks</li>
      <li>10% government tax: the price you see is the price you pay</li>
    </ul>
    <h2>Questions first-timers actually ask</h2>
    <div class="faq">
      <details><summary>I&rsquo;m scared I&rsquo;ll panic. What happens then?</summary><p>Then we slow down. The pool has standing depth, your instructor never leaves your side, and there is no schedule pushing you forward. Plenty of our best divers started exactly this nervous.</p></details>
      <details><summary>Do I need to be a strong swimmer?</summary><p>You need to be comfortable in water, not fast in it. If you can float and paddle, you can do this.</p></details>
      <details><summary>Does this count towards a certification?</summary><p>It&rsquo;s not a certification itself, but the skills carry straight into the PADI Open Water course, and if you continue with us, you&rsquo;ve already met the family.</p></details>
    </div>
  </div>
"""
    + booking("IDR 1.050.000", "&asymp; &euro;55 &middot; 1 dive &middot; all taxes &amp; equipment included",
              [("2 dives instead of 1", "IDR 1.450.000"),
               ("2 dives + 1 night &amp; breakfast", "IDR 1.700.000"),
               ("Continue to Open Water", "ask us")],
              "Hi!%20I%27d%20like%20to%20try%20Discover%20Scuba.%20My%20dates%20are%3A", TRUST_DEFAULT)
    + "\n</div>\n"
    + quote("Welcoming, kind and helpful. An amazing experience from start to finish.", "Google review &middot; one of 508 five-star reviews"),
)

# ─────────────────────────── ADVANCED ───────────────────────────
pages["course-advanced.html"] = (
    "PADI Advanced Open Water in Amed, Bali · Dive the Liberty Wreck | Diving La Vida Loca",
    "PADI Advanced Open Water course in Amed, Bali. Five adventure dives over two days including the USAT Liberty wreck and a 30 m deep dive. IDR 4.900.000, taxes included.",
    hero(f"{WP}/2022/09/Advanced_open_water.webp",
         '<a href="index.html">Home</a> / <a href="index.html#courses">Courses</a> / Advanced Open Water',
         "PADI Advanced Open Water",
         "Five adventure dives in two days, including the descent to 30 metres and, the one everyone comes for, the USAT Liberty wreck. This is the course Amed was made for.")
    + facts([("2 days", "duration"), ("30 m", "certified depth"), ("Age 12+", "minimum age"), ("5 dives", "adventure dives"), ("Max 4", "per instructor")])
    + f"""
<div class="container course-layout">
  <div class="course-content">
    <h2>What the two days look like</h2>
    <div class="day-plan">
      <div class="day"><h3>Day 1 · Navigation &amp; adventure dives</h3><p>Underwater navigation on the house reef, then two adventure dives chosen with you, peak buoyancy and fish ID are favourites. Knowledge reviews happen over coffee between dives, not in a classroom after them.</p></div>
      <div class="day"><h3>Day 2 · Deep &amp; the wreck</h3><p>Morning deep dive to 30 metres, where we show you how colour and light change, then the USAT Liberty wreck dive. A 120-metre WWII shipwreck, entered from the beach. There&rsquo;s no better adventure dive anywhere.</p></div>
    </div>
    <h2>What&rsquo;s included</h2>
    <ul>
      <li>Five adventure dives with all equipment and a dive computer</li>
      <li>The Liberty wreck and a 30 m deep dive as standard</li>
      <li>PADI certification fees and digital materials</li>
      <li>Transport, coffee, tea, water and snacks between dives</li>
      <li>10% government tax included</li>
    </ul>
    <h2>Questions divers actually ask</h2>
    <div class="faq">
      <details><summary>Can I take this straight after Open Water?</summary><p>Yes, and in Amed most people do. Our Open Water + Advanced pack (IDR 9.900.000) runs the two as one five-day arc, which is the best-value way to reach the wreck.</p></details>
      <details><summary>Which adventure dives can I choose?</summary><p>Deep and navigation are required. For the other three we&rsquo;ll talk through what excites you, wreck, peak performance buoyancy, fish ID, night, and more.</p></details>
      <details><summary>Is 30 metres a big jump?</summary><p>It&rsquo;s gradual and guided. We descend together along a reference, watching how you feel the whole way, with four divers maximum, nobody disappears into a crowd.</p></details>
    </div>
  </div>
"""
    + booking("IDR 4.900.000", "&asymp; &euro;255 per person &middot; all taxes &amp; equipment included",
              [("2 or more people", "IDR 4.550.000 each"),
               ("+ 2 nights bungalow &amp; breakfast", "IDR 5.500.000"),
               ("Open Water + Advanced pack", "IDR 9.900.000"),
               ("+ Enriched Air / Nitrox", "IDR 6.990.000")],
              "Hi!%20I%27d%20like%20to%20book%20the%20Advanced%20course.%20My%20dates%20are%3A", TRUST_DEFAULT)
    + "\n</div>\n"
    + quote("We feel like we could not have picked a better place.", "Google review &middot; one of 508 five-star reviews"),
)

# ─────────────────────────── RESCUE ───────────────────────────
pages["course-rescue.html"] = (
    "PADI Rescue Diver + EFR in Amed, Bali | Diving La Vida Loca",
    "PADI Rescue Diver course with Emergency First Response in Amed, Bali. Three days of scenario training that makes you a genuinely safer buddy. IDR 7.400.000, taxes included.",
    hero(f"{WP}/2022/09/Rescue_diver-1.webp",
         '<a href="index.html">Home</a> / <a href="index.html#courses">Courses</a> / Rescue Diver',
         "PADI Rescue Diver + EFR",
         "The course divers consistently call the most rewarding they&rsquo;ve ever done. Three days of role-play, problem-solving and scenario training, serious skills, taught with a sense of humour.")
    + facts([("3 days", "duration"), ("Age 12+", "minimum age"), ("EFR", "first aid included"), ("Scenarios", "hands-on training"), ("Max 4", "per instructor")])
    + f"""
<div class="container course-layout">
  <div class="course-content">
    <h2>What the three days look like</h2>
    <div class="day-plan">
      <div class="day"><h3>Day 1 · Emergency First Response</h3><p>CPR, first aid, bandaging, assessment, the land-based foundation, practised on each other until it&rsquo;s automatic. Useful far beyond diving.</p></div>
      <div class="day"><h3>Day 2 · Self-rescue &amp; skills</h3><p>In the pool and on the house reef: tired-diver tows, panicked-diver responses, finding a missing diver. Each skill drilled until it feels less like a test and more like a game.</p></div>
      <div class="day"><h3>Day 3 · Full scenarios</h3><p>The famous day. Our team improvises situations on the reef and you respond, expect surprises, laughter, and the quiet confidence that comes from having handled it.</p></div>
    </div>
    <h2>What&rsquo;s included</h2>
    <ul>
      <li>Emergency First Response certification (primary &amp; secondary care)</li>
      <li>All equipment, pool sessions, and ocean scenario dives</li>
      <li>PADI certification fees and digital materials</li>
      <li>Transport, coffee, tea, water and snacks</li>
      <li>10% government tax included</li>
    </ul>
    <h2>Questions divers actually ask</h2>
    <div class="faq">
      <details><summary>What are the prerequisites?</summary><p>Advanced Open Water (or Adventure Diver with the navigation dive), age 12+, and EFR training within 24 months, which is why we bundle EFR into the course.</p></details>
      <details><summary>Is it as exhausting as people say?</summary><p>It&rsquo;s the most physical course in recreational diving, and the one people talk about for years. We keep groups small so the intensity stays fun rather than stressful.</p></details>
      <details><summary>I already have a current EFR certificate.</summary><p>Then take the Rescue course alone for IDR 5.100.000 · message us and we&rsquo;ll check your certificate dates.</p></details>
    </div>
  </div>
"""
    + booking("IDR 7.400.000", "&asymp; &euro;385 &middot; Rescue + EFR &middot; all taxes &amp; equipment included",
              [("Rescue only (current EFR)", "IDR 5.100.000"),
               ("EFR only", "IDR 2.700.000"),
               ("+ 3 nights bungalow &amp; breakfast", "IDR 8.300.000")],
              "Hi!%20I%27d%20like%20to%20book%20the%20Rescue%20%2B%20EFR%20course.%20My%20dates%20are%3A", TRUST_DEFAULT)
    + "\n</div>\n"
    + quote("An authentic diving school, and I say that as a diving professional.", "Google review &middot; one of 508 five-star reviews"),
)

# ─────────────────────────── DIVEMASTER ───────────────────────────
pages["course-divemaster.html"] = (
    "PADI Divemaster Internship in Amed, Bali | Diving La Vida Loca",
    "Train as a PADI Divemaster in Amed, Bali. Up to two months embedded in a boutique dive center, real courses, real guests, real mentorship. From IDR 19.000.000.",
    hero(f"{WP}/2022/09/DiveMasterw.webp",
         '<a href="index.html">Home</a> / <a href="index.html#courses">Courses</a> / Divemaster',
         "PADI Divemaster",
         "Not a conveyor-belt internship. You&rsquo;ll be embedded in a boutique dive center for up to two months, assisting real courses, guiding real guests, and learning how a four-diver philosophy actually works.")
    + facts([("2 months", "up to"), ("Pro", "first professional rating"), ("Unlimited", "dives option"), ("1-on-1", "mentorship"), ("Real guests", "from week one")])
    + f"""
<div class="container course-layout">
  <div class="course-content">
    <h2>What you&rsquo;ll actually do</h2>
    <p>Divemaster here isn&rsquo;t shadowing from the back of a 20-person boat. With four guests maximum per trip, you&rsquo;re part of the team immediately: setting up, briefing, assisting Enric on courses, mapping sites, and eventually leading certified divers on reefs you&rsquo;ll know like your own street.</p>
    <ul>
      <li>Assist on real PADI courses from Discover Scuba to Rescue</li>
      <li>Guide fun dives across the Amed&ndash;Tulamben stretch, Liberty wreck included</li>
      <li>Workshops: dive theory, equipment, skill demonstration quality</li>
      <li>Conservation work woven in, site monitoring and cleanups are part of the job here, not an extra</li>
      <li>Spanish, Catalan, English, French or Indonesian, train in the language you&rsquo;ll work in</li>
    </ul>
    <h2>Two ways to run it</h2>
    <div class="day-plan">
      <div class="day"><h3>Standard · IDR 19.000.000</h3><p>The full Divemaster program with all training dives included, over up to two months.</p></div>
      <div class="day"><h3>Unlimited dives · IDR 26.000.000</h3><p>Same program, but every spare tank is yours. If you want to leave with 150+ dives and reef knowledge to match, this is the one.</p></div>
    </div>
    <h2>Questions candidates actually ask</h2>
    <div class="faq">
      <details><summary>What are the prerequisites?</summary><p>Rescue Diver with current EFR, 40 logged dives to start (60 to certify), a medical signed within 12 months. Not there yet? We&rsquo;ll build the path, many candidates arrive at Advanced level and do it all here.</p></details>
      <details><summary>What&rsquo;s not included?</summary><p>PADI&rsquo;s own annual fee and the Divemaster Crew Pack (manuals and materials PADI requires you to own). We&rsquo;ll quote current prices before you commit, no surprises.</p></details>
      <details><summary>Can you help with accommodation for two months?</summary><p>Yes, long-stay rates in our bungalows are part of the conversation. Message us and we&rsquo;ll put a full package together.</p></details>
    </div>
  </div>
"""
    + booking("IDR 19.000.000", "&asymp; &euro;985 &middot; full program &middot; PADI fees &amp; Crew Pack not included",
              [("Unlimited dives option", "IDR 26.000.000"),
               ("Long-stay accommodation", "ask us"),
               ("Path from Rescue level", "ask us")],
              "Hi!%20I%27m%20interested%20in%20the%20Divemaster%20program.%20Here%27s%20my%20experience%3A", TRUST_DEFAULT)
    + "\n</div>\n"
    + quote("I am happy diving and, when I get out of the water, I am happy thinking about what I have dived.", "Eduardo Admetlla &middot; Pioneer of Spanish Diving"),
)

# ─────────────────────────── SPECIALITIES ───────────────────────────
spec_cards = "".join(f"""
      <article class="eco-card">
        <span class="eco-num">{num}</span>
        <h3>{name}</h3>
        <p>{desc}</p>
        <p class="spec-price">{price}<small>{note}</small></p>
      </article>""" for num, name, desc, price, note in [
    ("01", "Enriched Air (Nitrox)", "The most popular speciality in diving: longer bottom times and shorter surface intervals. One day, with or without dives.", "IDR 2.150.000", "theory only &middot; IDR 2.900.000 with 2 dives"),
    ("02", "Deep Diving", "Four dives over two to three days, training you calmly down to 40 metres. Amed&rsquo;s walls make a perfect classroom.", "IDR 3.900.000", "4 dives &middot; age 15+"),
    ("03", "Deep + Nitrox pack", "The pairing that makes sense: dive deeper and stay longer. Two specialities in one arc.", "IDR 6.400.000", "2 days &middot; age 15+"),
    ("04", "Ultimate Diver Pack", "Advanced Open Water + Deep + Nitrox in three to four days. Arrive an Open Water diver, leave ready for almost anything.", "IDR 10.500.000", "3&ndash;4 days &middot; age 15+"),
    ("05", "Wreck Diving", "Four dives on the USAT Liberty learning lines, lights and safe penetration limits. The site does the selling.", "Ask us", "4 dives on the Liberty"),
    ("06", "Sidemount", "Two tanks, perfect trim, total streamlining. Taught by divers who actually dive sidemount, not just certify it.", "Ask us", "recreational sidemount"),
    ("07", "ReActivate Refresher", "Rusty? A half-day review in the pool, with an optional reef dive to finish. The kindest way back into the water.", "IDR 900.000", "+ 1 reef dive &middot; IDR 1.400.000"),
    ("08", "Emergency First Response", "CPR and first aid in one day, for divers, partners, parents, anyone. No dive certification needed.", "IDR 2.700.000", "1 day &middot; open to non-divers"),
])

pages["course-specialities.html"] = (
    "PADI Speciality Courses in Amed, Bali · Nitrox, Deep, Wreck, Sidemount | Diving La Vida Loca",
    "PADI speciality courses in Amed, Bali: Enriched Air Nitrox, Deep Diving, Wreck on the USAT Liberty, Sidemount, refreshers and EFR. From IDR 900.000.",
    hero(f"{WP}/2024/07/sidemount-rec-diver-3-1024x576.webp",
         '<a href="index.html">Home</a> / <a href="index.html#courses">Courses</a> / Specialities',
         "Specialities &amp; Continuing Education",
         "With a WWII wreck 25 minutes up the coast, walls dropping past 40 metres, and a house reef made for perfecting buoyancy, Amed is where speciality training stops being theoretical.")
    + f"""
<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Pick Your Path</h2></div>
    <p class="section-sub">Every speciality runs on the same rules as everything else here: four divers maximum, taught at your pace, all equipment and taxes included. Many more PADI specialities available, if you don&rsquo;t see yours, ask.</p>
    <div class="eco-grid" style="grid-template-columns: repeat(2, 1fr);">{spec_cards}
    </div>
    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hi!%20I%27m%20interested%20in%20a%20speciality%20course%3A">Ask about a speciality</a></div>
  </div>
</section>
"""
    + quote("We feel like we could not have picked a better place.", "Google review &middot; one of 508 five-star reviews"),
)

# ─────────────────────────── DIVE SITES ───────────────────────────
sites = [
    ("USAT Liberty Wreck", "Tulamben &middot; 25 min by car", f"{WP}/2022/09/Advanced_open_water.webp",
     "A 120-metre WWII cargo ship, torpedoed in 1942 and pushed into the sea by Mount Agung&rsquo;s 1963 eruption. Now it&rsquo;s the most famous shore dive on earth: walk in off the black sand, and within minutes you&rsquo;re drifting along a coral-crusted hull. Come at dawn and the resident school of bumphead parrotfish files past like commuters.",
     [("5&ndash;30 m", "depth"), ("All levels", "from Open Water"), ("Dawn", "best time")]),
    ("Jemeluk Bay", "Amed &middot; our house reef", f"{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp",
     "Calm, shallow, and absurdly generous, this is where every Open Water student takes their first reef breath, and where we keep coming back on days off. Coral gardens from three metres, a wall that drops away for the deeper dives, and the kind of macro life that turns a 45-minute dive into 70.",
     [("3&ndash;25 m", "depth"), ("All levels", "first dives welcome"), ("House reef", "our daily classroom")]),
    ("Japanese Wreck", "Banyuning &middot; 10 min by car", f"{WP}/2022/09/Open_water_padi.webp",
     "A small, coral-encrusted wreck of debated origin, sitting so shallow that snorkellers can see it, but its best secrets are for divers. The hull is completely overgrown with soft coral, and the surrounding slope hides pygmy seahorses for those with patient eyes and good buoyancy. An underrated favourite.",
     [("6&ndash;12 m", "depth"), ("All levels", "snorkellers too"), ("Macro", "pygmy seahorses")]),
    ("The Pyramids", "Amed &middot; 5 minutes away", f"{WP}/2022/09/DiveMasterw.webp",
     "Artificial reef structures stacked on the sand like sunken temples, now swarming with glassfish, lionfish and the occasional passing turtle. A brilliant second dive, a perfect navigation classroom, and proof that given a little help, the ocean rebuilds fast.",
     [("5&ndash;22 m", "depth"), ("All levels", "great second dive"), ("Turtles", "regular visitors")]),
    ("Coral Garden", "Tulamben &middot; 25 min by car", f"{WP}/2022/09/Nitrox.webp",
     "Tulamben&rsquo;s shallow sculpture garden: statues and structures laid among soft coral, all within easy reach of the surface. A photographer&rsquo;s playground, a gentle second dive, and the prettiest safety stop on the coast.",
     [("2&ndash;12 m", "depth"), ("All levels", "snorkellers too"), ("Photos", "sculpture &amp; soft coral")]),
    ("Tulamben Drop-Off", "Tulamben &middot; 25 min by car", f"{WP}/2022/09/Advanced_open_water.webp",
     "Where the lava rock falls away into deep blue. Giant fans, schooling fish along the wall, and the occasional something-big cruising past out of the depths. This is the classroom for our deep courses, and a favourite of every visiting divemaster.",
     [("10&ndash;40 m", "depth"), ("Advanced", "best enjoyed deep"), ("Wall", "fans &amp; pelagics")]),
    ("Melasti Reef", "Amed &middot; 500 m from our door", f"{WP}/2022/09/Rescue_diver-1.webp",
     "Our neighbourhood dive, literally down the path from the bungalows. A sloping coral reef with seagrass patches and resident turtles, perfect for an easy morning dive or a relaxed afternoon when you can&rsquo;t face the drive anywhere else.",
     [("4&ndash;20 m", "depth"), ("All levels", "easiest logistics"), ("Turtles", "resident")]),
    ("Seraya Secrets", "Seraya &middot; 20 min by car", f"{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp",
     "Black sand and tiny treasures. Seraya is the muck-diving icon of the coast: frogfish, harlequin shrimp, ghost pipefish, and nudibranchs by the dozen. Bring a torch, slow right down, and let Irman&rsquo;s biologist eyes find you things you&rsquo;d swim straight past.",
     [("5&ndash;20 m", "depth"), ("All levels", "macro patience helps"), ("Muck", "critter capital")]),
]
SITE_SLUG = {"USAT Liberty Wreck":"liberty","Jemeluk Bay":"jemeluk","Japanese Wreck":"japanese-wreck","The Pyramids":"pyramids","Coral Garden":"coral-garden","Tulamben Drop-Off":"drop-off","Melasti Reef":"melasti","Seraya Secrets":"seraya"}
site_rows = ""
for i, (name, kicker, img, desc, stats) in enumerate(sites):
    flip = " feature-row--flip" if i % 2 else ""
    slug = SITE_SLUG[name]
    stat_html = "".join(f'<div class="feature-stat"><strong>{a}</strong><span>{b}</span></div>' for a, b in stats)
    site_rows += f"""
    <a class="feature-row{flip} site-band" href="site-{slug}.html">
      <div class="container feature-row-grid">
        <div class="feature-img"><img src="{img}" alt="{name}" loading="lazy"></div>
        <div class="feature-body">
          <p class="feature-kicker">{kicker}</p>
          <h2><span class="site-link">{name}</span></h2>
          <p>{desc}</p>
          <div class="feature-stats">{stat_html}</div>
          <span class="feature-link">Read the full guide &rarr;</span>
        </div>
      </div>
    </a>"""

pages["dive-sites.html"] = (
    "Dive Sites in Amed & Tulamben · USAT Liberty, Jemeluk Bay & More | Diving La Vida Loca",
    "The dive sites of Amed and Tulamben, Bali: the USAT Liberty wreck, Jemeluk Bay, the Japanese Wreck and the Pyramids. All shore dives, all minutes from our door.",
    hero(f"{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp",
         '<a href="index.html">Home</a> / Dive Sites',
         "Where You&rsquo;ll Dive",
         "One volcanic coastline, strung with world-class shore dives: a WWII wreck, coral bays, walls and black-sand muck. These are the sites we dive daily and help look after.")
    + facts([("13", "named sites on our coast"), ("Shore entry", "every dive"), ("26&ndash;29&deg;C", "water all year"), ("Apr&ndash;Nov", "best visibility"), ("25 min", "drive to the Liberty")])
    + f"""
<section class="page-section map-fold">
  <div class="container">{coast_map("en")}</div>
</section>
"""
    + f"""
<section class="site-bands">{site_rows}
</section>
<section class="page-section">
  <div class="container">
    <div class="included-note">Every dive includes your guide, full equipment, transport in the Amed area, and coffee on the beach afterwards. Conditions briefing comes with every site, and if the reef is having a better day somewhere else, we&rsquo;ll tell you and go there instead. Want depths, seasons and history site by site? Read the full <a href="amed-diving-guide.html">Amed &amp; Tulamben diving guide</a>.</div>
    <div class="section-cta"><a class="section-cta-link" href="fun-dives.html">Fun dive prices &rarr;</a></div>
  </div>
</section>
"""
    + quote("The sea, once it casts its spell, holds one in its net of wonder forever.", "Jacques-Yves Cousteau"),
)

# ─────────────────────────── FUN DIVES ───────────────────────────
pages["fun-dives.html"] = (
    "Fun Dives in Amed & Tulamben, Bali · Prices & Packages | Diving La Vida Loca",
    "Guided fun dives in Amed and Tulamben from IDR 690.000 including equipment, guide and transport. Multi-day discounts, night dives and private guiding available.",
    hero(f"{WP}/2022/09/Nitrox.webp",
         '<a href="index.html">Home</a> / Fun Dives',
         "Fun Dives &amp; Prices",
         "Certified already? Give us your card and your wish list. Four divers maximum per guide, sites chosen for the day&rsquo;s conditions, and everything included, equipment, transport, and the post-dive coffee.")
    + facts([("4 max", "divers per guide"), ("All gear", "always included"), ("12+", "sites to choose"), ("5&ndash;10%", "multi-day discounts"), ("&ndash;10%", "with 5+ days")])
    + f"""
<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Simple, Honest Pricing</h2></div>
    <p class="section-sub">All prices include 10% government tax, full equipment, your guide, transport in the Amed area, and coffee, tea, water and cookies. No surcharges waiting at the till.</p>

    <div class="price-block">
      <h3>Shore Dives, Amed &amp; Tulamben</h3>
      <p class="price-block-sub">Including the USAT Liberty wreck, Jemeluk Bay, the Japanese Wreck and the Pyramids.</p>
      <div class="price-row"><span class="price-name">1 fun dive</span><span class="price-val">IDR 690.000<small>&asymp; &euro;36</small></span></div>
      <div class="price-row"><span class="price-name">2 fun dives <small>the classic day out</small></span><span class="price-val">IDR 990.000<small>&asymp; &euro;51</small></span></div>
      <div class="price-row"><span class="price-name">3 fun dives <small>dawn wreck + two more</small></span><span class="price-val">IDR 1.490.000<small>&asymp; &euro;77</small></span></div>
      <div class="price-row"><span class="price-name">Night dive</span><span class="price-val">IDR 790.000<small>&asymp; &euro;41</small></span></div>
      <div class="price-row"><span class="price-name">Private guide <small>just you and your guide</small></span><span class="price-val">+ IDR 300.000<small>per dive</small></span></div>
    </div>

    <div class="price-block">
      <h3>Dive More, Pay Less</h3>
      <p class="price-block-sub">For divers settling in for a while, minimum two dives a day.</p>
      <div class="price-row"><span class="price-name">3 or more days of diving</span><span class="price-val">5% off</span></div>
      <div class="price-row"><span class="price-name">5 or more days of diving</span><span class="price-val">10% off</span></div>
      <div class="price-row"><span class="price-name">2 dives + 1 night &amp; breakfast</span><span class="price-val">IDR 1.290.000<small>&asymp; &euro;67</small></span></div>
    </div>

    <div class="included-note">Haven&rsquo;t dived in a while? The ReActivate refresher (IDR 900.000, half a day) gets you comfortable again before your fun dives, most divers say it&rsquo;s the best money of the trip.</div>
    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hi!%20I%27d%20like%20to%20book%20fun%20dives.%20My%20dates%20and%20certification%20level%3A">Book your dives on WhatsApp</a></div>
  </div>
</section>
"""
    + quote("Welcoming, kind and helpful. An amazing experience from start to finish.", "Google review &middot; one of 508 five-star reviews"),
)

# ─────────────────────────── STAY & DIVE ───────────────────────────
pages["stay-and-dive.html"] = (
    "Stay & Dive in Amed, Bali · Bungalows + Diving Packages | Diving La Vida Loca",
    "Sleep where you dive: bungalows between the rice fields of Amed, 500 m from Melasti beach, with breakfast included. Course and fun-dive packages from IDR 1.290.000.",
    hero(f"{WP}/2022/09/Terrace-768x512.webp",
         '<a href="index.html">Home</a> / Stay &amp; Dive',
         "Stay Where You Dive",
         "Bungalows between the rice fields, five hundred metres from Melasti beach. Wake up, have breakfast on the terrace, and walk to your dive briefing, the commute is a footpath.")
    + facts([("500 m", "to the beach"), ("Breakfast", "always included"), ("Rice fields", "your neighbours"), ("On-site", "pool &amp; restaurant"), ("Packs", "course + stay deals")])
    + f"""
<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">The Place</h2></div>
    <p class="section-sub">Staying on site is what turns a course into a week with the family: breakfast with your instructor, log books on the terrace at sunset, and first pick of the dawn wreck dives. Rooms are subject to availability, tell us your dates early.</p>
    <div class="gallery-grid">
      <img src="{WP}/2022/09/Terrace-768x512.webp" alt="Bungalow terrace at Diving La Vida Loca" loading="lazy">
      <img src="{WP}/2022/09/kantor-depan-HDR-Edit-768x576.webp" alt="Diving La Vida Loca front office and grounds" loading="lazy">
      <img src="{WP}/2022/09/Meeting-room-1-768x512.webp" alt="Classroom and meeting room" loading="lazy">
    </div>

    <div style="height:3rem"></div>
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Stay &amp; Dive Packs</h2></div>
    <p class="section-sub">Accommodation packs include breakfast. All prices include 10% government tax.</p>
    <div class="price-block">
      <h3>Course + Accommodation</h3>
      <div class="price-row"><span class="price-name">Discover Scuba (2 dives) + 1 night</span><span class="price-val">IDR 1.700.000<small>&asymp; &euro;88</small></span></div>
      <div class="price-row"><span class="price-name">Open Water + 3 nights</span><span class="price-val">IDR 6.300.000<small>&asymp; &euro;325</small></span></div>
      <div class="price-row"><span class="price-name">Advanced + 2 nights</span><span class="price-val">IDR 5.500.000<small>&asymp; &euro;285</small></span></div>
      <div class="price-row"><span class="price-name">Rescue + EFR + 3 nights</span><span class="price-val">IDR 8.300.000<small>&asymp; &euro;430</small></span></div>
      <div class="price-row"><span class="price-name">2 fun dives + 1 night</span><span class="price-val">IDR 1.290.000<small>&asymp; &euro;67</small></span></div>
    </div>
    <div class="included-note">Doing the Divemaster program? Long-stay rates for up to two months are part of the package conversation, just ask.</div>
    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hi!%20I%27d%20like%20a%20stay%20%26%20dive%20pack.%20My%20dates%3A">Check availability on WhatsApp</a></div>
  </div>
</section>
"""
    + quote("We feel like we could not have picked a better place.", "Google review &middot; one of 508 five-star reviews"),
)

# ─────────────────────────── ABOUT ───────────────────────────
pages["about.html"] = (
    "About Us · Boutique Dive Center in Amed, Bali | Diving La Vida Loca",
    "A boutique Spanish-run PADI dive center in Amed, Bali. Meet the team, see the place, and learn why we never take more than four divers per trip.",
    hero(f"{WP}/2022/08/TEAM5-768x512.webp",
         '<a href="index.html">Home</a> / About',
         "Small by Choice",
         "Most dive shops grow by adding boats, benches and bookings. We grew by deciding not to. Four divers per trip is not a limitation, it&rsquo;s the entire idea.", pos="center 20%")
    + facts([("4 max", "divers per trip"), ("20+ yrs", "in the water"), ("5", "languages"), ("5.0 &#9733;", "508 Google reviews"), ("PADI", "Dive Center")])
    + f"""
<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">The Idea</h2></div>
    <div class="feature-row">
      <div class="feature-img"><img src="{WP}/2022/09/equipment-room-1-768x512.webp" alt="Equipment room at Diving La Vida Loca" loading="lazy"></div>
      <div class="feature-body">
        <p>Diving La Vida Loca is a Spanish-run PADI Dive Center set between the rice fields of Amed, five hundred metres from Melasti beach. The name is the philosophy: diving is the crazy, joyful part of life, and it deserves to be done properly.</p>
        <p>That means a private pool for every first skill. It means equipment maintained like we dive it ourselves, because we do. It means courses taught at your pace, in your language. And it means that when you come back next year (people do), someone remembers your name and how you like your coffee.</p>
      </div>
    </div>

    <div style="height:4rem"></div>
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">The Team</h2></div>
    <p class="section-sub">More than twenty years in the water between us, teaching in Spanish, Catalan, English, French, and Indonesian.</p>
    <div class="team-grid">
      <article class="team-card">
        <div class="team-photo"><img src="{WP}/2022/08/Enrik_mask1-600x900.webp" alt="Enric, PADI Master Scuba Diver Trainer" loading="lazy"></div>
        <h3 class="team-name">Enric</h3>
        <p class="team-role">Master Scuba Diver Trainer</p>
        <p class="team-bio">PADI Elite Instructor and commercial diver. He&rsquo;ll be in the pool with you on day one.</p>
      </article>
      <article class="team-card">
        <div class="team-photo"><img src="{WP}/2022/08/Irman_mask_1-600x900.webp" alt="Irman, Divemaster and biologist" loading="lazy"></div>
        <h3 class="team-name">Irman</h3>
        <p class="team-role">Divemaster &middot; Biologist</p>
        <p class="team-bio">Knows every critter on the reef by name, the Latin one and the local one.</p>
      </article>
      <article class="team-card">
        <div class="team-photo"><img src="{WP}/2022/08/NENGAH_mod_2.webp" alt="Nengah, front office" loading="lazy"></div>
        <h3 class="team-name">Nengah</h3>
        <p class="team-role">Front Office</p>
        <p class="team-bio">The first smile you&rsquo;ll see, and the person who makes everything run on time.</p>
      </article>
    </div>

    <div style="height:4rem"></div>
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">The Place</h2></div>
    <p class="section-sub">Have a look around before you arrive, the pool, the equipment room, the classroom, the terrace.</p>
    <div class="gallery-grid">
      <img src="{WP}/2022/09/equipment-room-2-768x512.webp" alt="Dive equipment room" loading="lazy">
      <img src="{WP}/2022/09/Clean_equipment-768x512.webp" alt="Clean, maintained dive equipment" loading="lazy">
      <img src="{WP}/2022/09/Meeting-room-1-768x512.webp" alt="Course classroom" loading="lazy">
      <img src="{WP}/2022/09/front-office-768x512.webp" alt="Front office" loading="lazy">
      <img src="{WP}/2022/09/car-1-768x512.webp" alt="Dive transport" loading="lazy">
      <img src="{WP}/2022/09/Terrace-768x512.webp" alt="Guest terrace" loading="lazy">
    </div>
    <div class="section-cta"><a class="section-cta-link" href="conservation.html">Our conservation work &rarr;</a></div>
  </div>
</section>
"""
    + quote("An authentic diving school, and I say that as a diving professional.", "Google review &middot; one of 508 five-star reviews"),
)

# ─────────────────────────── CONSERVATION ───────────────────────────
pages["conservation.html"] = (
    "Reef Conservation in Amed, Bali · Diving La Vida Loca | Diving La Vida Loca",
    "Conservation at Diving La Vida Loca: reef-first dive training, cleanups and site monitoring, and a boutique model that keeps pressure off Amed's reefs.",
    hero(f"{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp",
         '<a href="index.html">Home</a> / Conservation',
         "We Don&rsquo;t Just Dive Here.<br>We Look After Here.",
         "Amed&rsquo;s reefs are our workplace, our classroom, and our home. Conservation isn&rsquo;t a page on our website, it&rsquo;s how every briefing starts and how every dive is led.")
    + f"""
<section class="page-section">
  <div class="container">
    <div class="feature-row">
      <div class="feature-img"><img src="{WP}/2024/07/GOPR9425-768x1024.webp" alt="Buoyancy training in the pool" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">01 &middot; Reef-first training</p>
        <h2>The kindest thing a diver can learn is buoyancy</h2>
        <p>Every diver we certify leaves knowing how to enjoy a reef without touching it. Perfect buoyancy isn&rsquo;t a speciality here, it&rsquo;s the foundation of every course, drilled in the pool before anyone meets coral. Four divers per instructor means nobody&rsquo;s fins go unwatched.</p>
      </div>
    </div>
    <div class="feature-row feature-row--flip">
      <div class="feature-img"><img src="{WP}/2022/09/Clean_equipment-768x512.webp" alt="Care and maintenance at the dive center" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">02 &middot; Hands in the water</p>
        <h2>Cleanups, monitoring, and paying attention</h2>
        <p>We dive these sites every day, which makes us their early-warning system. Reef and beach cleanups, keeping an eye on coral health through the seasons, and raising the alarm when something changes. Ask us what&rsquo;s happening on the reef this season, we&rsquo;ll talk your ear off.</p>
      </div>
    </div>
    <div class="feature-row">
      <div class="feature-img"><img src="{WP}/2022/08/TEAM5-768x512.webp" alt="The Diving La Vida Loca team" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">03 &middot; Part of Amed</p>
        <h2>A reef economy works when everyone wins</h2>
        <p>We&rsquo;re a small team rooted in this village, working alongside the local community that depends on a healthy reef as much as we do. Keeping groups tiny isn&rsquo;t just better diving, it&rsquo;s less pressure on the sites everyone here lives from.</p>
      </div>
    </div>
    <div class="included-note">Want to help while you&rsquo;re here? Join a cleanup dive, take the Peak Performance Buoyancy speciality, or just ask Irman to show you the reef through a biologist&rsquo;s eyes, it changes how you dive forever.</div>
    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hi!%20I%27d%20like%20to%20join%20a%20cleanup%20or%20conservation%20dive%3A">Join a conservation dive</a></div>
  </div>
</section>
"""
    + quote("People protect what they love.", "Jacques-Yves Cousteau"),
)

# ─────────────────────────── CONTACT ───────────────────────────
pages["contact.html"] = (
    "Contact Diving La Vida Loca · Amed, Bali | WhatsApp & Enquiries",
    "Contact Diving La Vida Loca in Amed, Bali. WhatsApp +62 821 4553 8716, Instagram, Facebook, or send an enquiry. 500 m from Melasti beach.",
    hero(f"{WP}/2022/09/kantor-depan-HDR-Edit-768x576.webp",
         '<a href="index.html">Home</a> / Contact',
         "Say Hola",
         "WhatsApp is fastest: we usually answer within the hour. Tell us your dates, your certification level (or none at all), and what you&rsquo;re dreaming about. We&rsquo;ll shape the rest around you.")
    + f"""
<section class="page-section">
  <div class="container contact-grid">
    <div>
      <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Find Us</h2></div>
      <ul class="contact-list">
        <li><strong>WhatsApp</strong><a href="{WA}">+62 821 4553 8716</a></li>
        <li><strong>Instagram</strong><a href="https://www.instagram.com/diving.lavidaloca">@diving.lavidaloca</a></li>
        <li><strong>Facebook</strong><a href="https://www.facebook.com/Divinglavidaloca">Diving La Vida Loca</a></li>
        <li><strong>Where</strong>Amed, Karangasem, Bali, between the rice fields, 500 m from Melasti beach</li>
      </ul>
      <a class="pill-btn pill-btn--whatsapp" href="{WA}">Chat on WhatsApp</a>
      <div class="map-embed">
        <iframe title="Map of Amed, Bali" src="https://www.openstreetmap.org/export/embed.html?bbox=115.63,-8.37,115.71,-8.31&amp;layer=mapnik&amp;marker=-8.34,115.67" loading="lazy"></iframe>
      </div>
      <p class="map-attrib">Map &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</p>
    </div>
    <div class="form-card">
      <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Or Write to Us</h2></div>
      <form id="enquiry-form">
        <div class="form-field"><label for="f-name">Name</label><input id="f-name" type="text" placeholder="Your name"></div>
        <div class="form-field"><label for="f-email">Email</label><input id="f-email" type="email" placeholder="you@example.com"></div>
        <div class="form-field"><label for="f-course">I&rsquo;m interested in</label>
          <select id="f-course">
            <option>Discover Scuba Diving</option>
            <option>PADI Open Water</option>
            <option>Advanced Open Water</option>
            <option>Rescue Diver + EFR</option>
            <option>Divemaster</option>
            <option>Specialities</option>
            <option>Fun dives</option>
            <option>Stay &amp; dive package</option>
          </select>
        </div>
        <div class="form-field"><label for="f-dates">Dates</label><input id="f-dates" type="text" placeholder="e.g. 12&ndash;18 August"></div>
        <div class="form-field"><label for="f-msg">Message</label><textarea id="f-msg" rows="4" placeholder="Certification level, group size, dreams&hellip;"></textarea></div>
        <button class="pill-btn" type="submit">Send via WhatsApp</button>
      </form>
    </div>
  </div>
</section>
""",
)


# ─────────────────────────── DIVING GUIDE ───────────────────────────
guide_sites_en = """
    <div class="feature-row" id="liberty">
      <div class="feature-img"><img src="{WP}/2022/09/Advanced_open_water.webp" alt="Divers on the USAT Liberty wreck, Tulamben" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">The flagship &middot; Tulamben</p>
        <h2><a href="site-liberty.html" class="site-link">USAT Liberty Wreck</a></h2>
        <p>The Liberty is the reason most divers have heard of this coast. A 120-metre US Army transport ship, she was torpedoed by a Japanese submarine in January 1942 while crossing the Lombok Strait, towed towards Bali, and beached at Tulamben. There she sat for twenty years, until the tremors of Mount Agung&rsquo;s 1963 eruption pushed her off the sand and into the water, where the ocean got to work.</p>
        <p>Today she lies on a black-sand slope between roughly 5 and 30 metres, completely colonised by hard and soft coral. You can snorkel her shallowest sections; an Open Water diver sees most of her; an Advanced diver gets the stern and the deeper swim-throughs. The resident school of bumphead parrotfish patrols at first light, with jacks, barracuda and garden eels on the slope.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>5&ndash;30 m</strong><span>depth</span></div><div class="feature-stat"><strong>All levels</strong><span>snorkellers too</span></div><div class="feature-stat"><strong>Dawn</strong><span>bumpheads &amp; empty wreck</span></div></div>
      </div>
    </div>
    <div class="included-note">How we dive it: the Liberty receives day-trippers from south Bali from mid-morning. Staying in Amed, we&rsquo;re in the water at sunrise, before the first buses arrive, with four divers at most. You get the wreck, the bumpheads, and the silence.</div>

    <div class="feature-row feature-row--flip" id="jemeluk">
      <div class="feature-img"><img src="{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp" alt="Coral reef in Jemeluk Bay, Amed" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">Our house reef &middot; Amed</p>
        <h2><a href="site-jemeluk.html" class="site-link">Jemeluk Bay &amp; the Amed Wall</a></h2>
        <p>Jemeluk is the bay the village curls around: calm, shallow coral gardens from three metres, sloping to a wall that falls away past 25 metres at its eastern point. It&rsquo;s where every Open Water student takes their first sea breaths, and the snorkelling is good enough that non-diving partners don&rsquo;t feel left out. Expect anthias clouds, octopus if you look slowly, and the underwater post box the tourists love.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>3&ndash;25 m</strong><span>depth</span></div><div class="feature-stat"><strong>All levels</strong><span>first dives welcome</span></div><div class="feature-stat"><strong>House reef</strong><span>our daily classroom</span></div></div>
      </div>
    </div>

    <div class="feature-row" id="japanese-wreck">
      <div class="feature-img"><img src="{WP}/2022/09/Open_water_padi.webp" alt="Soft coral on the Japanese wreck, Banyuning" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">The shallow secret &middot; Banyuning</p>
        <h2><a href="site-japanese-wreck.html" class="site-link">Japanese Wreck</a></h2>
        <p>A small steel vessel from WWII lying improbably shallow, between roughly 2 and 12 metres, close enough to the surface that snorkellers float over it. Don&rsquo;t let the depth fool you: the hull is smothered in soft coral, and the reef slope beside it drops away with gorgonians that hide pygmy seahorses. Long, shallow, colour-saturated dives with huge bottom time, and a photographer&rsquo;s favourite.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>2&ndash;12 m</strong><span>the wreck itself</span></div><div class="feature-stat"><strong>All levels</strong><span>epic bottom time</span></div><div class="feature-stat"><strong>Macro</strong><span>pygmy seahorses nearby</span></div></div>
      </div>
    </div>

    <div class="feature-row feature-row--flip" id="pyramids">
      <div class="feature-img"><img src="{WP}/2022/09/DiveMasterw.webp" alt="Divers over reef structures in Amed" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">Two more Amed regulars</p>
        <h2><a href="site-pyramids.html" class="site-link">The Pyramids</a> &amp; <a href="site-melasti.html" class="site-link">Melasti Reef</a></h2>
        <p>The Pyramids are tiered artificial-reef structures seeded on the sand off Amed beach, a few minutes along from Jemeluk, now two decades grown and swarming with glassfish, lionfish and passing turtles: a brilliant second dive and our navigation classroom. Melasti is the reef at the end of our own path, a gentle slope of coral and seagrass with resident turtles, perfect when you want an easy morning with zero logistics.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>5&ndash;22 m</strong><span>Pyramids</span></div><div class="feature-stat"><strong>4&ndash;20 m</strong><span>Melasti</span></div><div class="feature-stat"><strong>500 m</strong><span>Melasti from our door</span></div></div>
      </div>
    </div>

    <div class="feature-row" id="coral-garden">
      <div class="feature-img"><img src="{WP}/2022/09/Nitrox.webp" alt="Diver at Coral Garden, Tulamben" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">Tulamben&rsquo;s other two</p>
        <h2><a href="site-coral-garden.html" class="site-link">Coral Garden</a> &amp; the <a href="site-drop-off.html" class="site-link">Drop-Off</a></h2>
        <p>Coral Garden is Tulamben&rsquo;s shallow gallery: statues and structures laid among soft coral at 2&ndash;12 metres, busy with life and ideal for long, relaxed dives and the prettiest safety stops on the coast. Ten minutes&rsquo; walk along the beach, the Drop-Off (locals call it The Wall) is the opposite mood: volcanic rock plunging from 10 metres to beyond 40, hung with giant gorgonians, schooling fish stacked against the wall, and the occasional something-big cruising out of the blue. It&rsquo;s where our deep training happens.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>2&ndash;12 m</strong><span>Coral Garden</span></div><div class="feature-stat"><strong>10&ndash;40 m</strong><span>Drop-Off</span></div><div class="feature-stat"><strong>Advanced</strong><span>for the wall&rsquo;s best</span></div></div>
      </div>
    </div>

    <div class="feature-row feature-row--flip" id="seraya">
      <div class="feature-img"><img src="{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp" alt="Macro life on black sand at Seraya" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">For the critter hunters &middot; Seraya</p>
        <h2><a href="site-seraya.html" class="site-link">Seraya Secrets</a></h2>
        <p>A few minutes before Tulamben on the coast road, Seraya is the muck-diving icon of east Bali: a featureless-looking black-sand slope that rewards slow eyes with frogfish, harlequin shrimp, ghost pipefish, seahorses and nudibranchs by the dozen. It&rsquo;s a different discipline, hovering still, searching small, and with Irman&rsquo;s biologist eyes along, it ruins ordinary reef dives forever, in the best way.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>5&ndash;20 m</strong><span>depth</span></div><div class="feature-stat"><strong>All levels</strong><span>buoyancy helps</span></div><div class="feature-stat"><strong>Muck</strong><span>critter capital</span></div></div>
      </div>
    </div>
"""

pages["amed-diving-guide.html"] = (
    "Amed & Tulamben Diving Guide · Every Dive Site, Honestly Rated | Diving La Vida Loca",
    "The complete guide to diving Amed and Tulamben, Bali: the USAT Liberty wreck's history and depths, Jemeluk, the Japanese Wreck, Seraya muck diving, conditions month by month, written by the dive center that dives them daily.",
    hero(f"{WP}/2022/09/Advanced_open_water.webp",
         '<a href="index.html">Home</a> / <a href="blog.html">Blog</a> / Diving Guide',
         "The Amed &amp; Tulamben Diving Guide",
         "Everything we know about the coast we dive every day: the Liberty&rsquo;s story, real depths, who each site suits, when to come, and the local tricks that make the difference. No site sold harder than it deserves.")
    + facts([("13", "sites in this guide"), ("Shore entry", "every single dive"), ("26&ndash;29&deg;C", "water all year"), ("15&ndash;30 m", "dry-season visibility"), ("Apr&ndash;Nov", "prime season")])
    + f"""
<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Why This Coast Is Special</h2></div>
    <p class="section-sub">The short coastal stretch between Amed and Tulamben packs a world-famous wreck, coral bays, a plunging wall and black-sand muck diving, all entered on foot from the beach. No boats, no long rides: you wade in, descend, and you&rsquo;re there. Mount Agung&rsquo;s volcanic sand makes the coral colours pop and feeds the macro life the area is famous for.</p>
{guide_sites_en.replace("{{WP}}".replace("{{","{").replace("}}","}"), WP)}


  </div>
</section>

<section class="more-sites">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">More Sites We Dive</h2></div>
    <p class="section-sub">The eight above are the heart of the coast; these five round out the map for divers staying longer or chasing something specific.</p>
    <div class="day-plan">
      <div class="day" id="boga"><h3><a href="site-boga.html" class="site-link">Boga Wreck &middot; Kubu &middot; 16&ndash;40 m</a></h3><p>A 40-metre cargo vessel purpose-sunk in 2012 as an artificial reef, ten minutes past Tulamben. She sits upright with statues on deck and a famously surreal sunken car, but her depth makes this an Advanced dive, ideally on Nitrox.</p></div>
      <div class="day" id="batu-kelebit"><h3><a href="site-batu-kelebit.html" class="site-link">Batu Kelebit &middot; Tulamben &middot; 15&ndash;40 m</a></h3><p>Rocky ridges running into deep water just east of the Drop-Off: big gorgonians, schooling fish, the coast&rsquo;s best chance of something pelagic cruising past. Tulamben&rsquo;s wilder edge, best with some experience.</p></div>
      <div class="day" id="bunutan"><h3><a href="site-bunutan.html" class="site-link">Bunutan &middot; Amed &middot; 10&ndash;30 m</a></h3><p>A sandy point on the Amed strip with garden eel colonies, seagrass patches and a gentle deep slope, often dived as an easy drift. Quietly excellent, and usually empty.</p></div>
      <div class="day" id="lipah"><h3><a href="site-lipah.html" class="site-link">Lipah Bay &middot; Amed &middot; 3&ndash;20 m</a></h3><p>A small bay of coral bommies on sand, relaxed and shallow, as good for snorkellers as divers. A classic easy second dive on the way back from the Japanese Wreck.</p></div>
      <div class="day" id="gili-selang"><h3><a href="site-gili-selang.html" class="site-link">Gili Selang &middot; Bali&rsquo;s eastern tip &middot; 5&ndash;30 m</a></h3><p>The little islet off Bali&rsquo;s easternmost point: pristine coral and real pelagic potential, guarded by strong, unpredictable currents. Advanced divers only, on the right day, with the right plan. Ask us.</p></div>
    </div>
  </div>
</section>

<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">When to Come</h2></div>
    <p class="section-sub">Amed dives all year. The dry season, April to November, brings the best visibility (often 15&ndash;30 metres) and glassy mornings; the rainy season is quieter, warmer-aired and still very diveable, with visibility that varies day to day. Water sits between 26 and 29&deg;C whatever the month, a 3 mm suit is plenty. Mornings are almost always the best conditions of the day, which suits the way we run things anyway.</p>

    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Good to Know</h2></div>
    <p class="section-sub">Entries are over black sand and pebbles, so booties are standard kit (ours are included, like everything else). Currents on this coast are generally gentle, which is why it&rsquo;s such a good place to learn. And the reef etiquette matters to us: perfect buoyancy before big cameras, nothing touched, nothing chased. The reef pays everyone&rsquo;s wages here.</p>

    <h2 style="font-size:1.5rem; margin:2.5rem 0 1.2rem;">Questions divers ask about this coast</h2>
    <div class="faq">
      <details><summary>Can beginners dive the Liberty wreck?</summary><p>Yes. The wreck starts around 5 metres, so Open Water divers, and even snorkellers, see plenty. The deeper stern and swim-throughs are the reason most people pair it with the Advanced course.</p></details>
      <details><summary>What is the best time of day for the Liberty?</summary><p>First light, without question. The bumphead parrotfish are still patrolling, the day-trip crowds from south Bali haven&rsquo;t arrived, and the light through the superstructure is the photo you came for. Staying in Amed makes this easy.</p></details>
      <details><summary>Is there current in Amed and Tulamben?</summary><p>Generally mild, which is why the coast is ideal for courses and relaxed diving. Conditions change day to day, and we brief honestly every morning. If a site is having a bad day, we go to a better one.</p></details>
      <details><summary>Do I need a boat for any of these sites?</summary><p>No. Every site in this guide is a shore entry, that is the magic of this coast. You walk in off the beach with your guide, maximum four divers.</p></details>
      <details><summary>When is whale or mola season in Amed?</summary><p>Amed is not a mola or pelagic destination, that is Nusa Penida&rsquo;s game. What this coast does better than almost anywhere: wrecks, healthy shallow coral, macro life and easy, beautiful diving you can do three times a day.</p></details>
    </div>

    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hi!%20I%20read%20your%20diving%20guide.%20My%20dates%20and%20level%3A">Plan your dives with us</a></div>
  </div>
</section>
"""
    + quote("The sea, once it casts its spell, holds one in its net of wonder forever.", "Jacques-Yves Cousteau"),
)


# ─────────────────────────── BLOG ───────────────────────────
pages["blog.html"] = (
    "The Diving La Vida Loca Blog · Guides &amp; Stories from Amed, Bali",
    "Diving guides, dive-site deep-dives and stories from Amed and Tulamben, Bali, written by the team that dives this coast every day.",
    hero(f"{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp",
         '<a href="index.html">Home</a> / Blog',
         "The Blog",
         "Guides, dive-site deep-dives and stories from the coast we dive every day. Written by us, in plain language, with nothing sold harder than it deserves.")
    + facts([("Local", "stories &amp; guides"), ("Written", "by our divers"), ("Conservation", "front and centre"), ("Updated", "through 2026"), ("Honest", "no fluff")])
    + f"""
<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Latest</h2></div>
    <div class="blog-grid">
      <article class="blog-card">
        <a class="blog-card-img" href="blog-karangasem-mpa.html"><img src="{WP}/2022/09/Nitrox.webp" alt="Coral reef inside the Karangasem Marine Protected Area, Amed" loading="lazy"></a>
        <div class="blog-card-body">
          <p class="blog-card-cat">Conservation</p>
          <h2><a href="blog-karangasem-mpa.html">Inside the Karangasem Marine Protected Area</a></h2>
          <p>The conservation zone that now covers Amed, Seraya, Tulamben and the Liberty wreck: its no-take core zones, who looks after it in 2026, and what it changes about diving this coast.</p>
          <a class="blog-card-link" href="blog-karangasem-mpa.html">Read the article &rarr;</a>
        </div>
      </article>
      <article class="blog-card">
        <a class="blog-card-img" href="blog-reef-health-2026.html"><img src="{WP}/2022/09/Rescue_diver-1.webp" alt="Healthy coral and reef fish on a shallow reef in Amed, Bali" loading="lazy"></a>
        <div class="blog-card-body">
          <p class="blog-card-cat">Conservation</p>
          <h2><a href="blog-reef-health-2026.html">How Amed&rsquo;s Reefs Are Doing in 2026</a></h2>
          <p>A straight look at warm-water stress and bleaching watch on this coast, NOAA&rsquo;s 2026 monitoring, and the restoration and Green Fins work putting coral back, reef by reef.</p>
          <a class="blog-card-link" href="blog-reef-health-2026.html">Read the article &rarr;</a>
        </div>
      </article>
      <article class="blog-card">
        <a class="blog-card-img" href="amed-diving-guide.html"><img src="{WP}/2022/09/Advanced_open_water.webp" alt="Diver on the USAT Liberty wreck, Tulamben" loading="lazy"></a>
        <div class="blog-card-body">
          <p class="blog-card-cat">Dive Guide</p>
          <h2><a href="amed-diving-guide.html">The Amed &amp; Tulamben Diving Guide</a></h2>
          <p>Every dive site on our coast, honestly rated: the Liberty&rsquo;s story and real depths, who each site suits, when to come, and the local tricks that make the difference.</p>
          <a class="blog-card-link" href="amed-diving-guide.html">Read the guide &rarr;</a>
        </div>
      </article>
    </div>
    <p class="section-sub" style="margin-top:2.4rem;">More guides and stories from the coast are on the way. Follow us on <a href="https://www.instagram.com/diving.lavidaloca">Instagram</a> for the latest from underwater.</p>
  </div>
</section>
""",
)


# ─────────────────────────── BLOG POST: KARANGASEM MPA ───────────────────────────
pages["blog-karangasem-mpa.html"] = (
    "Inside the Karangasem Marine Protected Area · Diving Amed &amp; Tulamben Responsibly | Diving La Vida Loca",
    "What the Karangasem Marine Protected Area means for divers in Amed and Tulamben, Bali: the 5,478-hectare zone covering Amed, Seraya, Tulamben and the USAT Liberty, its no-take core areas, who manages it in 2026, and the simple rules every diver follows.",
    hero(f"{WP}/2022/09/Nitrox.webp",
         '<a href="index.html">Home</a> / <a href="blog.html">Blog</a> / Karangasem Marine Protected Area',
         "Inside the Karangasem Marine Protected Area",
         "The coast we dive every day is now a protected one, on paper and, increasingly, in the water. Here is what that actually means when you descend on the Liberty or drift along the Amed wall.")
    + facts([("5,478 ha", "total protected area"), ("Tulamben&ndash;Padangbai", "coastline covered"), ("179 ha", "core no-take zone"), ("2023", "declared"), ("2026", "now Province-managed")])
    + f"""
<section class="page-section article">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">A Protected Coast, on Paper and in the Water</h2></div>
    <p class="section-sub">In July 2023 the Indonesian Ministry of Marine Affairs and Fisheries formally declared the Karangasem Marine Protected Area, a conservation zone of more than 5,478 hectares running along Bali&rsquo;s northeast coastline from Tulamben down to Padangbai. On the map it is designated a <em>Taman di Perairan</em>, a marine park, created to protect coral reefs, reef fish and wider marine biodiversity while keeping space for sustainable tourism and the traditional fishing this coast has always depended on.</p>
    <p class="section-sub">For those of us who dive here daily, the declaration put a legal frame around something we already felt: this is a special, and a fragile, stretch of sea. Every site we guide, from the Boga Wreck at Kubu to Gili Selang at Bali&rsquo;s eastern tip, sits inside or alongside this zone.</p>

    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">The Zones, and Why They Matter to You</h2></div>
    <p class="section-sub">The MPA is not a single rope-line. It is split into four main regions, each managed differently. Tulamben covers roughly 1,308 hectares and includes the USAT Liberty, the 120-metre wreck most visitors come to Bali to dive. The Amed and Seraya stretch is the largest at over 2,200 hectares and holds a 179-hectare core conservation zone where diving and fishing are both off-limits, left completely alone so coral and fish can recover on their own terms. Candidasa adds around 1,755 hectares further southwest, and Padangbai contributes a small 12-hectare rehabilitation zone.</p>
    <p class="section-sub">Across those regions, three kinds of zone do the work. Core conservation areas prohibit all extractive activity, no fishing, no collecting, often no diving at all. Sustainable-use zones, which is where most diving happens, allow guided diving and traditional fishing under eco-friendly guidelines. Rehabilitation zones are living laboratories, set aside for coral planting and habitat restoration. Knowing which zone you are in is part of a good briefing, and it is why we will sometimes tell you a particular patch of reef is simply not ours to enter.</p>

    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Who Looks After It in 2026</h2></div>
    <p class="section-sub">Management of the marine park now sits with the Bali Provincial Government, which has taken over day-to-day oversight of the area. As with most young MPAs, the paper protections are ahead of enforcement on the water, and the honest truth is that a zone this size is only as protected as the operators and fishers who choose to respect it. That is exactly where dive centres come in. A boat that drops anchor on coral, or a group of forty divers kicking up a reef, undoes a lot of what a decree is trying to achieve.</p>

    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">What It Means for How We Dive</h2></div>
    <p class="section-sub">The rules the MPA asks of divers are not complicated, and they are the same things good diving has always asked for: respect the designated zones, keep your buoyancy under control, never touch or stand on coral, use reef-safe sunscreen, and carry your plastic back out with you. None of that is a hardship. It is just diving done with attention.</p>
    <p class="section-sub">It is also, more or less, our whole model. We keep groups to a maximum of four divers per guide, which means nobody&rsquo;s fins go unwatched and we can actually steer people away from contact before it happens. We drill buoyancy in the pool before anyone meets a reef. We dive from the shore, so there are no anchors going down on coral. And because we live here, the health of these reefs is not an abstraction to us, it is our workplace, our classroom and our home. The MPA did not change how we dive. It just gave a name to why we have always dived this way.</p>

    <h2 style="font-size:1.5rem; margin:2.5rem 0 1.2rem;">Questions divers ask about the MPA</h2>
    <div class="faq">
      <details><summary>Can I still dive the USAT Liberty inside the MPA?</summary><p>Yes. The Liberty sits in the Tulamben region of the marine park, in a zone that permits guided diving. The protection is about how the site is used, not about closing it. We dive it at first light with a maximum of four divers, before the day-trip crowds arrive.</p></details>
      <details><summary>Are there areas I am not allowed to dive?</summary><p>Yes. The Amed and Seraya stretch contains a 179-hectare core no-take zone where diving and fishing are prohibited so the reef can recover undisturbed. Your guide will know the boundaries and plan around them.</p></details>
      <details><summary>Is there an MPA entry fee?</summary><p>Arrangements for marine-park fees on this coast are still settling as the Provincial Government takes over management. If a conservation or site fee applies on the day, we will always tell you up front, with no surprises.</p></details>
      <details><summary>Does the MPA mean the reefs are fully protected now?</summary><p>It is a strong start, but enforcement across a 5,478-hectare zone takes time and resources. In practice the reefs are protected by the everyday choices of divers, guides and fishers. That is why low-impact, small-group diving matters more here, not less.</p></details>
    </div>

    <div class="included-note">Want the site-by-site detail? Our <a href="amed-diving-guide.html">Amed and Tulamben diving guide</a> walks the whole coast, depths, conditions and all, and our <a href="conservation.html">conservation page</a> explains how we keep our own footprint small.</div>
    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hi!%20I%27d%20like%20to%20dive%20Amed%20with%20a%20low-impact%20centre.%20My%20dates%3A">Dive this coast with us</a></div>
  </div>
</section>
"""
    + quote("In the end we will conserve only what we love, we will love only what we understand.", "Baba Dioum"),
)


# ─────────────────────────── BLOG POST: REEF HEALTH 2026 ───────────────────────────
pages["blog-reef-health-2026.html"] = (
    "How Amed&rsquo;s Reefs Are Doing in 2026 · Heat, Bleaching Watch &amp; Restoration | Diving La Vida Loca",
    "An honest 2026 update on reef health in Amed and Tulamben, Bali: warm-water stress and NOAA bleaching watch, what coral bleaching really is, the coast's history of heat events, and the restoration and Green Fins work putting coral back.",
    hero(f"{WP}/2022/09/Rescue_diver-1.webp",
         '<a href="index.html">Home</a> / <a href="blog.html">Blog</a> / Amed Reef Health 2026',
         "How Amed&rsquo;s Reefs Are Doing in 2026",
         "No spin, no doom. Here is a straight read on the state of the reefs we dive, the warm-water risk we watch every dry season, and the people quietly putting coral back on this coast.")
    + facts([("26&ndash;30&deg;C", "water on this coast"), ("NOAA", "monitors Bali heat stress"), ("~55,000", "restoration structures nearby"), ("Green Fins", "the standard we dive to")])
    + f"""
<section class="page-section article">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">The Honest Picture</h2></div>
    <p class="section-sub">Amed and Tulamben are, by Bali standards, in good shape. Shore-entry reefs, gentle currents and volcanic sand that feeds an extraordinary amount of macro life all add up to a coast that still rewards a diver hugely. But healthy is not the same as safe, and the single biggest thing we keep an eye on is heat. Warm water is what stresses coral, and a hot, still dry season is exactly the kind of weather that puts reefs under pressure.</p>
    <p class="section-sub">That is not guesswork. NOAA&rsquo;s Coral Reef Watch programme runs satellite heat-stress monitoring for the East Java and Bali region, and through 2026 it continues to track sea-surface temperatures and bleaching risk for our part of the world. Water on this coast usually sits between 26 and 30 degrees, and it is the upper end of that range, held for weeks, that we worry about.</p>

    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">What Bleaching Actually Is</h2></div>
    <p class="section-sub">Coral is an animal living in partnership with tiny algae that live inside its tissue and give it both its colour and most of its food. When water stays too warm for too long, the coral expels those algae and turns bone-white. That is bleaching. A bleached coral is not yet a dead coral: if the heat passes quickly enough, the algae return and the colony recovers over weeks or months. If the heat lingers, the coral starves, becomes prone to disease, and can die, after which the reef can tip toward an algae-dominated state that takes years, sometimes decades, to come back. This is why a single bad season matters, and why every degree and every week counts.</p>

    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">History on This Coast</h2></div>
    <p class="section-sub">This is not new for Bali. Back in 2009, a Reef Check survey along the north coast found Amed had been hit hardest in that event, with around 40 percent of hard coral bleached, while Tulamben came off lightest at roughly 10 percent, with water temperatures recorded between 29 and 30 degrees at the time. Go further back and the 1997 to 1998 global event was far worse, with parts of Bali losing enormous coral cover. We share these numbers not to alarm you but because the pattern is the point: this coast has bleached before, it has also recovered before, and which way a given season goes depends a lot on how warm the water gets and how much extra stress we humans pile on top.</p>

    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Putting Coral Back</h2></div>
    <p class="section-sub">The hopeful half of the story is restoration, and northeast Bali has become one of the busiest places in Indonesia for it. North Bali Reef Conservation, founded in 2017, has grown into one of the country&rsquo;s largest reef-restoration efforts, with roughly 55,000 artificial structures deployed by the start of 2026 across sites that include the Tulamben area near us. Visitors can join their multi-day coral courses, from a few days to several weeks, learning coral farming, restoration and reef ecology hands-on. It is some of the most rewarding diving you can do on this coast, and it is the kind of work the MPA&rsquo;s rehabilitation zones are designed for.</p>

    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Green Fins, and How We Dive</h2></div>
    <p class="section-sub">The other quiet shift is in how dive centres themselves operate. Green Fins is the international environmental standard for diving and snorkelling operators, run with the UN Environment Programme, and through 2026 more Karangasem centres have been passing its assessments, with the best earning Gold member status. It measures the unglamorous things that actually protect reefs: briefings, buoyancy standards, waste and chemical handling, group sizes, anchoring.</p>
    <p class="section-sub">That list will sound familiar if you have read this far, because it is how we already run. Four divers per guide. Buoyancy drilled in the pool before anyone meets coral. Shore entries, so no anchors on the reef. Cleanups when we see rubbish, and an honest briefing every morning about what the sea is doing that day. None of it makes a dramatic photo. All of it is what keeps a reef worth photographing in the first place.</p>

    <h2 style="font-size:1.5rem; margin:2.5rem 0 1.2rem;">Questions divers ask about reef health here</h2>
    <div class="faq">
      <details><summary>Are Amed&rsquo;s reefs bleached right now?</summary><p>Bleaching risk rises and falls with water temperature through the season, which is why NOAA monitors it. Conditions vary year to year and even site to site. We brief honestly every morning on what we are actually seeing underwater, and if one reef is having a bad spell we will take you to a healthier one.</p></details>
      <details><summary>Is it still worth diving here if reefs are under stress?</summary><p>Absolutely, and responsible diving is part of the solution, not the problem. Visiting with a low-impact centre supports a reef economy that gives these sites real value alive. Just choose your operator with care.</p></details>
      <details><summary>Can I dive on a coral restoration project?</summary><p>Yes. Restoration courses run on this coast, and they are some of the most meaningful dives you can do. Ask us and we will point you in the right direction.</p></details>
      <details><summary>What is the one thing I can do to help?</summary><p>Master your buoyancy and keep your hands to yourself. A diver who never touches the reef, never kicks up sediment and never chases the wildlife is already doing the most important thing. Reef-safe sunscreen and taking your plastic home come a close second.</p></details>
    </div>

    <div class="included-note">More on our own approach is on the <a href="conservation.html">conservation page</a>, and the full site-by-site picture is in the <a href="amed-diving-guide.html">Amed and Tulamben diving guide</a>.</div>
    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hi!%20I%27d%20love%20to%20dive%20Amed%20responsibly.%20Tell%20me%20more%3A">Dive Amed, the careful way</a></div>
  </div>
</section>
"""
    + quote("The sea, once it casts its spell, holds one in its net of wonder forever.", "Jacques-Yves Cousteau"),
)


# ─────────────────────────── TRIP BUILDER ───────────────────────────
pages["plan-your-trip.html"] = (
    "Tailor Your Dive Trip in Amed, Bali · Instant Estimate | Diving La Vida Loca",
    "Answer three questions and get an instant estimate for your diving in Amed, Bali: courses, fun dives, stay & dive packs. Real prices, no commitment, confirmed on WhatsApp.",
    hero(f"{WP}/2022/09/Open_water_padi.webp",
         '<a href="index.html">Home</a> / Tailor Your Trip',
         "Tailor Your Trip",
         "Three questions, an honest estimate from our real price list, and your plan lands in our WhatsApp ready to confirm. Tailored is the whole point: this just gets the conversation started.")
    + f"""
<section class="page-section">
  <div class="container wiz-wrap">
    <div id="wizard" class="wiz-card"></div>
  </div>
</section>
<script src="wizard.js?v=9" defer></script>
"""
    + quote("We feel like we could not have picked a better place.", "Google review &middot; one of 508 five-star reviews"),
)

for fname, (title, desc, body) in pages.items():
    es_name = fname.replace(".html", "-es.html")
    schema = _faq_schema(body)
    if fname.startswith("course-"):
        schema += _course_schema(title, desc, BASE + fname)
    html = (HEAD.replace("{{TITLE}}", title).replace("{{DESC}}", desc) + body + FOOT)
    html = (html.replace("{{ES_URL}}", es_name)
                .replace("{{SELF}}", BASE + fname)
                .replace("{{EN_ABS}}", BASE + fname)
                .replace("{{ES_ABS}}", BASE + es_name)
                .replace("{{SCHEMA}}", schema))
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)
    print(f"wrote {fname} ({len(html)} bytes)")
