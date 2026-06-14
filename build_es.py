#!/usr/bin/env python3
"""Genera las páginas interiores en castellano del mockup DLVL."""
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
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,700;1,800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/webp" href="WPURL/2022/08/DivingLaVidaLoca-150x150.webp">
<meta name="google" content="notranslate">
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
{{SCHEMA}}<link rel="stylesheet" href="styles.css?v=35">
</head>
<body>

<header class="site-header">
  <div class="header-inner">
    <a href="index-es.html" class="brand">
      <img class="brand-logo" src="WPURL/2022/08/DivingLaVidaLoca-215x214.webp" alt="Logo de Diving La Vida Loca" width="46" height="46">
      <span class="brand-name">Diving La Vida Loca<small>PADI Dive Center &middot; Amed &middot; Bali</small></span>
    </a>
    <nav class="site-nav" aria-label="Principal">
      <a href="index-es.html#courses">Cursos</a>
      <a href="dive-sites-es.html">Puntos de Inmersi&oacute;n</a>
      <a href="fun-dives-es.html">Inmersiones</a>
      <a href="stay-and-dive-es.html">Aloja y Bucea</a>
      <a href="about-es.html">Nosotros</a>
      <a href="contact-es.html">Contacto</a>
    </nav>
    <div class="header-actions">
      <span class="lang-toggle"><a class="lang-es" href="{{EN_URL}}">EN</a> / <strong>ES</strong></span>
      <a class="pill-btn pill-btn--whatsapp" href="WAURL">WhatsApp</a>
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
        <p class="footer-tag">Centro de buceo boutique entre los arrozales de Amed, Bali, a 500 m de la playa de Melasti. Nunca m&aacute;s de cuatro buceadores por salida.</p>
      </div>
      <div>
        <h4>Bucea</h4>
        <ul>
          <li><a href="index-es.html#courses">Cursos PADI</a></li>
          <li><a href="dive-sites-es.html">Puntos de Inmersi&oacute;n</a></li>
          <li><a href="fun-dives-es.html">Inmersiones y Precios</a></li>
          <li><a href="amed-diving-guide-es.html">Gu&iacute;a de Buceo</a></li>
          <li><a href="plan-your-trip-es.html">Crea tu Viaje</a></li>
          <li><a href="stay-and-dive-es.html">Aloja y Bucea</a></li>
        </ul>
      </div>
      <div>
        <h4>Con&oacute;cenos</h4>
        <ul>
          <li><a href="about-es.html">El Equipo</a></li>
          <li><a href="conservation-es.html">Conservaci&oacute;n</a></li>
          <li><a href="index-es.html#reviews">Rese&ntilde;as</a></li>
          <li><a href="contact-es.html">Contacto</a></li>
        </ul>
      </div>
      <div>
        <h4>Contacto</h4>
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
      <span><a href="{{EN_URL}}">English</a> &middot; Espa&ntilde;ol</span>
    </div>
  </div>
</footer>

<script src="script.js?v=6" defer></script>
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
              T("Deep ridges with real pelagic chances.", "Crestas profundas con opci&oacute;n real de pel&aacute;gicos."), ""),
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
        pin_html += f"""
      <a href="{guide}#{anchor}" data-name="{plain}" data-meta="{meta}" data-desc="{desc}"{imgattr}>
        <circle class="pin-c" cx="{x}" cy="{y}" r="11" fill="#91131b" stroke="#c9a227" stroke-width="1.5"/>
        <text x="{x}" y="{y + 4}" text-anchor="middle" style="font: 700 10px Inter, sans-serif; fill: #fff;">{n}</text>
        <line x1="{x}" y1="{y - 12}" x2="{lx}" y2="{ly + 5}" stroke="#c9a227" stroke-width="1" opacity="0.45"/>
        <text x="{lx}" y="{ly}" text-anchor="middle" style="font: 600 11px Inter, sans-serif; letter-spacing: 1.2px; text-transform: uppercase; fill: #2a1d18;">{label}</text>
      </a>"""
    sea = "Bali Sea" if en else "Mar de Bali"
    note = "Hand-drawn &middot; not to scale" if en else "Dibujado a mano &middot; no a escala"
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
    return f'<section class="facts-bar" aria-label="Datos clave">\n  <div class="facts-inner">\n{cells}\n  </div>\n</section>\n'


def booking(price, sub, options, wa_text, trust):
    opts = "\n".join(f'      <li><span>{a}</span><span>{b}</span></li>' for a, b in options)
    ticks = "\n".join(f'      <li>{t}</li>' for t in trust)
    return f"""
  <aside class="booking-card" aria-label="Reservar">
    <p class="booking-price">{price}<small>{sub}</small></p>
    <ul class="booking-options">
{opts}
    </ul>
    <a class="pill-btn" href="plan-your-trip-es.html">Crea tu viaje &rarr;</a>
    <p class="booking-note">Preguntar no cuesta nada: dinos tus fechas y te confirmamos disponibilidad.</p>
    <ul class="booking-trust">
{ticks}
    </ul>
  </aside>
"""


TRUST = [
    "5,0 &#9733; con 508 rese&ntilde;as en Google",
    "M&aacute;x. 4 buceadores por instructor",
    "Cursos en ES &middot; CA &middot; EN &middot; FR &middot; ID",
    "Te recogemos gratis en la zona de Amed",
]


def quote(q, a):
    return f"""
<section class="hp-quote">
  <div class="container">
    <p class="quote-text">&ldquo;{q}&rdquo;</p>
    <span class="quote-attribution">{a}</span>
  </div>
</section>
"""


pages = {}

# ─────────────────────────── BAUTIZO (DISCOVER SCUBA) ───────────────────────────
pages["course-discover-scuba-es.html"] = ("course-discover-scuba.html",
    "Bautizo de Buceo en Bali, en Español · Amed, Sin Experiencia | Diving La Vida Loca",
    "Tu bautizo de buceo en Bali con instructores en español: media jornada en Amed con piscina privada e inmersión guiada en el arrecife. Desde IDR 1.050.000, todo incluido.",
    hero(f"{WP}/2024/07/GOPR9425-scaled.webp",
         '<a href="index-es.html">Inicio</a> / <a href="index-es.html#courses">Cursos</a> / Bautizo de Buceo',
         "Bautizo de Buceo",
         "Tu primera bocanada de aire bajo el agua, sin agobios. Una ma&ntilde;ana en nuestra piscina privada y despu&eacute;s una inmersi&oacute;n guiada en el arrecife, con el instructor a tu lado en todo momento. Sin experiencia, sin titulaci&oacute;n, sin prisas.")
    + facts([("Media jornada", "duraci&oacute;n"), ("12 m", "profundidad m&aacute;x."), ("Desde 10 a&ntilde;os", "edad m&iacute;nima"), ("1&ndash;2", "inmersiones"), ("M&aacute;x. 4", "por instructor")])
    + f"""
<div class="container course-layout">
  <div class="course-content">
    <h2>C&oacute;mo es la ma&ntilde;ana</h2>
    <div class="day-plan">
      <div class="day"><h3>1 · Caf&eacute; y briefing</h3><p>Te contamos c&oacute;mo funciona eso de respirar bajo el agua, qu&eacute; vas a sentir y las tres habilidades sencillas que vas a practicar. Pregunta todo lo que quieras: esto es una charla, no una clase magistral.</p></div>
      <div class="day"><h3>2 · La piscina</h3><p>Agua donde haces pie y el instructor a un brazo de distancia. Respiras, vac&iacute;as la m&aacute;scara y le coges el punto a tu ritmo. De la piscina no sale nadie sin una sonrisa.</p></div>
      <div class="day"><h3>3 · El arrecife</h3><p>Entrada tranquila desde la orilla en la bah&iacute;a de Jemeluk, nuestro arrecife de casa. Tres cuartos de hora entre coral con tu instructor de gu&iacute;a; la mayor&iacute;a est&aacute; tan ocupada mirando peces que se le olvidan los nervios.</p></div>
    </div>
    <h2>Qu&eacute; incluye</h2>
    <ul>
      <li>Todo el equipo, ajustado a ti antes de mojarte</li>
      <li>Sesi&oacute;n en piscina privada, nada de piscinas de hotel abarrotadas</li>
      <li>Inmersi&oacute;n guiada en el arrecife con transporte por la zona de Amed</li>
      <li>Caf&eacute;, t&eacute;, agua y algo de picar</li>
      <li>10% de impuestos incluidos, el precio que ves es el que pagas</li>
    </ul>
    <h2>Lo que pregunta todo el mundo la primera vez</h2>
    <div class="faq">
      <details><summary>Me da miedo agobiarme. &iquest;Qu&eacute; pasa entonces?</summary><p>Pues que vamos m&aacute;s despacio. En la piscina haces pie, el instructor no se separa de ti y aqu&iacute; no hay horario que te empuje. Muchos de nuestros mejores buceadores empezaron exactamente igual de nerviosos.</p></details>
      <details><summary>&iquest;Tengo que nadar muy bien?</summary><p>Tienes que estar a gusto en el agua, no ser nadador ol&iacute;mpico. Si flotas y chapoteas, puedes con esto.</p></details>
      <details><summary>&iquest;Cuenta para alguna titulaci&oacute;n?</summary><p>El bautizo en s&iacute; no es una titulaci&oacute;n, pero lo aprendido te sirve directamente para el Open Water, y si sigues con nosotros, ya eres de la familia.</p></details>
    </div>
  </div>
"""
    + booking("IDR 1.050.000", "&asymp; 55 &euro; &middot; 1 inmersi&oacute;n &middot; impuestos y equipo incluidos",
              [("2 inmersiones en vez de 1", "IDR 1.450.000"),
               ("2 inmersiones + 1 noche y desayuno", "IDR 1.700.000"),
               ("Seguir con el Open Water", "preg&uacute;ntanos")],
              "Hola!%20Quiero%20hacer%20un%20bautizo%20de%20buceo.%20Mis%20fechas%3A", TRUST)
    + "\n</div>\n"
    + quote("Acogedores, amables y siempre pendientes. Una experiencia incre&iacute;ble de principio a fin.", "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas"),
)

# ─────────────────────────── ADVANCED ───────────────────────────
pages["course-advanced-es.html"] = ("course-advanced.html",
    "Curso Advanced Open Water en Bali, en Español · Pecio del Liberty | Diving La Vida Loca",
    "Curso PADI Advanced Open Water en Amed, Bali. Cinco inmersiones de aventura en dos días, incluido el pecio USAT Liberty y una profunda a 30 m. IDR 4.900.000, impuestos incluidos.",
    hero(f"{WP}/2022/09/Advanced_open_water.webp",
         '<a href="index-es.html">Inicio</a> / <a href="index-es.html#courses">Cursos</a> / Advanced',
         "PADI Advanced Open Water",
         "Cinco inmersiones de aventura en dos d&iacute;as, con la bajada a 30 metros y, la que todo el mundo viene buscando, el pecio del USAT Liberty. Para este curso se invent&oacute; Amed.")
    + facts([("2 d&iacute;as", "duraci&oacute;n"), ("30 m", "profundidad titulada"), ("Desde 12 a&ntilde;os", "edad m&iacute;nima"), ("5", "inmersiones"), ("M&aacute;x. 4", "por instructor")])
    + f"""
<div class="container course-layout">
  <div class="course-content">
    <h2>C&oacute;mo son los dos d&iacute;as</h2>
    <div class="day-plan">
      <div class="day"><h3>D&iacute;a 1 · Navegaci&oacute;n y aventura</h3><p>Navegaci&oacute;n subacu&aacute;tica en el arrecife de casa y dos inmersiones de aventura elegidas contigo, flotabilidad perfecta e identificaci&oacute;n de peces son las favoritas. La teor&iacute;a se repasa con un caf&eacute; entre inmersiones, no en un aula al acabar.</p></div>
      <div class="day"><h3>D&iacute;a 2 · Profunda y pecio</h3><p>Por la ma&ntilde;ana, la profunda a 30 metros, donde ver&aacute;s c&oacute;mo cambian la luz y el color, y despu&eacute;s, el pecio del USAT Liberty. Un carguero de 120 metros de la Segunda Guerra Mundial al que se entra andando desde la playa. No existe mejor inmersi&oacute;n de aventura.</p></div>
    </div>
    <h2>Qu&eacute; incluye</h2>
    <ul>
      <li>Cinco inmersiones de aventura con todo el equipo y ordenador</li>
      <li>El pecio del Liberty y la profunda a 30 m, de serie</li>
      <li>Tasas de certificaci&oacute;n PADI y material digital</li>
      <li>Transporte, caf&eacute;, t&eacute;, agua y algo de picar entre inmersiones</li>
      <li>10% de impuestos incluidos</li>
    </ul>
    <h2>Lo que preguntan los buceadores</h2>
    <div class="faq">
      <details><summary>&iquest;Puedo hacerlo justo despu&eacute;s del Open Water?</summary><p>S&iacute;, y en Amed es lo que hace casi todo el mundo. Nuestro pack Open Water + Advanced (IDR 9.900.000) une los dos cursos en cinco d&iacute;as seguidos: la forma con mejor precio de llegar al pecio.</p></details>
      <details><summary>&iquest;Qu&eacute; inmersiones de aventura puedo elegir?</summary><p>Profunda y navegaci&oacute;n son obligatorias. Para las otras tres, hablamos de lo que te apetece: pecio, flotabilidad perfecta, identificaci&oacute;n de peces, nocturna y m&aacute;s.</p></details>
      <details><summary>&iquest;30 metros no es mucho salto?</summary><p>Es gradual y siempre acompa&ntilde;ado. Bajamos juntos con una referencia, pendientes de c&oacute;mo te encuentras en todo momento, con cuatro buceadores como m&aacute;ximo, aqu&iacute; nadie se pierde en el grupo.</p></details>
    </div>
  </div>
"""
    + booking("IDR 4.900.000", "&asymp; 255 &euro; por persona &middot; impuestos y equipo incluidos",
              [("2 personas o m&aacute;s", "IDR 4.550.000 c/u"),
               ("+ 2 noches en bungal&oacute;w con desayuno", "IDR 5.500.000"),
               ("Pack Open Water + Advanced", "IDR 9.900.000"),
               ("+ Aire Enriquecido / Nitrox", "IDR 6.990.000")],
              "Hola!%20Quiero%20reservar%20el%20curso%20Advanced.%20Mis%20fechas%3A", TRUST)
    + "\n</div>\n"
    + quote("Sentimos que no pod&iacute;amos haber elegido un sitio mejor.", "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas"),
)

# ─────────────────────────── RESCUE ───────────────────────────
pages["course-rescue-es.html"] = ("course-rescue.html",
    "Curso Rescue Diver + EFR en Bali, en Español · Amed | Diving La Vida Loca",
    "Curso PADI Rescue Diver con Emergency First Response en Amed, Bali. Tres días de simulacros que te convierten en un compañero de buceo de verdad. IDR 7.400.000, impuestos incluidos.",
    hero(f"{WP}/2022/09/Rescue_diver-1.webp",
         '<a href="index-es.html">Inicio</a> / <a href="index-es.html#courses">Cursos</a> / Rescue',
         "PADI Rescue Diver + EFR",
         "El curso que los buceadores siempre describen como el m&aacute;s gratificante que han hecho. Tres d&iacute;as de simulacros, juego de roles y resoluci&oacute;n de problemas, cosas serias, ense&ntilde;adas con sentido del humor.")
    + facts([("3 d&iacute;as", "duraci&oacute;n"), ("Desde 12 a&ntilde;os", "edad m&iacute;nima"), ("EFR", "primeros auxilios incl."), ("Simulacros", "pr&aacute;ctica real"), ("M&aacute;x. 4", "por instructor")])
    + f"""
<div class="container course-layout">
  <div class="course-content">
    <h2>C&oacute;mo son los tres d&iacute;as</h2>
    <div class="day-plan">
      <div class="day"><h3>D&iacute;a 1 · Emergency First Response</h3><p>RCP, primeros auxilios, vendajes, valoraci&oacute;n, la base en seco, practicada entre vosotros hasta que sale sola. &Uacute;til mucho m&aacute;s all&aacute; del buceo.</p></div>
      <div class="day"><h3>D&iacute;a 2 · Autorrescate y habilidades</h3><p>En la piscina y en el arrecife de casa: remolcar a un buceador cansado, responder a uno en p&aacute;nico, buscar a uno desaparecido. Cada ejercicio se repite hasta que parece m&aacute;s un juego que un examen.</p></div>
      <div class="day"><h3>D&iacute;a 3 · Simulacros completos</h3><p>El d&iacute;a famoso. El equipo improvisa situaciones en el arrecife y t&uacute; respondes, espera sorpresas, risas, y esa confianza tranquila que da el haberlo resuelto.</p></div>
    </div>
    <h2>Qu&eacute; incluye</h2>
    <ul>
      <li>Certificaci&oacute;n Emergency First Response (cuidados primarios y secundarios)</li>
      <li>Todo el equipo, sesiones de piscina y simulacros en el mar</li>
      <li>Tasas de certificaci&oacute;n PADI y material digital</li>
      <li>Transporte, caf&eacute;, t&eacute;, agua y algo de picar</li>
      <li>10% de impuestos incluidos</li>
    </ul>
    <h2>Lo que preguntan los buceadores</h2>
    <div class="faq">
      <details><summary>&iquest;Qu&eacute; requisitos hay?</summary><p>Advanced Open Water (o Adventure Diver con la de navegaci&oacute;n), 12 a&ntilde;os o m&aacute;s, y formaci&oacute;n EFR de los &uacute;ltimos 24 meses, por eso lo incluimos en el curso.</p></details>
      <details><summary>&iquest;Es tan agotador como dicen?</summary><p>Es el curso m&aacute;s f&iacute;sico del buceo recreativo, y del que la gente habla durante a&ntilde;os. Con grupos peque&ntilde;os, la intensidad se queda en divertida en vez de estresante.</p></details>
      <details><summary>Ya tengo el EFR en vigor.</summary><p>Entonces haz solo el Rescue por IDR 5.100.000 · escr&iacute;benos y comprobamos las fechas de tu certificado.</p></details>
    </div>
  </div>
"""
    + booking("IDR 7.400.000", "&asymp; 385 &euro; &middot; Rescue + EFR &middot; impuestos y equipo incluidos",
              [("Solo Rescue (con EFR en vigor)", "IDR 5.100.000"),
               ("Solo EFR", "IDR 2.700.000"),
               ("+ 3 noches en bungal&oacute;w con desayuno", "IDR 8.300.000")],
              "Hola!%20Quiero%20reservar%20el%20Rescue%20%2B%20EFR.%20Mis%20fechas%3A", TRUST)
    + "\n</div>\n"
    + quote("Una escuela de buceo aut&eacute;ntica, y lo digo como profesional del buceo.", "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas"),
)

# ─────────────────────────── DIVEMASTER ───────────────────────────
pages["course-divemaster-es.html"] = ("course-divemaster.html",
    "Divemaster en Bali, en Español · Prácticas Reales en Amed | Diving La Vida Loca",
    "Fórmate como Divemaster PADI en Amed, Bali. Hasta dos meses integrado en un centro boutique: cursos reales, clientes reales, mentoría de verdad. Desde IDR 19.000.000.",
    hero(f"{WP}/2022/09/DiveMasterw.webp",
         '<a href="index-es.html">Inicio</a> / <a href="index-es.html#courses">Cursos</a> / Divemaster',
         "PADI Divemaster",
         "Nada de pr&aacute;cticas en cadena. Estar&aacute;s integrado en un centro boutique hasta dos meses: asistiendo en cursos reales, guiando a clientes reales y aprendiendo c&oacute;mo funciona de verdad la filosof&iacute;a de cuatro buceadores por salida.")
    + facts([("2 meses", "hasta"), ("Pro", "primera titulaci&oacute;n profesional"), ("Ilimitadas", "opci&oacute;n de inmersiones"), ("1 a 1", "mentor&iacute;a"), ("Clientes reales", "desde la primera semana")])
    + f"""
<div class="container course-layout">
  <div class="course-content">
    <h2>Qu&eacute; vas a hacer de verdad</h2>
    <p>Ser Divemaster aqu&iacute; no es mirar desde el fondo de un barco con veinte personas. Con cuatro clientes como m&aacute;ximo por salida, formas parte del equipo desde el primer d&iacute;a: preparando equipo, dando briefings, asistiendo a Enric en los cursos, cartografiando puntos de inmersi&oacute;n y, con el tiempo, guiando a buceadores titulados por arrecifes que conocer&aacute;s como tu propia calle.</p>
    <ul>
      <li>Asiste en cursos PADI reales, del bautizo al Rescue</li>
      <li>Gu&iacute;a inmersiones por todo el tramo Amed&ndash;Tulamben, pecio del Liberty incluido</li>
      <li>Talleres de teor&iacute;a, equipo y calidad de demostraci&oacute;n de habilidades</li>
      <li>La conservaci&oacute;n forma parte del trabajo, seguimiento de los puntos de inmersi&oacute;n y limpiezas, no un extra</li>
      <li>Espa&ntilde;ol, catal&aacute;n, ingl&eacute;s, franc&eacute;s o indonesio, f&oacute;rmate en el idioma en que vas a trabajar</li>
    </ul>
    <h2>Dos maneras de hacerlo</h2>
    <div class="day-plan">
      <div class="day"><h3>Est&aacute;ndar, IDR 19.000.000</h3><p>El programa Divemaster completo con todas las inmersiones de formaci&oacute;n incluidas, en hasta dos meses.</p></div>
      <div class="day"><h3>Inmersiones ilimitadas · IDR 26.000.000</h3><p>El mismo programa, pero cada botella libre es tuya. Si quieres irte con m&aacute;s de 150 inmersiones y un conocimiento del arrecife a la altura, es esta.</p></div>
    </div>
    <h2>Lo que preguntan los candidatos</h2>
    <div class="faq">
      <details><summary>&iquest;Qu&eacute; requisitos hay?</summary><p>Rescue Diver con EFR en vigor, 40 inmersiones registradas para empezar (60 para certificarte) y un reconocimiento m&eacute;dico de los &uacute;ltimos 12 meses. &iquest;A&uacute;n no llegas? Te montamos el camino, muchos candidatos llegan con el Advanced y lo hacen todo aqu&iacute;.</p></details>
      <details><summary>&iquest;Qu&eacute; no est&aacute; incluido?</summary><p>La cuota anual de PADI y el Crew Pack de Divemaster (los manuales que PADI te exige tener). Te pasamos los precios actuales antes de comprometerte, sin sorpresas.</p></details>
      <details><summary>&iquest;Me ayud&aacute;is con el alojamiento para dos meses?</summary><p>S&iacute;, las tarifas de larga estancia en nuestros bungal&oacute;ws forman parte de la conversaci&oacute;n. Escr&iacute;benos y te montamos el paquete completo.</p></details>
    </div>
  </div>
"""
    + booking("IDR 19.000.000", "&asymp; 985 &euro; &middot; programa completo &middot; cuotas PADI y Crew Pack no incluidos",
              [("Opci&oacute;n inmersiones ilimitadas", "IDR 26.000.000"),
               ("Alojamiento de larga estancia", "preg&uacute;ntanos"),
               ("Camino desde el Rescue", "preg&uacute;ntanos")],
              "Hola!%20Me%20interesa%20el%20programa%20Divemaster.%20Mi%20experiencia%3A", TRUST)
    + "\n</div>\n"
    + quote("Soy feliz buceando y, cuando salgo del agua, soy feliz pensando en lo que he buceado.", "Eduardo Admetlla &middot; Pionero del buceo espa&ntilde;ol"),
)

# ─────────────────────────── ESPECIALIDADES ───────────────────────────
spec_cards = "".join(f"""
      <article class="eco-card">
        <span class="eco-num">{num}</span>
        <h3>{name}</h3>
        <p>{desc}</p>
        <p class="spec-price">{price}<small>{note}</small></p>
      </article>""" for num, name, desc, price, note in [
    ("01", "Aire Enriquecido (Nitrox)", "La especialidad m&aacute;s popular del buceo: m&aacute;s tiempo de fondo y menos intervalo en superficie. Un d&iacute;a, con o sin inmersiones.", "IDR 2.150.000", "solo teor&iacute;a &middot; IDR 2.900.000 con 2 inmersiones"),
    ("02", "Buceo Profundo", "Cuatro inmersiones en dos o tres d&iacute;as, bajando con calma hasta los 40 metros. Las paredes de Amed son el aula perfecta.", "IDR 3.900.000", "4 inmersiones &middot; desde 15 a&ntilde;os"),
    ("03", "Pack Profundo + Nitrox", "La pareja con m&aacute;s sentido: baja m&aacute;s y qu&eacute;date m&aacute;s tiempo. Dos especialidades en un mismo arco.", "IDR 6.400.000", "2 d&iacute;as &middot; desde 15 a&ntilde;os"),
    ("04", "Pack Ultimate Diver", "Advanced + Profundo + Nitrox en tres o cuatro d&iacute;as. Llegas con el Open Water y te vas listo para casi todo.", "IDR 10.500.000", "3&ndash;4 d&iacute;as &middot; desde 15 a&ntilde;os"),
    ("05", "Buceo en Pecios", "Cuatro inmersiones en el USAT Liberty aprendiendo cabos, focos y l&iacute;mites seguros de penetraci&oacute;n. El sitio se vende solo.", "Preg&uacute;ntanos", "4 inmersiones en el Liberty"),
    ("06", "Sidemount", "Dos botellas, trimado perfecto, hidrodin&aacute;mica total. Ense&ntilde;ado por gente que bucea en sidemount de verdad, no que solo lo certifica.", "Preg&uacute;ntanos", "sidemount recreativo"),
    ("07", "Refresco ReActivate", "&iquest;Oxidado? Media jornada de repaso en la piscina, con inmersi&oacute;n opcional en el arrecife para rematar. La vuelta al agua m&aacute;s amable.", "IDR 900.000", "+ 1 inmersi&oacute;n &middot; IDR 1.400.000"),
    ("08", "Emergency First Response", "RCP y primeros auxilios en un d&iacute;a, para buceadores, parejas, padres, cualquiera. No hace falta titulaci&oacute;n de buceo.", "IDR 2.700.000", "1 d&iacute;a &middot; abierto a no buceadores"),
])

pages["course-specialities-es.html"] = ("course-specialities.html",
    "Especialidades PADI en Amed, Bali · Nitrox, Profundo, Pecios, Sidemount | Diving La Vida Loca",
    "Especialidades PADI en Amed, Bali: Aire Enriquecido Nitrox, Buceo Profundo, Pecios en el USAT Liberty, Sidemount, refrescos y EFR. Desde IDR 900.000.",
    hero(f"{WP}/2024/07/sidemount-rec-diver-3-1024x576.webp",
         '<a href="index-es.html">Inicio</a> / <a href="index-es.html#courses">Cursos</a> / Especialidades',
         "Especialidades y Formaci&oacute;n Continua",
         "Con un pecio de la Segunda Guerra Mundial a 25 minutos por la costa, paredes que caen m&aacute;s all&aacute; de los 40 metros y un arrecife de casa hecho para pulir la flotabilidad, en Amed las especialidades dejan de ser teor&iacute;a.")
    + f"""
<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Elige Tu Camino</h2></div>
    <p class="section-sub">Todas las especialidades funcionan con las mismas reglas que todo lo dem&aacute;s aqu&iacute;: m&aacute;ximo cuatro buceadores, a tu ritmo, con equipo e impuestos incluidos. Hay muchas m&aacute;s especialidades PADI disponibles, si no ves la tuya, pregunta.</p>
    <div class="eco-grid" style="grid-template-columns: repeat(2, 1fr);">{spec_cards}
    </div>
    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hola!%20Me%20interesa%20una%20especialidad%3A">Pregunta por una especialidad</a></div>
  </div>
</section>
"""
    + quote("Sentimos que no pod&iacute;amos haber elegido un sitio mejor.", "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas"),
)

# ─────────────────────────── PUNTOS DE INMERSIÓN ───────────────────────────
sites = [
    ("Pecio del USAT Liberty", "Tulamben &middot; 25 min en coche", f"{WP}/2022/09/Advanced_open_water.webp",
     "Un carguero de 120 metros de la Segunda Guerra Mundial, torpedeado en 1942 y empujado al mar por la erupci&oacute;n del Agung en 1963. Hoy es la inmersi&oacute;n desde la costa m&aacute;s famosa del mundo: entras andando por la arena volc&aacute;nica y en minutos est&aacute;s planeando sobre un casco cubierto de coral. Ven al amanecer y el banco de peces loro cabez&oacute;n desfila como quien va al trabajo.",
     [("5&ndash;30 m", "profundidad"), ("Todos los niveles", "desde Open Water"), ("Amanecer", "mejor momento")]),
    ("Bah&iacute;a de Jemeluk", "Amed &middot; nuestro arrecife de casa", f"{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp",
     "Tranquila, somera y absurdamente generosa, aqu&iacute; respira por primera vez en el mar cada alumno de Open Water, y aqu&iacute; volvemos nosotros en los d&iacute;as libres. Jardines de coral desde los tres metros, una pared que se descuelga para las inmersiones m&aacute;s profundas, y la clase de vida macro que convierte 45 minutos en 70.",
     [("3&ndash;25 m", "profundidad"), ("Todos los niveles", "primeras inmersiones"), ("De casa", "el aula de cada d&iacute;a")]),
    ("Pecio Japon&eacute;s", "Banyuning &middot; 10 min en coche", f"{WP}/2022/09/Open_water_padi.webp",
     "Una peque&ntilde;a patrullera de la Segunda Guerra Mundial, tan somera que hasta los esnorquelistas la ven, pero sus mejores secretos son para buceadores. El casco est&aacute; completamente cubierto de coral blando, y la ladera de alrededor esconde caballitos pigmeos para ojos pacientes y buena flotabilidad. Un favorito infravalorado.",
     [("2&ndash;12 m", "profundidad"), ("Todos los niveles", "esn&oacute;rquel tambi&eacute;n"), ("Macro", "caballitos pigmeos")]),
    ("Las Pir&aacute;mides", "Amed &middot; a 5 minutos", f"{WP}/2022/09/DiveMasterw.webp",
     "Estructuras de arrecife artificial apiladas en la arena como templos hundidos, hoy repletas de peces cristal, peces le&oacute;n y alguna tortuga de paso. Una segunda inmersi&oacute;n brillante, un aula perfecta de navegaci&oacute;n, y la prueba de que con un poco de ayuda el mar se reconstruye r&aacute;pido.",
     [("5&ndash;22 m", "profundidad"), ("Todos los niveles", "gran segunda inmersi&oacute;n"), ("Tortugas", "visitantes habituales")]),
    ("Coral Garden", "Tulamben &middot; 25 min en coche", f"{WP}/2022/09/Nitrox.webp",
     "El jard&iacute;n de esculturas sumergido de Tulamben: estatuas y estructuras entre coral blando, todo al alcance de la superficie. Un parque de juegos para fot&oacute;grafos, una segunda inmersi&oacute;n tranquila y la parada de seguridad m&aacute;s bonita de la costa.",
     [("2&ndash;12 m", "profundidad"), ("Todos los niveles", "esn&oacute;rquel tambi&eacute;n"), ("Fotos", "esculturas y coral")]),
    ("Drop-Off de Tulamben", "Tulamben &middot; 25 min en coche", f"{WP}/2022/09/Advanced_open_water.webp",
     "Donde la roca volc&aacute;nica se desploma hacia el azul. Gorgonias gigantes, bancos de peces pegados a la pared y, de vez en cuando, algo grande que pasa de largo desde el fondo. Es el aula de nuestros cursos profundos, y el favorito de cada divemaster que nos visita.",
     [("10&ndash;40 m", "profundidad"), ("Avanzado", "mejor en profundidad"), ("Pared", "gorgonias y pel&aacute;gicos")]),
    ("Arrecife de Melasti", "Amed &middot; a 500 m de la puerta", f"{WP}/2022/09/Rescue_diver-1.webp",
     "Nuestra inmersi&oacute;n de barrio, literalmente bajando el camino desde los bungal&oacute;ws. Un arrecife en pendiente con praderas y tortugas residentes, perfecto para una ma&ntilde;ana f&aacute;cil o una tarde relajada cuando no apetece coger el coche.",
     [("4&ndash;20 m", "profundidad"), ("Todos los niveles", "la log&iacute;stica m&aacute;s f&aacute;cil"), ("Tortugas", "residentes")]),
    ("Seraya Secrets", "Seraya &middot; 20 min en coche", f"{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp",
     "Arena negra y tesoros diminutos. Seraya es el icono del muck diving de esta costa: peces sapo, gambas arlequ&iacute;n, peces pipa fantasma y nudibranquios por docenas. Trae un foco, baja el ritmo y deja que los ojos de bi&oacute;logo de Irman te encuentren cosas que pasar&iacute;as nadando de largo.",
     [("5&ndash;20 m", "profundidad"), ("Todos los niveles", "paciencia para el macro"), ("Muck", "capital del bicheo")]),
]
site_rows = ""
for i, (name, kicker, img, desc, stats) in enumerate(sites):
    flip = " feature-row--flip" if i % 2 else ""
    stat_html = "".join(f'<div class="feature-stat"><strong>{a}</strong><span>{b}</span></div>' for a, b in stats)
    site_rows += f"""
    <div class="feature-row{flip}">
      <div class="feature-img"><img src="{img}" alt="{name}" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">{kicker}</p>
        <h2>{name}</h2>
        <p>{desc}</p>
        <div class="feature-stats">{stat_html}</div>
      </div>
    </div>"""

pages["dive-sites-es.html"] = ("dive-sites.html",
    "Buceo en Tulamben y Amed, Bali · Pecio USAT Liberty y Más | Diving La Vida Loca",
    "Los puntos de inmersión de Amed y Tulamben, Bali: el pecio del USAT Liberty, la bahía de Jemeluk, el Pecio Japonés y más. Todo desde la costa, todo a minutos de nuestra puerta.",
    hero(f"{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp",
         '<a href="index-es.html">Inicio</a> / Puntos de Inmersi&oacute;n',
         "D&oacute;nde Bucear&aacute;s",
         "Una sola costa volc&aacute;nica, llena de inmersiones de primer nivel desde la orilla: un pecio de la II Guerra Mundial, bah&iacute;as de coral, paredes y muck sobre arena negra. Los sitios que buceamos a diario y ayudamos a cuidar.")
    + facts([("13", "puntos con nombre en la costa"), ("Desde la costa", "todas las inmersiones"), ("26&ndash;29&deg;C", "agua todo el a&ntilde;o"), ("Abr&ndash;Nov", "mejor visibilidad"), ("25 min", "en coche hasta el Liberty")])
    + f"""
<section class="page-section map-fold">
  <div class="container">{coast_map("es")}</div>
</section>
"""
    + f"""
<section class="page-section">
  <div class="container">{site_rows}
    <div class="included-note">Cada inmersi&oacute;n incluye gu&iacute;a, equipo completo, transporte por la zona de Amed y caf&eacute; en la playa al salir. Con cada sitio va su briefing de condiciones, y si ese d&iacute;a el arrecife est&aacute; mejor en otro punto, te lo decimos y vamos all&iacute;. &iquest;Quieres profundidades, temporadas e historia punto por punto? Lee la <a href="amed-diving-guide-es.html">gu&iacute;a completa de buceo en Amed y Tulamben</a>.</div>
    <div class="section-cta"><a class="section-cta-link" href="fun-dives-es.html">Precios de inmersiones &rarr;</a></div>
  </div>
</section>
"""
    + quote("El mar, una vez lanzado su hechizo, te atrapa para siempre en su red de asombro.", "Jacques-Yves Cousteau"),
)

# ─────────────────────────── INMERSIONES ───────────────────────────
pages["fun-dives-es.html"] = ("fun-dives.html",
    "Inmersiones en Amed y Tulamben, Bali · Precios y Packs | Diving La Vida Loca",
    "Inmersiones guiadas en Amed y Tulamben desde IDR 690.000 con equipo, guía y transporte incluidos. Descuentos por varios días, nocturnas y guía privado.",
    hero(f"{WP}/2022/09/Nitrox.webp",
         '<a href="index-es.html">Inicio</a> / Inmersiones',
         "Inmersiones y Precios",
         "&iquest;Ya tienes titulaci&oacute;n? Ens&eacute;&ntilde;anos la tarjeta y cu&eacute;ntanos tu lista de deseos. M&aacute;ximo cuatro buceadores por gu&iacute;a, sitios elegidos seg&uacute;n las condiciones del d&iacute;a, y todo incluido, equipo, transporte y el caf&eacute; de despu&eacute;s.")
    + facts([("M&aacute;x. 4", "buceadores por gu&iacute;a"), ("Todo el equipo", "siempre incluido"), ("12+", "puntos para elegir"), ("5&ndash;10%", "descuento por d&iacute;as"), ("&ndash;10%", "con 5+ d&iacute;as")])
    + f"""
<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Precios Claros, Sin Letra Peque&ntilde;a</h2></div>
    <p class="section-sub">Todos los precios incluyen el 10% de impuestos, equipo completo, gu&iacute;a, transporte por la zona de Amed y caf&eacute;, t&eacute;, agua y galletas. Sin recargos esperando en caja.</p>

    <div class="price-block">
      <h3>Inmersiones desde la costa, Amed y Tulamben</h3>
      <p class="price-block-sub">Incluido el pecio del USAT Liberty, la bah&iacute;a de Jemeluk, el Pecio Japon&eacute;s y Las Pir&aacute;mides.</p>
      <div class="price-row"><span class="price-name">1 inmersi&oacute;n</span><span class="price-val">IDR 690.000<small>&asymp; 36 &euro;</small></span></div>
      <div class="price-row"><span class="price-name">2 inmersiones <small>el cl&aacute;sico d&iacute;a completo</small></span><span class="price-val">IDR 990.000<small>&asymp; 51 &euro;</small></span></div>
      <div class="price-row"><span class="price-name">3 inmersiones <small>pecio al amanecer + dos m&aacute;s</small></span><span class="price-val">IDR 1.490.000<small>&asymp; 77 &euro;</small></span></div>
      <div class="price-row"><span class="price-name">Inmersi&oacute;n nocturna</span><span class="price-val">IDR 790.000<small>&asymp; 41 &euro;</small></span></div>
      <div class="price-row"><span class="price-name">Gu&iacute;a privado <small>t&uacute; y tu gu&iacute;a, nadie m&aacute;s</small></span><span class="price-val">+ IDR 300.000<small>por inmersi&oacute;n</small></span></div>
    </div>

    <div class="price-block">
      <h3>Bucea M&aacute;s, Paga Menos</h3>
      <p class="price-block-sub">Para quien se queda una temporada, m&iacute;nimo dos inmersiones al d&iacute;a.</p>
      <div class="price-row"><span class="price-name">3 o m&aacute;s d&iacute;as de buceo</span><span class="price-val">5% dto.</span></div>
      <div class="price-row"><span class="price-name">5 o m&aacute;s d&iacute;as de buceo</span><span class="price-val">10% dto.</span></div>
      <div class="price-row"><span class="price-name">2 inmersiones + 1 noche con desayuno</span><span class="price-val">IDR 1.290.000<small>&asymp; 67 &euro;</small></span></div>
    </div>

    <div class="included-note">&iquest;Hace tiempo que no buceas? El refresco ReActivate (IDR 900.000, media jornada) te devuelve la soltura antes de tus inmersiones, la mayor&iacute;a dice que es el dinero mejor gastado del viaje.</div>
    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hola!%20Quiero%20reservar%20inmersiones.%20Mis%20fechas%20y%20titulaci%C3%B3n%3A">Reserva tus inmersiones por WhatsApp</a></div>
  </div>
</section>
"""
    + quote("Acogedores, amables y siempre pendientes. Una experiencia incre&iacute;ble de principio a fin.", "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas"),
)

# ─────────────────────────── ALOJA Y BUCEA ───────────────────────────
pages["stay-and-dive-es.html"] = ("stay-and-dive.html",
    "Aloja y Bucea en Amed, Bali · Bungalós + Packs de Buceo | Diving La Vida Loca",
    "Duerme donde buceas: bungalós entre los arrozales de Amed, a 500 m de la playa de Melasti, con desayuno incluido. Packs de curso e inmersiones desde IDR 1.290.000.",
    hero(f"{WP}/2022/09/Terrace-768x512.webp",
         '<a href="index-es.html">Inicio</a> / Aloja y Bucea',
         "Duerme Donde Buceas",
         "Bungal&oacute;ws entre los arrozales, a quinientos metros de la playa de Melasti. Te levantas, desayunas en la terraza y vas andando al briefing, el trayecto al trabajo es un sendero.")
    + facts([("500 m", "hasta la playa"), ("Desayuno", "siempre incluido"), ("Arrozales", "tus vecinos"), ("En el centro", "piscina y restaurante"), ("Packs", "curso + estancia")])
    + f"""
<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">El Sitio</h2></div>
    <p class="section-sub">Quedarte aqu&iacute; es lo que convierte un curso en una semana en familia: desayuno con tu instructor, los diarios de buceo en la terraza al atardecer, y prioridad para el pecio al amanecer. Las habitaciones van seg&uacute;n disponibilidad, dinos tus fechas pronto.</p>
    <div class="gallery-grid">
      <img src="{WP}/2022/09/Terrace-768x512.webp" alt="Terraza de los bungal&oacute;ws de Diving La Vida Loca" loading="lazy">
      <img src="{WP}/2022/09/kantor-depan-HDR-Edit-768x576.webp" alt="Recepci&oacute;n y jardines de Diving La Vida Loca" loading="lazy">
      <img src="{WP}/2022/09/Meeting-room-1-768x512.webp" alt="Aula y sala de reuniones" loading="lazy">
    </div>

    <div style="height:3rem"></div>
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Packs Aloja y Bucea</h2></div>
    <p class="section-sub">Los packs con alojamiento incluyen desayuno. Todos los precios llevan el 10% de impuestos incluido.</p>
    <div class="price-block">
      <h3>Curso + Alojamiento</h3>
      <div class="price-row"><span class="price-name">Bautizo (2 inmersiones) + 1 noche</span><span class="price-val">IDR 1.700.000<small>&asymp; 88 &euro;</small></span></div>
      <div class="price-row"><span class="price-name">Open Water + 3 noches</span><span class="price-val">IDR 6.300.000<small>&asymp; 325 &euro;</small></span></div>
      <div class="price-row"><span class="price-name">Advanced + 2 noches</span><span class="price-val">IDR 5.500.000<small>&asymp; 285 &euro;</small></span></div>
      <div class="price-row"><span class="price-name">Rescue + EFR + 3 noches</span><span class="price-val">IDR 8.300.000<small>&asymp; 430 &euro;</small></span></div>
      <div class="price-row"><span class="price-name">2 inmersiones + 1 noche</span><span class="price-val">IDR 1.290.000<small>&asymp; 67 &euro;</small></span></div>
    </div>
    <div class="included-note">&iquest;Vienes al programa Divemaster? Las tarifas de larga estancia, hasta dos meses, forman parte del paquete, preg&uacute;ntanos.</div>
    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hola!%20Quiero%20un%20pack%20aloja%20y%20bucea.%20Mis%20fechas%3A">Consulta disponibilidad por WhatsApp</a></div>
  </div>
</section>
"""
    + quote("Sentimos que no pod&iacute;amos haber elegido un sitio mejor.", "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas"),
)

# ─────────────────────────── NOSOTROS ───────────────────────────
pages["about-es.html"] = ("about.html",
    "Centro de Buceo Español en Bali · Amed, Boutique | Diving La Vida Loca",
    "Centro de buceo español en Bali: PADI boutique en Amed, cursos en tu idioma y nunca más de cuatro buceadores por salida. Conoce al equipo y el centro.",
    hero(f"{WP}/2022/08/TEAM5-768x512.webp",
         '<a href="index-es.html">Inicio</a> / Nosotros',
         "Peque&ntilde;os a Prop&oacute;sito",
         "La mayor&iacute;a de los centros de buceo crecen a&ntilde;adiendo barcos, bancos y reservas. Nosotros crecimos decidiendo no hacerlo. Cuatro buceadores por salida no es una limitaci&oacute;n, es la idea entera.", pos="center 20%")
    + facts([("M&aacute;x. 4", "buceadores por salida"), ("20+ a&ntilde;os", "en el agua"), ("5", "idiomas"), ("5,0 &#9733;", "508 rese&ntilde;as en Google"), ("PADI", "Dive Center")])
    + f"""
<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">La Idea</h2></div>
    <div class="feature-row">
      <div class="feature-img"><img src="{WP}/2022/09/equipment-room-1-768x512.webp" alt="Sala de equipo de Diving La Vida Loca" loading="lazy"></div>
      <div class="feature-body">
        <p>Diving La Vida Loca es un PADI Dive Center de gesti&oacute;n espa&ntilde;ola entre los arrozales de Amed, a quinientos metros de la playa de Melasti. El nombre es la filosof&iacute;a: bucear es la parte loca y alegre de la vida, y merece hacerse bien.</p>
        <p>Eso significa una piscina privada para cada primera habilidad. Significa equipo mantenido como si bucear&aacute;ramos con &eacute;l nosotros, porque lo hacemos. Significa cursos a tu ritmo y en tu idioma. Y significa que cuando vuelvas el a&ntilde;o que viene (la gente vuelve), alguien se acordar&aacute; de tu nombre y de c&oacute;mo te gusta el caf&eacute;.</p>
      </div>
    </div>

    <div style="height:4rem"></div>
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">El Equipo</h2></div>
    <p class="section-sub">M&aacute;s de veinte a&ntilde;os en el agua entre todos, ense&ntilde;ando en espa&ntilde;ol, catal&aacute;n, ingl&eacute;s, franc&eacute;s e indonesio.</p>
    <div class="team-grid">
      <article class="team-card">
        <div class="team-photo"><img src="{WP}/2022/08/Enrik_mask1-600x900.webp" alt="Enric, PADI Master Scuba Diver Trainer" loading="lazy"></div>
        <h3 class="team-name">Enric</h3>
        <p class="team-role">Master Scuba Diver Trainer</p>
        <p class="team-bio">Instructor Elite de PADI y buceador profesional. Estar&aacute; contigo en la piscina desde el primer d&iacute;a.</p>
      </article>
      <article class="team-card">
        <div class="team-photo"><img src="{WP}/2022/08/Irman_mask_1-600x900.webp" alt="Irman, Divemaster y bi&oacute;logo" loading="lazy"></div>
        <h3 class="team-name">Irman</h3>
        <p class="team-role">Divemaster &middot; Bi&oacute;logo</p>
        <p class="team-bio">Conoce cada bicho del arrecife por su nombre, el latino y el local.</p>
      </article>
      <article class="team-card">
        <div class="team-photo"><img src="{WP}/2022/08/NENGAH_mod_2.webp" alt="Nengah, recepci&oacute;n" loading="lazy"></div>
        <h3 class="team-name">Nengah</h3>
        <p class="team-role">Recepci&oacute;n</p>
        <p class="team-bio">La primera sonrisa que ver&aacute;s, y la persona que hace que todo salga a su hora.</p>
      </article>
    </div>

    <div style="height:4rem"></div>
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">El Centro</h2></div>
    <p class="section-sub">Echa un vistazo antes de venir, la piscina, la sala de equipo, el aula, la terraza.</p>
    <div class="gallery-grid">
      <img src="{WP}/2022/09/equipment-room-2-768x512.webp" alt="Sala de equipo de buceo" loading="lazy">
      <img src="{WP}/2022/09/Clean_equipment-768x512.webp" alt="Equipo de buceo limpio y mantenido" loading="lazy">
      <img src="{WP}/2022/09/Meeting-room-1-768x512.webp" alt="Aula de cursos" loading="lazy">
      <img src="{WP}/2022/09/front-office-768x512.webp" alt="Recepci&oacute;n" loading="lazy">
      <img src="{WP}/2022/09/car-1-768x512.webp" alt="Transporte del centro" loading="lazy">
      <img src="{WP}/2022/09/Terrace-768x512.webp" alt="Terraza" loading="lazy">
    </div>
    <div class="section-cta"><a class="section-cta-link" href="conservation-es.html">Nuestra labor de conservaci&oacute;n &rarr;</a></div>
  </div>
</section>
"""
    + quote("Una escuela de buceo aut&eacute;ntica, y lo digo como profesional del buceo.", "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas"),
)

# ─────────────────────────── CONSERVACIÓN ───────────────────────────
pages["conservation-es.html"] = ("conservation.html",
    "Conservación del Arrecife en Amed, Bali · Diving La Vida Loca | Diving La Vida Loca",
    "Conservación en Diving La Vida Loca: formación que pone el arrecife primero, limpiezas y seguimiento de los puntos de inmersión, y un modelo boutique que quita presión a los arrecifes de Amed.",
    hero(f"{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp",
         '<a href="index-es.html">Inicio</a> / Conservaci&oacute;n',
         "No Solo Buceamos Aqu&iacute;.<br>Lo Cuidamos.",
         "Los arrecifes de Amed son nuestro lugar de trabajo, nuestra aula y nuestra casa. La conservaci&oacute;n no es una p&aacute;gina de la web, es c&oacute;mo empieza cada briefing y c&oacute;mo se gu&iacute;a cada inmersi&oacute;n.")
    + f"""
<section class="page-section">
  <div class="container">
    <div class="feature-row">
      <div class="feature-img"><img src="{WP}/2024/07/GOPR9425-768x1024.webp" alt="Pr&aacute;ctica de flotabilidad en la piscina" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">01 &middot; El arrecife, primero</p>
        <h2>Lo m&aacute;s amable que puede aprender un buceador es flotabilidad</h2>
        <p>Cada buceador que certificamos se va sabiendo disfrutar de un arrecife sin tocarlo. La flotabilidad perfecta aqu&iacute; no es una especialidad, es la base de cada curso, trabajada en la piscina antes de que nadie vea un coral. Con cuatro buceadores por instructor, no hay aleta que se quede sin vigilar.</p>
      </div>
    </div>
    <div class="feature-row feature-row--flip">
      <div class="feature-img"><img src="{WP}/2022/09/Clean_equipment-768x512.webp" alt="Cuidado y mantenimiento en el centro" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">02 &middot; Manos en el agua</p>
        <h2>Limpiezas, seguimiento y estar atentos</h2>
        <p>Buceamos estos sitios todos los d&iacute;as, y eso nos convierte en su sistema de alerta temprana. Limpiezas de arrecife y de playa, ojo puesto en la salud del coral en cada estaci&oacute;n, y la voz de alarma cuando algo cambia. Preg&uacute;ntanos qu&eacute; est&aacute; pasando en el arrecife esta temporada. No vamos a saber parar de hablar.</p>
      </div>
    </div>
    <div class="feature-row">
      <div class="feature-img"><img src="{WP}/2022/08/TEAM5-768x512.webp" alt="El equipo de Diving La Vida Loca" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">03 &middot; Parte de Amed</p>
        <h2>La econom&iacute;a del arrecife funciona cuando ganan todos</h2>
        <p>Somos un equipo peque&ntilde;o con ra&iacute;ces en este pueblo, trabajando junto a la comunidad local que depende de un arrecife sano tanto como nosotros. Llevar grupos diminutos no es solo mejor buceo, es menos presi&oacute;n sobre los sitios de los que aqu&iacute; vive todo el mundo.</p>
      </div>
    </div>
    <div class="included-note">&iquest;Quieres echar una mano mientras est&aacute;s aqu&iacute;? Ap&uacute;ntate a una inmersi&oacute;n de limpieza, haz la especialidad de Flotabilidad Perfecta, o simplemente p&iacute;dele a Irman que te ense&ntilde;e el arrecife con ojos de bi&oacute;logo, te cambia la forma de bucear para siempre.</div>
    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hola!%20Quiero%20apuntarme%20a%20una%20inmersi%C3%B3n%20de%20limpieza%3A">Ap&uacute;ntate a una inmersi&oacute;n de limpieza</a></div>
  </div>
</section>
"""
    + quote("La gente protege lo que ama.", "Jacques-Yves Cousteau"),
)

# ─────────────────────────── CONTACTO ───────────────────────────
pages["contact-es.html"] = ("contact.html",
    "Contacto · Diving La Vida Loca, Amed, Bali | WhatsApp y Cómo Llegar",
    "Contacta con Diving La Vida Loca en Amed, Bali. WhatsApp +62 821 4553 8716, Instagram, Facebook, o mándanos una consulta. A 500 m de la playa de Melasti.",
    hero(f"{WP}/2022/09/kantor-depan-HDR-Edit-768x576.webp",
         '<a href="index-es.html">Inicio</a> / Contacto',
         "Di Hola",
         "WhatsApp es lo m&aacute;s r&aacute;pido, solemos contestar en menos de una hora. Dinos tus fechas, tu titulaci&oacute;n (o ninguna) y con qu&eacute; sue&ntilde;as. El resto lo montamos a tu medida.")
    + f"""
<section class="page-section">
  <div class="container contact-grid">
    <div>
      <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Encu&eacute;ntranos</h2></div>
      <ul class="contact-list">
        <li><strong>WhatsApp</strong><a href="{WA}">+62 821 4553 8716</a></li>
        <li><strong>Instagram</strong><a href="https://www.instagram.com/diving.lavidaloca">@diving.lavidaloca</a></li>
        <li><strong>Facebook</strong><a href="https://www.facebook.com/Divinglavidaloca">Diving La Vida Loca</a></li>
        <li><strong>D&oacute;nde</strong>Amed, Karangasem, Bali, entre los arrozales, a 500 m de la playa de Melasti</li>
      </ul>
      <a class="pill-btn pill-btn--whatsapp" href="{WA}">Escr&iacute;benos por WhatsApp</a>
      <div class="map-embed">
        <iframe title="Mapa de Amed, Bali" src="https://www.openstreetmap.org/export/embed.html?bbox=115.63,-8.37,115.71,-8.31&amp;layer=mapnik&amp;marker=-8.34,115.67" loading="lazy"></iframe>
      </div>
      <p class="map-attrib">Mapa &copy; colaboradores de <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a></p>
    </div>
    <div class="form-card">
      <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">O Escr&iacute;benos Aqu&iacute;</h2></div>
      <form id="enquiry-form">
        <div class="form-field"><label for="f-name">Nombre</label><input id="f-name" type="text" placeholder="Tu nombre"></div>
        <div class="form-field"><label for="f-email">Email</label><input id="f-email" type="email" placeholder="tu@email.com"></div>
        <div class="form-field"><label for="f-course">Me interesa</label>
          <select id="f-course">
            <option>Bautizo de buceo</option>
            <option>PADI Open Water</option>
            <option>Advanced Open Water</option>
            <option>Rescue + EFR</option>
            <option>Divemaster</option>
            <option>Especialidades</option>
            <option>Inmersiones</option>
            <option>Pack aloja y bucea</option>
          </select>
        </div>
        <div class="form-field"><label for="f-dates">Fechas</label><input id="f-dates" type="text" placeholder="p. ej. 12&ndash;18 de agosto"></div>
        <div class="form-field"><label for="f-msg">Mensaje</label><textarea id="f-msg" rows="4" placeholder="Titulaci&oacute;n, cu&aacute;ntos sois, sue&ntilde;os&hellip;"></textarea></div>
        <button class="pill-btn" type="submit">Enviar por WhatsApp</button>
      </form>
    </div>
  </div>
</section>
""",
)


# ─────────────────────────── GUÍA DE BUCEO ───────────────────────────
guia_sitios = """
    <div class="feature-row" id="liberty">
      <div class="feature-img"><img src="{WP}/2022/09/Advanced_open_water.webp" alt="Buceadores en el pecio USAT Liberty, Tulamben" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">La joya &middot; Tulamben</p>
        <h2>Pecio del USAT Liberty</h2>
        <p>El Liberty es la raz&oacute;n por la que media comunidad buceadora conoce esta costa. Un transporte del ej&eacute;rcito estadounidense de 120 metros, torpedeado por un submarino japon&eacute;s en enero de 1942 cuando cruzaba el estrecho de Lombok, remolcado hacia Bali y varado en la playa de Tulamben. All&iacute; pas&oacute; veinte a&ntilde;os, hasta que los temblores de la erupci&oacute;n del Agung en 1963 lo empujaron al agua, y el mar se puso manos a la obra.</p>
        <p>Hoy descansa sobre una ladera de arena volc&aacute;nica entre los 5 y los 30 metros, colonizado por completo de coral duro y blando. Su parte alta se ve haciendo esn&oacute;rquel; con el Open Water ves casi todo; con el Advanced llegas a la popa y a los pasajes profundos. El banco residente de peces loro cabez&oacute;n patrulla al amanecer, con j&uacute;reles, barracudas y anguilas jard&iacute;n en la ladera.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>5&ndash;30 m</strong><span>profundidad</span></div><div class="feature-stat"><strong>Todos los niveles</strong><span>esn&oacute;rquel incluido</span></div><div class="feature-stat"><strong>Amanecer</strong><span>cabezones y pecio vac&iacute;o</span></div></div>
      </div>
    </div>
    <div class="included-note">C&oacute;mo lo buceamos: el Liberty recibe excursiones del sur de Bali desde media ma&ntilde;ana. Alojados en Amed, nosotros entramos al agua al amanecer, antes de que llegue el primer autob&uacute;s, con cuatro buceadores como mucho. Te llevas el pecio, los cabezones y el silencio.</div>

    <div class="feature-row feature-row--flip" id="jemeluk">
      <div class="feature-img"><img src="{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp" alt="Arrecife de coral en la bah&iacute;a de Jemeluk, Amed" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">Nuestro arrecife de casa &middot; Amed</p>
        <h2>Bah&iacute;a de Jemeluk y la pared de Amed</h2>
        <p>Jemeluk es la bah&iacute;a alrededor de la que se enrosca el pueblo: jardines de coral tranquilos y someros desde los tres metros, bajando hasta una pared que se descuelga m&aacute;s all&aacute; de los 25 en su punta este. Aqu&iacute; respira por primera vez en el mar cada alumno de Open Water, y el esn&oacute;rquel es tan bueno que la pareja no buceadora no se queda fuera del plan. Nubes de anthias, alg&uacute;n pulpo si miras despacio, y el famoso buz&oacute;n submarino.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>3&ndash;25 m</strong><span>profundidad</span></div><div class="feature-stat"><strong>Todos los niveles</strong><span>primeras inmersiones</span></div><div class="feature-stat"><strong>De casa</strong><span>el aula de cada d&iacute;a</span></div></div>
      </div>
    </div>

    <div class="feature-row" id="japanese-wreck">
      <div class="feature-img"><img src="{WP}/2022/09/Open_water_padi.webp" alt="Coral blando en el pecio japon&eacute;s, Banyuning" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">El secreto somero &middot; Banyuning</p>
        <h2>Pecio Japon&eacute;s</h2>
        <p>Un peque&ntilde;o barco de acero de la Segunda Guerra Mundial increíblemente somero, entre los 2 y los 12 metros, tan cerca de la superficie que los esnorquelistas flotan por encima. Que la profundidad no te enga&ntilde;e: el casco est&aacute; forrado de coral blando, y la ladera de al lado cae con gorgonias que esconden caballitos pigmeos. Inmersiones largas, someras y saturadas de color, con tiempo de fondo infinito. El favorito de los fot&oacute;grafos.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>2&ndash;12 m</strong><span>el pecio en s&iacute;</span></div><div class="feature-stat"><strong>Todos los niveles</strong><span>tiempo de fondo &eacute;pico</span></div><div class="feature-stat"><strong>Macro</strong><span>pigmeos al lado</span></div></div>
      </div>
    </div>

    <div class="feature-row feature-row--flip" id="pyramids">
      <div class="feature-img"><img src="{WP}/2022/09/DiveMasterw.webp" alt="Buceadores sobre estructuras de arrecife en Amed" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">Dos cl&aacute;sicos de Amed</p>
        <h2>Las Pir&aacute;mides y el arrecife de Melasti</h2>
        <p>Las Pir&aacute;mides son estructuras de arrecife artificial sembradas en la arena frente a la playa de Amed, a un paso de Jemeluk, con dos d&eacute;cadas de crecimiento encima y repletas de peces cristal, peces le&oacute;n y tortugas de paso: una segunda inmersi&oacute;n brillante y nuestra aula de navegaci&oacute;n. Melasti es el arrecife al final de nuestro propio camino, una pendiente suave de coral y praderas con tortugas residentes, perfecta para una ma&ntilde;ana f&aacute;cil con log&iacute;stica cero.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>5&ndash;22 m</strong><span>Pir&aacute;mides</span></div><div class="feature-stat"><strong>4&ndash;20 m</strong><span>Melasti</span></div><div class="feature-stat"><strong>500 m</strong><span>Melasti desde la puerta</span></div></div>
      </div>
    </div>

    <div class="feature-row" id="coral-garden">
      <div class="feature-img"><img src="{WP}/2022/09/Nitrox.webp" alt="Buceador en Coral Garden, Tulamben" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">Los otros dos de Tulamben</p>
        <h2>Coral Garden y el Drop-Off</h2>
        <p>Coral Garden es la galer&iacute;a somera de Tulamben: estatuas y estructuras entre coral blando a 2&ndash;12 metros, llenas de vida, ideales para inmersiones largas y relajadas y las paradas de seguridad m&aacute;s bonitas de la costa. A diez minutos andando por la playa, el Drop-Off (los locales lo llaman The Wall) es el polo opuesto: roca volc&aacute;nica cayendo desde los 10 metros hasta m&aacute;s all&aacute; de los 40, colgada de gorgonias gigantes, con bancos de peces pegados a la pared y, de vez en cuando, algo grande saliendo del azul. Aqu&iacute; hacemos nuestra formaci&oacute;n profunda.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>2&ndash;12 m</strong><span>Coral Garden</span></div><div class="feature-stat"><strong>10&ndash;40 m</strong><span>Drop-Off</span></div><div class="feature-stat"><strong>Avanzado</strong><span>para lo mejor de la pared</span></div></div>
      </div>
    </div>

    <div class="feature-row feature-row--flip" id="seraya">
      <div class="feature-img"><img src="{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp" alt="Vida macro en arena negra, Seraya" loading="lazy"></div>
      <div class="feature-body">
        <p class="feature-kicker">Para cazadores de bichos &middot; Seraya</p>
        <h2>Seraya Secrets</h2>
        <p>Unos minutos antes de llegar a Tulamben por la carretera de la costa, Seraya es el icono del muck diving del este de Bali: una ladera de arena negra que parece vac&iacute;a y que premia los ojos lentos con peces sapo, gambas arlequ&iacute;n, peces pipa fantasma, caballitos y nudibranquios por docenas. Es otra disciplina, flotar quieto, buscar peque&ntilde;o, y con los ojos de bi&oacute;logo de Irman al lado, te estropea para siempre las inmersiones normales. En el buen sentido.</p>
        <div class="feature-stats"><div class="feature-stat"><strong>5&ndash;20 m</strong><span>profundidad</span></div><div class="feature-stat"><strong>Todos los niveles</strong><span>la flotabilidad ayuda</span></div><div class="feature-stat"><strong>Muck</strong><span>capital del bicheo</span></div></div>
      </div>
    </div>
"""

pages["amed-diving-guide-es.html"] = ("amed-diving-guide.html",
    "Guía de Buceo en Amed y Tulamben, Bali · Todos los Puntos, Sin Vender Humo | Diving La Vida Loca",
    "La guía completa para bucear en Amed y Tulamben, Bali: la historia y profundidades del pecio USAT Liberty, Jemeluk, el Pecio Japonés, el muck de Seraya y la mejor época, escrita en español por el centro que los bucea a diario.",
    hero(f"{WP}/2022/09/Advanced_open_water.webp",
         '<a href="index-es.html">Inicio</a> / <a href="dive-sites-es.html">Puntos de Inmersi&oacute;n</a> / Gu&iacute;a de Buceo',
         "Gu&iacute;a de Buceo de Amed y Tulamben",
         "Todo lo que sabemos de la costa que buceamos cada d&iacute;a: la historia del Liberty, profundidades reales, a qui&eacute;n le va cada punto, cu&aacute;ndo venir y los trucos locales que marcan la diferencia. Sin vender ning&uacute;n sitio m&aacute;s de lo que merece.")
    + facts([("13", "puntos en esta gu&iacute;a"), ("Desde la costa", "todas las inmersiones"), ("26&ndash;29&deg;C", "agua todo el a&ntilde;o"), ("15&ndash;30 m", "visibilidad en seca"), ("Abr&ndash;Nov", "temporada top")])
    + f"""
<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Por Qu&eacute; Esta Costa Es Especial</h2></div>
    <p class="section-sub">En el corto tramo de costa entre Amed y Tulamben caben un pecio de fama mundial, bah&iacute;as de coral, una pared que se desploma y muck diving sobre arena negra, todo entrando a pie desde playas de un mismo tramo de costa. Sin barcos ni trayectos largos: te metes andando, desciendes, y ya est&aacute;s. La arena volc&aacute;nica del Agung hace estallar los colores del coral y alimenta la vida macro que da fama a la zona.</p>
{guia_sitios.replace("{{WP}}".replace("{{","{").replace("}}","}"), WP)}


  </div>
</section>

<section class="more-sites">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">M&aacute;s Puntos Que Buceamos</h2></div>
    <p class="section-sub">Los ocho de arriba son el coraz&oacute;n de la costa; estos cinco completan el mapa para quien se queda m&aacute;s tiempo o busca algo concreto.</p>
    <div class="day-plan">
      <div class="day" id="boga"><h3>Pecio Boga &middot; Kubu &middot; 16&ndash;40 m</h3><p>Un carguero de 40 metros hundido a prop&oacute;sito en 2012 como arrecife artificial, diez minutos pasado Tulamben. Descansa adrizado, con estatuas en cubierta y un coche hundido de lo m&aacute;s surrealista; su profundidad lo convierte en inmersi&oacute;n para Advanced, ideal con Nitrox.</p></div>
      <div class="day" id="batu-kelebit"><h3>Batu Kelebit &middot; Tulamben &middot; 15&ndash;40 m</h3><p>Crestas rocosas que se hunden hacia el azul justo al este del Drop-Off: gorgonias grandes, bancos de peces y la mejor papeleta de la costa para que pase algo pel&aacute;gico. El lado salvaje de Tulamben, mejor con algo de experiencia.</p></div>
      <div class="day" id="bunutan"><h3>Bunutan &middot; Amed &middot; 10&ndash;30 m</h3><p>Una punta de arena en el tramo de Amed con colonias de anguilas jard&iacute;n, praderas y una pendiente suave hacia lo profundo, que solemos bucear como deriva f&aacute;cil. Discretamente excelente, y casi siempre vac&iacute;o.</p></div>
      <div class="day" id="lipah"><h3>Bah&iacute;a de Lipah &middot; Amed &middot; 3&ndash;20 m</h3><p>Una bah&iacute;a peque&ntilde;a de bommies de coral sobre arena, relajada y somera, tan buena para esn&oacute;rquel como para bucear. La cl&aacute;sica segunda inmersi&oacute;n f&aacute;cil volviendo del Pecio Japon&eacute;s.</p></div>
      <div class="day" id="gili-selang"><h3>Gili Selang &middot; la punta este de Bali &middot; 5&ndash;30 m</h3><p>El islote de la punta m&aacute;s oriental de Bali: coral intacto y potencial pel&aacute;gico de verdad, custodiados por corrientes fuertes e impredecibles. Solo buceadores avanzados, el d&iacute;a adecuado y con el plan adecuado. Preg&uacute;ntanos.</p></div>
    </div>
  </div>
</section>

<section class="page-section">
  <div class="container">
    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Cu&aacute;ndo Venir</h2></div>
    <p class="section-sub">En Amed se bucea todo el a&ntilde;o. La estaci&oacute;n seca, de abril a noviembre, trae la mejor visibilidad (a menudo 15&ndash;30 metros) y ma&ntilde;anas de espejo; la de lluvias es m&aacute;s tranquila y perfectamente buceable, con visibilidad que var&iacute;a seg&uacute;n el d&iacute;a. El agua va de 26 a 29&deg;C sea el mes que sea: con un 3 mm vas sobrado. Las ma&ntilde;anas casi siempre dan las mejores condiciones del d&iacute;a, que es justo como nos gusta trabajar.</p>

    <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">Bueno Saberlo</h2></div>
    <p class="section-sub">Las entradas son sobre arena negra y cantos, as&iacute; que los escarpines son equipo de serie (los nuestros van incluidos, como todo). Las corrientes en esta costa suelen ser suaves, por eso es tan buen sitio para aprender. Y la etiqueta con el arrecife aqu&iacute; va en serio: flotabilidad perfecta antes que c&aacute;maras grandes, nada se toca, nada se persigue. Del arrecife comemos todos.</p>

    <h2 style="font-size:1.5rem; margin:2.5rem 0 1.2rem;">Lo que preguntan los buceadores sobre esta costa</h2>
    <div class="faq">
      <details><summary>&iquest;Puede un principiante bucear el pecio Liberty?</summary><p>S&iacute;. El pecio empieza sobre los 5 metros, as&iacute; que con el Open Water, e incluso con esn&oacute;rquel, ves much&iacute;simo. La popa profunda y los pasajes son el motivo por el que casi todos lo combinan con el curso Advanced.</p></details>
      <details><summary>&iquest;Cu&aacute;l es la mejor hora para el Liberty?</summary><p>El amanecer, sin discusi&oacute;n. Los peces loro cabez&oacute;n a&uacute;n patrullan, las excursiones del sur de Bali no han llegado, y la luz entrando por la superestructura es la foto que vienes buscando. Alojarse en Amed lo pone f&aacute;cil.</p></details>
      <details><summary>&iquest;Hay corriente en Amed y Tulamben?</summary><p>Generalmente suave, por eso esta costa es ideal para cursos y buceo tranquilo. Las condiciones cambian a diario y el briefing de cada ma&ntilde;ana es honesto. Si un punto tiene un mal d&iacute;a, vamos a otro mejor.</p></details>
      <details><summary>&iquest;Hace falta barco para alguno de estos puntos?</summary><p>No. Todos los puntos de esta gu&iacute;a son de entrada desde la costa: esa es la magia de esta zona. Entras andando desde la playa con tu gu&iacute;a, m&aacute;ximo cuatro buceadores.</p></details>
      <details><summary>&iquest;Cu&aacute;ndo es temporada de mola mola en Amed?</summary><p>Amed no es destino de molas ni grandes pel&aacute;gicos: ese es el terreno de Nusa Penida. Lo que esta costa hace mejor que casi nadie: pecios, coral somero sano, vida macro y un buceo f&aacute;cil y precioso que puedes repetir tres veces al d&iacute;a.</p></details>
    </div>

    <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text=Hola!%20He%20le%C3%ADdo%20vuestra%20gu%C3%ADa%20de%20buceo.%20Mis%20fechas%20y%20nivel%3A">Planifica tus inmersiones con nosotros</a></div>
  </div>
</section>
"""
    + quote("El mar, una vez lanzado su hechizo, te atrapa para siempre en su red de asombro.", "Jacques-Yves Cousteau"),
)



# ─────────────────────────── CREA TU VIAJE ───────────────────────────
pages["plan-your-trip-es.html"] = ("plan-your-trip.html",
    "Crea Tu Viaje de Buceo en Amed, Bali · Presupuesto al Instante | Diving La Vida Loca",
    "Responde tres preguntas y consigue un presupuesto al instante para bucear en Amed, Bali: cursos, inmersiones y packs aloja y bucea. Precios reales, sin compromiso, confirmado por WhatsApp.",
    hero(f"{WP}/2022/09/Open_water_padi.webp",
         '<a href="index-es.html">Inicio</a> / Crea tu Viaje',
         "Crea Tu Viaje",
         "Tres preguntas, una estimaci&oacute;n honesta sacada de nuestra lista de precios real, y tu plan llega a nuestro WhatsApp listo para confirmar. Lo de hecho a medida va en serio: esto solo arranca la conversaci&oacute;n.")
    + f"""
<section class="page-section">
  <div class="container wiz-wrap">
    <div id="wizard" class="wiz-card"></div>
  </div>
</section>
<script src="wizard.js?v=9" defer></script>
"""
    + quote("Sentimos que no pod&iacute;amos haber elegido un sitio mejor.", "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas"),
)

for fname, (en_url, title, desc, body) in pages.items():
    schema = _faq_schema(body)
    if fname.startswith("course-"):
        schema += _course_schema(title, desc, BASE + fname)
    html = (HEAD.replace("{{TITLE}}", title).replace("{{DESC}}", desc) + body + FOOT)
    html = (html.replace("{{EN_URL}}", en_url)
                .replace("{{SELF}}", BASE + fname)
                .replace("{{EN_ABS}}", BASE + en_url)
                .replace("{{ES_ABS}}", BASE + fname)
                .replace("{{SCHEMA}}", schema))
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)
    print(f"wrote {fname} ({len(html)} bytes)")
