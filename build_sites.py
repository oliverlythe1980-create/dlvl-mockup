#!/usr/bin/env python3
"""Generates individual dive-site article pages (EN + ES) for the diving guide.
Content grounded in current public dive-site references (2026); shop framing added.
Reuses HEAD/FOOT from build.py and build_es.py for exact consistency."""
import os, json, html as _html, re

import build as _b          # noqa: imports also regenerate main pages (harmless)
import build_es as _be

OUT = os.path.dirname(os.path.abspath(__file__))
WP = "https://divinglavidaloca.com/wp-content/uploads"
WA = "https://wa.me/6282145538716"
BASE = "https://divinglavidaloca.com/"
G3904 = f"{WP}/2024/07/g390496193bc5ff85ec056dccfdff8a3ed9468489c1b0181b34acd7a160d79bb7ede477176a73be0aa3a047b7ccbe434b89c09aaee0cf6fa17ed85353bc4426ba_1280-1049477-1024x683.webp"

HEAD_EN, FOOT_EN = _b.HEAD, _b.FOOT
HEAD_ES, FOOT_ES = _be.HEAD, _be.FOOT


def clean(s):
    return _html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def facts_bar(items):
    cells = "\n".join(
        f'    <div class="fact"><strong>{a}</strong><span>{b}</span></div>' for a, b in items
    )
    return f'<section class="facts-bar" aria-label="Key facts">\n  <div class="facts-inner">\n{cells}\n  </div>\n</section>\n'


def faq_block(faqs):
    rows = "".join(
        f"\n      <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    return f'<div class="faq">{rows}\n    </div>'


def body(lang, s, prev, nxt):
    en = lang == "en"
    d = s[lang]
    sfx = "" if en else "-es"
    nav_label = "More dive sites" if en else "Mas puntos"
    all_sites = "All sites" if en else "Todos los puntos"
    if prev:
        prev_html = '<a class="sn-prev" href="site-' + prev["slug"] + sfx + '.html">&larr; ' + prev[lang]["name"] + '</a>'
    else:
        prev_html = '<span class="sn-prev"></span>'
    if nxt:
        next_html = '<a class="sn-next" href="site-' + nxt["slug"] + sfx + '.html">' + nxt[lang]["name"] + ' &rarr;</a>'
    else:
        next_html = '<span class="sn-next"></span>'
    guide = "amed-diving-guide.html" if en else "amed-diving-guide-es.html"
    crumb_home = "Home" if en else "Inicio"
    crumb_guide = "Diving Guide" if en else "Gu&iacute;a de Buceo"
    idx = "index.html" if en else "index-es.html"
    h_site = "The Site" if en else "El Punto"
    h_see = "What You&rsquo;ll See" if en else "Qu&eacute; Ver&aacute;s"
    h_cond = "Conditions &amp; When to Dive It" if en else "Condiciones y Cu&aacute;ndo Bucearlo"
    h_how = "How We Dive It" if en else "C&oacute;mo Lo Buceamos"
    h_faq = "Good to Know" if en else "Bueno Saberlo"
    overview = "\n    ".join(f"<p>{p}</p>" for p in d["overview"])
    see = "".join(f"\n      <li>{x}</li>" for x in d["see"])
    cta = ("Plan a dive here" if en else "Planifica una inmersi&oacute;n aqu&iacute;")
    back = ("&larr; Back to the diving guide" if en else "&larr; Volver a la gu&iacute;a de buceo")
    wa_text = ("Hi!%20I%27d%20like%20to%20dive%20" if en else "Hola!%20Quiero%20bucear%20") + s["slug"].replace("-", "%20")
    return f"""
<section class="course-hero">
  <img class="bg" src="{s['img']}" alt="" aria-hidden="true" fetchpriority="high">
  <div class="container course-hero-body">
    <p class="breadcrumb"><a href="{idx}">{crumb_home}</a> / <a href="{guide}">{crumb_guide}</a> / {d['name']}</p>
    <h1>{d['name']}</h1>
    <p class="lede">{d['lede']}</p>
  </div>
</section>
{facts_bar(d['facts'])}
<section class="page-section">
  <div class="container">
    <div class="course-content" style="max-width: 780px; margin: 0 auto;">
      <div class="section-hed"><span class="section-rule"></span><h2 class="section-title">{h_site}</h2></div>
    {overview}
      <h2>{h_see}</h2>
      <ul>{see}
      </ul>
      <h2>{h_cond}</h2>
      <p>{d['conditions']}</p>
      <h2>{h_how}</h2>
      <p>{d['how']}</p>
      <h2>{h_faq}</h2>
      {faq_block(d['faqs'])}
      <div class="section-cta"><a class="pill-btn pill-btn--whatsapp" href="{WA}?text={wa_text}">{cta}</a></div>
      <nav class="site-nav-prevnext" aria-label="{nav_label}">
        {prev_html}
        <a class="sn-all" href="{guide}">{all_sites}</a>
        {next_html}
      </nav>
    </div>
  </div>
</section>
<section class="hp-quote">
  <div class="container">
    <p class="quote-text">&ldquo;{d['quote']}&rdquo;</p>
    <span class="quote-attribution">{d['quote_by']}</span>
  </div>
</section>
"""


# ─────────────────────────── SITE DATA ───────────────────────────
# img reuse from the shop's media; depths/levels/history from public 2026 references.
SITES = [
  {
    "slug": "liberty", "img": f"{WP}/2022/09/Advanced_open_water.webp",
    "en": {
      "name": "USAT Liberty Wreck",
      "lede": "A 120-metre WWII shipwreck you walk to from the beach. Coral-blanketed, bumphead parrotfish at dawn, and one of the easiest great wreck dives on earth.",
      "facts": [("5&ndash;30 m", "depth"), ("All levels", "snorkellers too"), ("Shore entry", "Tulamben"), ("Dawn", "best time"), ("~25 min", "by car")],
      "overview": [
        "The USAT Liberty is the reason most divers have heard of this coast. A 120-metre United States Army cargo ship, she was torpedoed by a Japanese submarine on 11 January 1942 while crossing the Lombok Strait carrying rubber and railway parts. Two destroyers tried to tow her to Singaraja, but she was taking on too much water, so the crew beached her at Tulamben.",
        "She sat on the sand for twenty years until the 1963 eruption of Mount Agung shook her off the beach and into the sea, breaking her apart as she rolled down the slope. Today she lies parallel to the shore on a sandy slope between roughly 5 and 30 metres, completely colonised by hard and soft coral, gorgonians and sponges.",
        "Entry is a short walk over the black-sand beach and a 30-metre surface swim. The top of the wreck sits at around 5 metres, so snorkellers and Open Water divers see plenty, while the deeper stern and swim-throughs reward Advanced divers.",
      ],
      "see": [
        "The resident school of bumphead parrotfish that patrols the wreck at first light",
        "Green and hawksbill turtles, often resting on the structure",
        "Gorgonian fans, barrel sponges and dense soft coral over the whole hull",
        "Great barracuda, schooling jacks and garden eels on the surrounding sand",
        "Macro life on the plates: pygmy seahorses, nudibranchs and ghost pipefish",
      ],
      "conditions": "The Liberty dives year-round and suits every level. Visibility is typically 15&ndash;30 metres in the dry season (April to November). Currents are usually mild. Water sits at 26&ndash;29&deg;C, so a 3 mm suit is plenty.",
      "how": "We dive the Liberty at sunrise, before the day-trip buses arrive from south Bali, with four divers maximum. That means the bumpheads are still patrolling and the wreck is yours. Open Water divers tour the shallower sections; if you want the deep stern, we pair it with the Advanced course.",
      "faqs": [
        ("Can beginners dive the Liberty?", "Yes. The wreck starts at around 5 metres, so Open Water divers and even snorkellers see most of it. The deeper stern is the reason many continue with the Advanced course."),
        ("Why dive it at dawn?", "The bumphead parrotfish are still on the wreck, the south-Bali day-trippers haven&rsquo;t arrived, and the light through the structure is unbeatable. Staying in Amed makes the early slot easy."),
      ],
      "quote": "An authentic diving school, and I say that as a diving professional.",
      "quote_by": "Google review &middot; one of 508 five-star reviews",
    },
    "es": {
      "name": "Pecio del USAT Liberty",
      "lede": "Un pecio de 120 m de la II Guerra Mundial al que entras andando desde la playa. Forrado de coral, peces loro cabez&oacute;n al amanecer, y una de las inmersiones de pecio m&aacute;s f&aacute;ciles del mundo.",
      "facts": [("5&ndash;30 m", "profundidad"), ("Todos los niveles", "esn&oacute;rquel incl."), ("Desde costa", "Tulamben"), ("Amanecer", "mejor momento"), ("~25 min", "en coche")],
      "overview": [
        "El USAT Liberty es la raz&oacute;n por la que media comunidad buceadora conoce esta costa. Un carguero del ej&eacute;rcito estadounidense de 120 metros, torpedeado por un submarino japon&eacute;s el 11 de enero de 1942 cuando cruzaba el estrecho de Lombok cargado de caucho y piezas de ferrocarril. Dos destructores intentaron remolcarlo a Singaraja, pero hac&iacute;a demasiada agua, as&iacute; que la tripulaci&oacute;n lo var&oacute; en la playa de Tulamben.",
        "Pas&oacute; veinte a&ntilde;os sobre la arena hasta que la erupci&oacute;n del Agung en 1963 lo sacudi&oacute; al mar, parti&eacute;ndolo mientras rodaba por la ladera. Hoy descansa paralelo a la orilla sobre una pendiente de arena entre los 5 y los 30 metros, colonizado por completo de coral duro y blando, gorgonias y esponjas.",
        "La entrada es un paseo corto por la playa de arena negra y unos 30 metros nadando en superficie. La parte alta est&aacute; sobre los 5 metros, as&iacute; que esnorquelistas y buceadores Open Water ven much&iacute;simo, mientras que la popa honda y los pasajes premian a los Advanced.",
      ],
      "see": [
        "El banco residente de peces loro cabez&oacute;n que patrulla el pecio al amanecer",
        "Tortugas verdes y carey, a menudo posadas en la estructura",
        "Gorgonias, esponjas barril y coral blando denso por todo el casco",
        "Barracudas, bancos de j&uacute;reles y anguilas jard&iacute;n en la arena de alrededor",
        "Vida macro en las planchas: caballitos pigmeos, nudibranquios y peces pipa fantasma",
      ],
      "conditions": "El Liberty se bucea todo el a&ntilde;o y vale para todos los niveles. La visibilidad suele ser de 15&ndash;30 metros en la estaci&oacute;n seca (abril a noviembre). Las corrientes son normalmente suaves. El agua est&aacute; a 26&ndash;29&deg;C: con un 3 mm vas sobrado.",
      "how": "Buceamos el Liberty al amanecer, antes de que lleguen los autobuses del sur de Bali, con cuatro buceadores como m&aacute;ximo. As&iacute; los cabezones siguen patrullando y el pecio es tuyo. Los Open Water recorren la parte somera; si quieres la popa honda, lo combinamos con el curso Advanced.",
      "faqs": [
        ("&iquest;Puede un principiante bucear el Liberty?", "S&iacute;. El pecio empieza sobre los 5 metros, as&iacute; que los Open Water e incluso los esnorquelistas ven casi todo. La popa honda es el motivo por el que muchos siguen con el Advanced."),
        ("&iquest;Por qu&eacute; bucearlo al amanecer?", "Los peces loro cabez&oacute;n siguen en el pecio, las excursiones del sur de Bali no han llegado, y la luz entre la estructura es inmejorable. Alojarse en Amed pone f&aacute;cil el turno temprano."),
      ],
      "quote": "Una escuela de buceo aut&eacute;ntica, y lo digo como profesional del buceo.",
      "quote_by": "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas",
    },
  },
  {
    "slug": "coral-garden", "img": f"{WP}/2022/09/Nitrox.webp",
    "en": {
      "name": "Coral Garden",
      "lede": "Tulamben&rsquo;s shallow sculpture garden: statues and structures among soft coral, all within easy reach of the surface. A photographer&rsquo;s playground.",
      "facts": [("2&ndash;12 m", "depth"), ("All levels", "snorkellers too"), ("Shore entry", "Tulamben"), ("Photos &amp; night", "best for"), ("~25 min", "by car")],
      "overview": [
        "A short walk from the Liberty, Coral Garden is a gentle, shallow site seeded with statues and artificial-reef structures that have grown into a thriving coral community. Depths run from 2 to about 12 metres, which makes it endlessly relaxed and ideal for long dives and the prettiest safety stops on the coast.",
        "It&rsquo;s a favourite for underwater photographers and a brilliant night dive, when the reef&rsquo;s nocturnal residents come out to play.",
      ],
      "see": [
        "Submerged statues slowly disappearing under soft coral",
        "Anemones and clownfish, anthias clouds and reef fish",
        "Turtles passing through, and the occasional blacktip in the shallows",
        "Night-dive specials: Spanish dancers, crabs, hunting lionfish",
      ],
      "conditions": "Shallow, sheltered and calm, with gentle currents and good light. Suits everyone from first-timers to macro photographers. Visibility 10&ndash;25 metres; warm water all year.",
      "how": "We use Coral Garden as a relaxed second dive, a night dive, and a calm classroom for buoyancy and photography. With a maximum of four divers, you get the unhurried pace these shallow sites are made for.",
      "faqs": [
        ("Is Coral Garden good for snorkelling?", "Yes, it&rsquo;s shallow enough that non-diving partners can enjoy it from the surface while you dive."),
        ("Can I do a night dive here?", "Absolutely, it&rsquo;s one of our favourite night dives. Ask us to add one to your plan."),
      ],
      "quote": "With knowing comes caring, and with caring there is hope.",
      "quote_by": "Dr Sylvia Earle",
    },
    "es": {
      "name": "Coral Garden",
      "lede": "El jard&iacute;n de esculturas somero de Tulamben: estatuas y estructuras entre coral blando, todo al alcance de la superficie. Un parque de juegos para fot&oacute;grafos.",
      "facts": [("2&ndash;12 m", "profundidad"), ("Todos los niveles", "esn&oacute;rquel incl."), ("Desde costa", "Tulamben"), ("Fotos y noche", "ideal para"), ("~25 min", "en coche")],
      "overview": [
        "A un paseo del Liberty, Coral Garden es un punto suave y somero sembrado de estatuas y estructuras de arrecife artificial que se han convertido en una comunidad de coral rebosante. Las profundidades van de los 2 a los 12 metros, lo que lo hace infinitamente tranquilo e ideal para inmersiones largas y las paradas de seguridad m&aacute;s bonitas de la costa.",
        "Es un favorito de los fot&oacute;grafos submarinos y una inmersi&oacute;n nocturna brillante, cuando salen los habitantes nocturnos del arrecife.",
      ],
      "see": [
        "Estatuas sumergidas desapareciendo poco a poco bajo el coral blando",
        "An&eacute;monas y peces payaso, nubes de anthias y peces de arrecife",
        "Tortugas de paso y alg&uacute;n punta negra en lo somero",
        "Especiales de nocturna: bailarinas espa&ntilde;olas, cangrejos, peces le&oacute;n cazando",
      ],
      "conditions": "Somero, resguardado y tranquilo, con corrientes suaves y buena luz. Vale para todos, desde principiantes hasta fot&oacute;grafos macro. Visibilidad 10&ndash;25 metros; agua c&aacute;lida todo el a&ntilde;o.",
      "how": "Usamos Coral Garden como segunda inmersi&oacute;n relajada, nocturna y aula tranquila de flotabilidad y fotograf&iacute;a. Con cuatro buceadores como m&aacute;ximo, tienes el ritmo pausado para el que estos sitios someros est&aacute;n hechos.",
      "faqs": [
        ("&iquest;Coral Garden vale para esn&oacute;rquel?", "S&iacute;, es lo bastante somero para que la pareja no buceadora lo disfrute desde la superficie mientras buceas."),
        ("&iquest;Puedo hacer una nocturna aqu&iacute;?", "Por supuesto, es una de nuestras nocturnas favoritas. P&iacute;denos a&ntilde;adirla a tu plan."),
      ],
      "quote": "Con el conocimiento llega el cari&ntilde;o, y con el cari&ntilde;o, la esperanza.",
      "quote_by": "Dra. Sylvia Earle",
    },
  },
  {
    "slug": "drop-off", "img": f"{WP}/2022/09/Advanced_open_water.webp",
    "en": {
      "name": "Tulamben Drop-Off",
      "lede": "Volcanic rock plunging into the blue. Giant gorgonians, schooling fish against the wall, and the occasional something-big out of the depths.",
      "facts": [("10&ndash;40 m", "depth"), ("Advanced", "for the wall"), ("Shore entry", "Tulamben"), ("Wall dive", "type"), ("~25 min", "by car")],
      "overview": [
        "Locally known as The Wall, the Tulamben Drop-Off begins in the shallows and falls away steeply, continuing well past 70 metres (recreational dives stay at a maximum of 30). The wall is hung with giant gorgonian fans, black coral and sponges, with schooling fish stacked along it and the occasional pelagic cruising out of the blue.",
        "It&rsquo;s the most dramatic of Tulamben&rsquo;s shore dives and our classroom for deep training.",
      ],
      "see": [
        "Huge gorgonian sea fans and black coral bushes",
        "Schooling fusiliers, snapper and trevally along the wall",
        "Reef sharks and larger pelagics on the deeper edge",
        "Macro on the wall: pygmy seahorses, nudibranchs, shrimp",
      ],
      "conditions": "Best enjoyed by Advanced divers because of the depth. Currents are usually gentle but can pick up; we brief honestly each morning. Visibility 15&ndash;30 metres in the dry season.",
      "how": "The Drop-Off is where we run the deep dive of the Advanced course and Deep Diver speciality. With four divers maximum we descend together along the wall, watching how you feel the whole way down.",
      "faqs": [
        ("Do I need to be Advanced?", "To enjoy the wall properly, yes, the best of it is below 18 metres. Open Water divers can dive the shallower top section."),
        ("Are there sharks?", "White-tip reef sharks are seen along the deeper edge, and you never know what passes by from the blue."),
      ],
      "quote": "The sea, once it casts its spell, holds one in its net of wonder forever.",
      "quote_by": "Jacques-Yves Cousteau",
    },
    "es": {
      "name": "Drop-Off de Tulamben",
      "lede": "Roca volc&aacute;nica desplom&aacute;ndose en el azul. Gorgonias gigantes, bancos de peces pegados a la pared y, de vez en cuando, algo grande saliendo de lo hondo.",
      "facts": [("10&ndash;40 m", "profundidad"), ("Avanzado", "para la pared"), ("Desde costa", "Tulamben"), ("Pared", "tipo"), ("~25 min", "en coche")],
      "overview": [
        "Conocido localmente como The Wall, el Drop-Off de Tulamben empieza en lo somero y cae en picado, siguiendo m&aacute;s all&aacute; de los 70 metros (las inmersiones recreativas se quedan en un m&aacute;ximo de 30). La pared est&aacute; colgada de gorgonias gigantes, coral negro y esponjas, con bancos de peces pegados a ella y alg&uacute;n pel&aacute;gico saliendo del azul.",
        "Es la m&aacute;s espectacular de las inmersiones desde costa de Tulamben y nuestra aula para la formaci&oacute;n profunda.",
      ],
      "see": [
        "Enormes gorgonias y matas de coral negro",
        "Bancos de fusileros, pargos y jureles a lo largo de la pared",
        "Tiburones de arrecife y pel&aacute;gicos mayores en el borde profundo",
        "Macro en la pared: caballitos pigmeos, nudibranquios, gambas",
      ],
      "conditions": "Mejor para buceadores Advanced por la profundidad. Las corrientes suelen ser suaves pero pueden subir; el briefing de cada ma&ntilde;ana es honesto. Visibilidad 15&ndash;30 metros en seca.",
      "how": "El Drop-Off es donde hacemos la inmersi&oacute;n profunda del curso Advanced y la especialidad Deep Diver. Con cuatro buceadores como m&aacute;ximo, bajamos juntos por la pared, pendientes de c&oacute;mo te encuentras todo el descenso.",
      "faqs": [
        ("&iquest;Necesito ser Advanced?", "Para disfrutar la pared de verdad, s&iacute;: lo mejor est&aacute; por debajo de los 18 metros. Los Open Water pueden bucear la parte alta somera."),
        ("&iquest;Hay tiburones?", "Se ven tiburones punta blanca en el borde profundo, y nunca se sabe qu&eacute; pasa desde el azul."),
      ],
      "quote": "El mar, una vez lanzado su hechizo, te atrapa para siempre en su red de asombro.",
      "quote_by": "Jacques-Yves Cousteau",
    },
  },
  {
    "slug": "batu-kelebit", "img": f"{WP}/2022/09/DiveMasterw.webp",
    "en": {
      "name": "Batu Kelebit",
      "lede": "Deep ridges and pinnacles east of the Drop-Off, where the coast&rsquo;s best chance of pelagics cruises the open water.",
      "facts": [("15&ndash;40 m", "depth"), ("Advanced", "level"), ("Shore entry", "Tulamben"), ("Pelagics", "highlight"), ("~25 min", "by car")],
      "overview": [
        "Just east of the Drop-Off, Batu Kelebit features two large submerged pinnacles rising from a sandy bottom at around 40 metres to a shallower reef at 18&ndash;20 metres. The site drops beyond 60 metres, with an average dive depth around 25 metres.",
        "Currents are generally light and visibility runs 10&ndash;30 metres. It&rsquo;s Tulamben&rsquo;s wilder edge, best with some experience, and the coast&rsquo;s strongest chance of meeting something big.",
      ],
      "see": [
        "Two coral-covered pinnacles and a healthy ridge reef",
        "Schooling tuna, trevally and barracuda over the deep",
        "Reef sharks and the occasional larger pelagic",
        "Gorgonians and sea fans on the deeper structure",
      ],
      "conditions": "Best for intermediate and advanced divers due to depth and open-water conditions. Light currents are possible. Visibility 10&ndash;30 metres; warm year-round.",
      "how": "We dive Batu Kelebit with experienced divers chasing the blue-water encounters. Four divers maximum, a clear plan, and an honest read on the day&rsquo;s conditions before we go.",
      "faqs": [
        ("What level do I need?", "Advanced, or solid experience, because of the depth and the open-water setting."),
        ("What might I see in the blue?", "Tuna and trevally are regular; reef sharks and larger pelagics turn up on the right day."),
      ],
      "quote": "We feel like we could not have picked a better place.",
      "quote_by": "Google review &middot; one of 508 five-star reviews",
    },
    "es": {
      "name": "Batu Kelebit",
      "lede": "Crestas profundas y pin&aacute;culos al este del Drop-Off, donde la mejor papeleta de la costa para ver pel&aacute;gicos cruza el agua azul.",
      "facts": [("15&ndash;40 m", "profundidad"), ("Avanzado", "nivel"), ("Desde costa", "Tulamben"), ("Pel&aacute;gicos", "lo mejor"), ("~25 min", "en coche")],
      "overview": [
        "Justo al este del Drop-Off, Batu Kelebit tiene dos grandes pin&aacute;culos sumergidos que se alzan desde un fondo de arena sobre los 40 metros hasta un arrecife m&aacute;s somero a 18&ndash;20 metros. El punto cae m&aacute;s all&aacute; de los 60 metros, con una profundidad media de unos 25.",
        "Las corrientes suelen ser suaves y la visibilidad va de 10 a 30 metros. Es el lado m&aacute;s salvaje de Tulamben, mejor con algo de experiencia, y la mayor opci&oacute;n de la costa de cruzarte con algo grande.",
      ],
      "see": [
        "Dos pin&aacute;culos cubiertos de coral y una cresta de arrecife sana",
        "Bancos de at&uacute;n, jureles y barracudas sobre lo hondo",
        "Tiburones de arrecife y alg&uacute;n pel&aacute;gico mayor",
        "Gorgonias y abanicos de mar en la estructura profunda",
      ],
      "conditions": "Mejor para buceadores intermedios y avanzados por la profundidad y el entorno de mar abierto. Posibles corrientes suaves. Visibilidad 10&ndash;30 metros; c&aacute;lido todo el a&ntilde;o.",
      "how": "Buceamos Batu Kelebit con buceadores con experiencia que buscan los encuentros en agua azul. Cuatro buceadores como m&aacute;ximo, un plan claro y una lectura honesta de las condiciones del d&iacute;a antes de ir.",
      "faqs": [
        ("&iquest;Qu&eacute; nivel necesito?", "Advanced, o experiencia s&oacute;lida, por la profundidad y el entorno de mar abierto."),
        ("&iquest;Qu&eacute; podr&iacute;a ver en el azul?", "At&uacute;n y jureles son habituales; tiburones de arrecife y pel&aacute;gicos mayores aparecen el d&iacute;a adecuado."),
      ],
      "quote": "Sentimos que no pod&iacute;amos haber elegido un sitio mejor.",
      "quote_by": "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas",
    },
  },
  {
    "slug": "boga", "img": f"{WP}/2022/09/Advanced_open_water.webp",
    "en": {
      "name": "Boga Wreck",
      "lede": "A 40-metre former Dutch cargo vessel sunk in 2012 as an artificial reef, sitting upright on the sand off Kubu, north of Tulamben.",
      "facts": [("16&ndash;38 m", "depth"), ("Advanced", "Nitrox ideal"), ("Shore entry", "Kubu"), ("Artificial reef", "type"), ("~30 min", "by car")],
      "overview": [
        "Also called the Kubu Wreck, the Boga is a roughly 40-metre former Dutch cargo and patrol vessel deliberately sunk in September 2012 off Kubu, just north of Tulamben, to create an artificial reef and ease pressure on the Liberty.",
        "She sits upright on a sandy slope between about 16 and 38 metres, around 30 metres from shore. After more than a decade underwater she&rsquo;s well grown-in, and her depth makes this an Advanced dive, ideally on Nitrox for the bottom time.",
      ],
      "see": [
        "An intact, upright wreck you can swim the length of",
        "Growing soft coral, sponges and schooling reef fish",
        "Moray eels, lionfish, groupers and sweetlips around the structure",
        "Stingrays and flounder on the surrounding sand",
      ],
      "conditions": "An Advanced dive because of depth. No strong currents, clear water and warm temperatures. Nitrox strongly recommended to make the most of the bottom time.",
      "how": "We dive the Boga as a deep dive for Advanced divers and Deep/Nitrox speciality students. Four divers maximum, a planned profile, and Nitrox available to stretch your time on the wreck.",
      "faqs": [
        ("How is it different from the Liberty?", "It&rsquo;s deeper, intact and upright, and far quieter, an Advanced wreck rather than an all-levels one."),
        ("Do I need Nitrox?", "Not required, but strongly recommended, the wreck&rsquo;s depth means Nitrox gives you noticeably more time on it."),
      ],
      "quote": "Welcoming, kind and helpful. An amazing experience from start to finish.",
      "quote_by": "Google review &middot; one of 508 five-star reviews",
    },
    "es": {
      "name": "Pecio Boga",
      "lede": "Un antiguo carguero holand&eacute;s de 40 metros hundido en 2012 como arrecife artificial, adrizado sobre la arena frente a Kubu, al norte de Tulamben.",
      "facts": [("16&ndash;38 m", "profundidad"), ("Avanzado", "Nitrox ideal"), ("Desde costa", "Kubu"), ("Arrecife artificial", "tipo"), ("~30 min", "en coche")],
      "overview": [
        "Tambi&eacute;n llamado el pecio de Kubu, el Boga es un antiguo buque de carga y patrulla holand&eacute;s de unos 40 metros hundido a prop&oacute;sito en septiembre de 2012 frente a Kubu, justo al norte de Tulamben, para crear un arrecife artificial y aliviar la presi&oacute;n sobre el Liberty.",
        "Descansa adrizado sobre una pendiente de arena entre los 16 y los 38 metros, a unos 30 metros de la orilla. Tras m&aacute;s de una d&eacute;cada bajo el agua est&aacute; bien colonizado, y su profundidad lo convierte en inmersi&oacute;n Advanced, ideal con Nitrox por el tiempo de fondo.",
      ],
      "see": [
        "Un pecio &iacute;ntegro y adrizado que puedes recorrer de proa a popa",
        "Coral blando en crecimiento, esponjas y bancos de peces de arrecife",
        "Morenas, peces le&oacute;n, m&eacute;ros y burros alrededor de la estructura",
        "Rayas l&aacute;tigo y lenguados sobre la arena de alrededor",
      ],
      "conditions": "Inmersi&oacute;n Advanced por la profundidad. Sin corrientes fuertes, agua clara y temperatura c&aacute;lida. Nitrox muy recomendable para aprovechar el tiempo de fondo.",
      "how": "Buceamos el Boga como inmersi&oacute;n profunda para Advanced y alumnos de las especialidades Deep/Nitrox. Cuatro buceadores como m&aacute;ximo, un perfil planificado y Nitrox disponible para estirar tu tiempo en el pecio.",
      "faqs": [
        ("&iquest;En qu&eacute; se diferencia del Liberty?", "Es m&aacute;s profundo, &iacute;ntegro y adrizado, y mucho m&aacute;s tranquilo: un pecio Advanced en vez de para todos los niveles."),
        ("&iquest;Necesito Nitrox?", "No es obligatorio, pero muy recomendable: por la profundidad, el Nitrox te da bastante m&aacute;s tiempo en &eacute;l."),
      ],
      "quote": "Acogedores, amables y siempre pendientes. Una experiencia incre&iacute;ble de principio a fin.",
      "quote_by": "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas",
    },
  },
  {
    "slug": "seraya", "img": G3904,
    "en": {
      "name": "Seraya Secrets",
      "lede": "The muck-diving icon of east Bali: a black-sand slope that rewards slow eyes with frogfish, mimic octopus and harlequin shrimp.",
      "facts": [("5&ndash;25 m", "depth"), ("All levels", "macro patience"), ("Shore entry", "Seraya"), ("Muck &amp; macro", "type"), ("~20 min", "by car")],
      "overview": [
        "A short drive before Tulamben, Seraya Secrets is one of the best macro dive sites in Southeast Asia. The featureless-looking black-sand slope is exactly the point: slow right down and it reveals an extraordinary cast of small, strange creatures.",
        "It&rsquo;s actually three sites in one, easily reached from shore: Top Secrets (the muck classic), Noisy Reef (more hard coral in the shallows) and Deep Secrets (a chance of larger pelagics deeper down). Maximum depth is around 25 metres, though most divers stay above 22 to maximise hunting time.",
      ],
      "see": [
        "Frogfish, including the tiny hairy frogfish",
        "Mimic and coconut octopus for the lucky and patient",
        "Harlequin shrimp, ghost pipefish and seahorses",
        "Nudibranchs by the dozen, mantis shrimp and ribbon eels",
      ],
      "conditions": "Weak current and good visibility (10&ndash;30 metres) make it accessible to all levels, though good buoyancy and patience help enormously. A torch reveals the colours hiding in the sand.",
      "how": "We dive Seraya slow, with four divers maximum and Irman&rsquo;s biologist eyes leading the hunt. He finds things you&rsquo;d swim straight past, it changes how you dive forever.",
      "faqs": [
        ("What is muck diving?", "Diving over sand and silt rather than coral, hunting for rare, well-camouflaged macro life. It&rsquo;s slow, absorbing and addictive."),
        ("Do I need a camera?", "No, but most people wish they had one. A macro setup and a torch make Seraya unforgettable."),
      ],
      "quote": "With knowing comes caring, and with caring there is hope.",
      "quote_by": "Dr Sylvia Earle",
    },
    "es": {
      "name": "Seraya Secrets",
      "lede": "El icono del muck diving del este de Bali: una ladera de arena negra que premia los ojos lentos con peces sapo, pulpo mimo y gambas arlequ&iacute;n.",
      "facts": [("5&ndash;25 m", "profundidad"), ("Todos los niveles", "paciencia macro"), ("Desde costa", "Seraya"), ("Muck y macro", "tipo"), ("~20 min", "en coche")],
      "overview": [
        "A poco antes de Tulamben, Seraya Secrets es uno de los mejores puntos macro del sudeste asi&aacute;tico. La ladera de arena negra que parece vac&iacute;a es justo la gracia: baja el ritmo y revela un reparto extraordinario de criaturas peque&ntilde;as y rar&iacute;simas.",
        "En realidad son tres puntos en uno, f&aacute;ciles desde costa: Top Secrets (el cl&aacute;sico del muck), Noisy Reef (m&aacute;s coral duro en lo somero) y Deep Secrets (opci&oacute;n de pel&aacute;gicos mayores m&aacute;s abajo). La profundidad m&aacute;xima ronda los 25 metros, aunque casi todos se quedan por encima de los 22 para maximizar el tiempo de b&uacute;squeda.",
      ],
      "see": [
        "Peces sapo, incluido el diminuto pez sapo peludo",
        "Pulpo mimo y pulpo de cocotero para los pacientes con suerte",
        "Gambas arlequ&iacute;n, peces pipa fantasma y caballitos",
        "Nudibranquios por docenas, galeras y anguilas cinta",
      ],
      "conditions": "La corriente d&eacute;bil y la buena visibilidad (10&ndash;30 metros) lo hacen accesible a todos los niveles, aunque la buena flotabilidad y la paciencia ayudan much&iacute;simo. Un foco revela los colores escondidos en la arena.",
      "how": "Buceamos Seraya despacio, con cuatro buceadores como m&aacute;ximo y los ojos de bi&oacute;logo de Irman guiando la b&uacute;squeda. Encuentra cosas que pasar&iacute;as nadando de largo: te cambia la forma de bucear para siempre.",
      "faqs": [
        ("&iquest;Qu&eacute; es el muck diving?", "Bucear sobre arena y fango en vez de coral, buscando vida macro rara y muy camuflada. Es lento, absorbente y adictivo."),
        ("&iquest;Necesito c&aacute;mara?", "No, pero casi todos desear&iacute;an tener una. Un equipo macro y un foco hacen de Seraya algo inolvidable."),
      ],
      "quote": "Con el conocimiento llega el cari&ntilde;o, y con el cari&ntilde;o, la esperanza.",
      "quote_by": "Dra. Sylvia Earle",
    },
  },
  {
    "slug": "jemeluk", "img": G3904,
    "en": {
      "name": "Jemeluk Bay",
      "lede": "Our house reef: calm, shallow coral gardens sloping to a wall, where every Open Water student takes their first breaths in the sea.",
      "facts": [("3&ndash;25 m", "depth"), ("All levels", "first dives"), ("Shore entry", "Amed"), ("House reef", "our daily"), ("On the doorstep", "Amed")],
      "overview": [
        "Jemeluk is the bay the village of Amed curls around, and the hub of the whole coast. Calm, shallow coral gardens start at three metres and slope to a wall that drops past 25 metres at the eastern point.",
        "It&rsquo;s where every Open Water student takes their first breaths in the sea, and the snorkelling is good enough that non-diving partners don&rsquo;t feel left out. It&rsquo;s also where we go on our days off.",
      ],
      "see": [
        "Coral gardens and the eastern wall with sea fans",
        "Clouds of anthias, octopus, moray eels and reef fish",
        "Turtles and the occasional reef shark on the wall",
        "The famous underwater post box, a fun photo stop",
      ],
      "conditions": "Calm, sheltered and gentle, ideal for training and relaxed diving. Visibility 10&ndash;25 metres; warm all year. Suitable for absolute beginners through to macro hunters.",
      "how": "Jemeluk is our training bay and easy daily dive. Pool skills move here for first sea dives, and certified divers enjoy long, relaxed tours, always four divers maximum.",
      "faqs": [
        ("Is this where courses start?", "Yes, Open Water students do their first sea dives here after the pool. It&rsquo;s calm, shallow and forgiving."),
        ("Can my non-diving partner come?", "Yes, the snorkelling over the coral gardens is excellent."),
      ],
      "quote": "We feel like we could not have picked a better place.",
      "quote_by": "Google review &middot; one of 508 five-star reviews",
    },
    "es": {
      "name": "Bah&iacute;a de Jemeluk",
      "lede": "Nuestro arrecife de casa: jardines de coral tranquilos y someros que bajan a una pared, donde cada alumno de Open Water respira por primera vez en el mar.",
      "facts": [("3&ndash;25 m", "profundidad"), ("Todos los niveles", "primeras inmersiones"), ("Desde costa", "Amed"), ("Arrecife de casa", "el de cada d&iacute;a"), ("En la puerta", "Amed")],
      "overview": [
        "Jemeluk es la bah&iacute;a alrededor de la que se enrosca el pueblo de Amed, y el centro de toda la costa. Jardines de coral tranquilos y someros empiezan a los tres metros y bajan a una pared que se descuelga m&aacute;s all&aacute; de los 25 en la punta este.",
        "Es donde cada alumno de Open Water respira por primera vez en el mar, y el esn&oacute;rquel es tan bueno que la pareja no buceadora no se queda fuera. Tambi&eacute;n es donde vamos en los d&iacute;as libres.",
      ],
      "see": [
        "Jardines de coral y la pared este con gorgonias",
        "Nubes de anthias, pulpos, morenas y peces de arrecife",
        "Tortugas y alg&uacute;n tibur&oacute;n de arrecife en la pared",
        "El famoso buz&oacute;n submarino, una parada divertida para la foto",
      ],
      "conditions": "Tranquilo, resguardado y suave, ideal para formaci&oacute;n y buceo relajado. Visibilidad 10&ndash;25 metros; c&aacute;lido todo el a&ntilde;o. Apto desde principiantes absolutos hasta cazadores de macro.",
      "how": "Jemeluk es nuestra bah&iacute;a de pr&aacute;cticas y la inmersi&oacute;n f&aacute;cil de cada d&iacute;a. Las habilidades de piscina pasan aqu&iacute; para las primeras inmersiones en el mar, y los titulados disfrutan recorridos largos y relajados, siempre cuatro buceadores como m&aacute;ximo.",
      "faqs": [
        ("&iquest;Aqu&iacute; empiezan los cursos?", "S&iacute;, los alumnos de Open Water hacen aqu&iacute; sus primeras inmersiones en el mar tras la piscina. Es tranquilo, somero e indulgente."),
        ("&iquest;Puede venir mi pareja no buceadora?", "S&iacute;, el esn&oacute;rquel sobre los jardines de coral es excelente."),
      ],
      "quote": "Sentimos que no pod&iacute;amos haber elegido un sitio mejor.",
      "quote_by": "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas",
    },
  },
  {
    "slug": "pyramids", "img": f"{WP}/2022/09/DiveMasterw.webp",
    "en": {
      "name": "The Pyramids",
      "lede": "Stacked concrete reef structures on the sand off Amed, two decades grown and swarming with glassfish, with turtles passing through.",
      "facts": [("5&ndash;22 m", "depth"), ("All levels", "great second dive"), ("Shore entry", "Amed"), ("Artificial reef", "type"), ("A few min", "by car")],
      "overview": [
        "The Pyramids are a series of concrete cube blocks stacked into pyramid shapes on a sandy bottom off Amed beach, a few minutes along the coast from Jemeluk. Seeded two decades ago, they&rsquo;ve grown into a thriving artificial reef and proof that, given a little help, the ocean rebuilds fast.",
        "It&rsquo;s a brilliant second dive, often run as a gentle drift, and our favourite classroom for underwater navigation.",
      ],
      "see": [
        "Swirling clouds of glassfish around the structures",
        "Lionfish, batfish, groupers and reef fish",
        "Turtles passing through the sand channels",
        "Macro on the blocks: nudibranchs, shrimp, gobies",
      ],
      "conditions": "Shallow and forgiving, suitable for all levels. Often a relaxed drift along the structures. Visibility 10&ndash;25 metres; gentle conditions most days.",
      "how": "We use the Pyramids as a relaxed second dive and our navigation classroom for the Advanced course. Four divers maximum, an easy pace, and plenty to point at.",
      "faqs": [
        ("Is it a drift dive?", "Often a gentle one, depending on the day. We brief it each morning."),
        ("Good for new divers?", "Yes, it&rsquo;s shallow and easy, a great confidence-builder after the house reef."),
      ],
      "quote": "Welcoming, kind and helpful. An amazing experience from start to finish.",
      "quote_by": "Google review &middot; one of 508 five-star reviews",
    },
    "es": {
      "name": "Las Pir&aacute;mides",
      "lede": "Estructuras de hormig&oacute;n apiladas sobre la arena frente a Amed, con dos d&eacute;cadas de crecimiento y repletas de peces cristal, con tortugas de paso.",
      "facts": [("5&ndash;22 m", "profundidad"), ("Todos los niveles", "gran segunda inmersi&oacute;n"), ("Desde costa", "Amed"), ("Arrecife artificial", "tipo"), ("Pocos min", "en coche")],
      "overview": [
        "Las Pir&aacute;mides son una serie de bloques c&uacute;bicos de hormig&oacute;n apilados en forma de pir&aacute;mide sobre un fondo de arena frente a la playa de Amed, a unos minutos por la costa desde Jemeluk. Sembradas hace dos d&eacute;cadas, se han convertido en un arrecife artificial rebosante y en la prueba de que, con un poco de ayuda, el mar se reconstruye r&aacute;pido.",
        "Es una segunda inmersi&oacute;n brillante, a menudo en deriva suave, y nuestra aula favorita de navegaci&oacute;n subacu&aacute;tica.",
      ],
      "see": [
        "Nubes giratorias de peces cristal alrededor de las estructuras",
        "Peces le&oacute;n, peces murci&eacute;lago, m&eacute;ros y peces de arrecife",
        "Tortugas cruzando los canales de arena",
        "Macro en los bloques: nudibranquios, gambas, gobios",
      ],
      "conditions": "Somero e indulgente, apto para todos los niveles. A menudo una deriva relajada por las estructuras. Visibilidad 10&ndash;25 metros; condiciones suaves casi siempre.",
      "how": "Usamos Las Pir&aacute;mides como segunda inmersi&oacute;n relajada y nuestra aula de navegaci&oacute;n para el curso Advanced. Cuatro buceadores como m&aacute;ximo, ritmo f&aacute;cil y mucho que se&ntilde;alar.",
      "faqs": [
        ("&iquest;Es una inmersi&oacute;n en deriva?", "A menudo una suave, seg&uacute;n el d&iacute;a. La explicamos cada ma&ntilde;ana."),
        ("&iquest;Buena para buceadores nuevos?", "S&iacute;, es somera y f&aacute;cil, ideal para coger confianza tras el arrecife de casa."),
      ],
      "quote": "Acogedores, amables y siempre pendientes. Una experiencia incre&iacute;ble de principio a fin.",
      "quote_by": "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas",
    },
  },
  {
    "slug": "melasti", "img": f"{WP}/2022/09/Rescue_diver-1.webp",
    "en": {
      "name": "Melasti Reef",
      "lede": "Our neighbourhood dive, 500 metres from the door: a gentle slope of coral and seagrass with resident turtles.",
      "facts": [("4&ndash;20 m", "depth"), ("All levels", "easiest logistics"), ("Shore entry", "Amed"), ("Resident turtles", "highlight"), ("500 m", "from our door")],
      "overview": [
        "Melasti is the reef at the end of our own path, 500 metres from the dive centre and the beach we&rsquo;re named after. A gentle slope of coral and seagrass, it&rsquo;s perfect for an easy morning dive or a relaxed afternoon when you don&rsquo;t feel like the drive anywhere else.",
        "Quietly lovely, and home to a population of resident turtles.",
      ],
      "see": [
        "Resident green turtles grazing the seagrass",
        "Sloping coral with reef fish and anthias",
        "Octopus, moray eels and macro on the slope",
        "Rays and garden eels on the sandy patches",
      ],
      "conditions": "Gentle and shallow, suitable for all levels and the easiest logistics on the coast, you can practically walk to it. Visibility 10&ndash;25 metres; calm most days.",
      "how": "Melasti is our zero-hassle dive: stroll down, gear up, dive. Ideal for a quick second dive, a refresher, or an early morning before the day warms up. Four divers maximum.",
      "faqs": [
        ("How far is it?", "500 metres from the dive centre, the easiest dive we run, no drive needed."),
        ("Will I see turtles?", "There&rsquo;s a resident population, so very often, yes."),
      ],
      "quote": "An authentic diving school, and I say that as a diving professional.",
      "quote_by": "Google review &middot; one of 508 five-star reviews",
    },
    "es": {
      "name": "Arrecife de Melasti",
      "lede": "Nuestra inmersi&oacute;n de barrio, a 500 metros de la puerta: una pendiente suave de coral y praderas con tortugas residentes.",
      "facts": [("4&ndash;20 m", "profundidad"), ("Todos los niveles", "la log&iacute;stica m&aacute;s f&aacute;cil"), ("Desde costa", "Amed"), ("Tortugas residentes", "lo mejor"), ("500 m", "de la puerta")],
      "overview": [
        "Melasti es el arrecife al final de nuestro propio camino, a 500 metros del centro y de la playa que nos da nombre. Una pendiente suave de coral y praderas, perfecta para una inmersi&oacute;n f&aacute;cil de ma&ntilde;ana o una tarde relajada cuando no apetece conducir a ning&uacute;n otro sitio.",
        "Discretamente preciosa, y hogar de una poblaci&oacute;n de tortugas residentes.",
      ],
      "see": [
        "Tortugas verdes residentes pastando la pradera",
        "Coral en pendiente con peces de arrecife y anthias",
        "Pulpos, morenas y macro en la ladera",
        "Rayas y anguilas jard&iacute;n en los claros de arena",
      ],
      "conditions": "Suave y somero, apto para todos los niveles y la log&iacute;stica m&aacute;s f&aacute;cil de la costa: pr&aacute;cticamente se va andando. Visibilidad 10&ndash;25 metros; tranquilo casi siempre.",
      "how": "Melasti es nuestra inmersi&oacute;n sin complicaciones: bajas, te equipas, buceas. Ideal para una segunda inmersi&oacute;n r&aacute;pida, un refresco o una primera hora antes de que apriete el d&iacute;a. Cuatro buceadores como m&aacute;ximo.",
      "faqs": [
        ("&iquest;A qu&eacute; distancia est&aacute;?", "A 500 metros del centro: la inmersi&oacute;n m&aacute;s f&aacute;cil que hacemos, sin coche."),
        ("&iquest;Ver&eacute; tortugas?", "Hay una poblaci&oacute;n residente, as&iacute; que muy a menudo, s&iacute;."),
      ],
      "quote": "Una escuela de buceo aut&eacute;ntica, y lo digo como profesional del buceo.",
      "quote_by": "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas",
    },
  },
  {
    "slug": "bunutan", "img": f"{WP}/2022/09/Open_water_padi.webp",
    "en": {
      "name": "Bunutan",
      "lede": "A sandy point on the Amed strip with garden-eel colonies and a gentle deep slope, often dived as an easy drift.",
      "facts": [("12&ndash;30 m", "depth"), ("All levels", "drift"), ("Shore entry", "Amed"), ("Garden eels", "highlight"), ("Amed strip", "location")],
      "overview": [
        "Bunutan Point begins with a gentle sandy slope dotted with macro life and garden-eel colonies, then deepens into open water often swept by a soft current, which makes it a lovely easy drift.",
        "Quietly excellent and usually empty, it&rsquo;s a favourite for divers who like to fly along a slope and let the reef come to them.",
      ],
      "see": [
        "Garden-eel colonies swaying on the sand",
        "Nudibranchs and macro critters on the slope",
        "Schooling fish, barracuda and the occasional reef shark deeper down",
        "Rays and flatfish on the sand",
      ],
      "conditions": "Suits all levels as a relaxed drift, with deeper sections for Advanced divers. Currents are usually gentle. Visibility 10&ndash;30 metres.",
      "how": "We run Bunutan as an easy drift, letting the current do the work while we point out the macro and watch the blue. Four divers maximum, a relaxed pace.",
      "faqs": [
        ("Is it a drift dive?", "Usually a gentle one, yes, an easy, enjoyable way to cover the slope."),
        ("Good for all levels?", "Yes, as a relaxed drift it suits everyone, with deeper sections for Advanced divers who want them."),
      ],
      "quote": "We feel like we could not have picked a better place.",
      "quote_by": "Google review &middot; one of 508 five-star reviews",
    },
    "es": {
      "name": "Bunutan",
      "lede": "Una punta de arena en el tramo de Amed con colonias de anguilas jard&iacute;n y una pendiente suave hacia lo hondo, que solemos bucear como deriva f&aacute;cil.",
      "facts": [("12&ndash;30 m", "profundidad"), ("Todos los niveles", "deriva"), ("Desde costa", "Amed"), ("Anguilas jard&iacute;n", "lo mejor"), ("Tramo de Amed", "ubicaci&oacute;n")],
      "overview": [
        "La punta de Bunutan empieza con una pendiente suave de arena salpicada de vida macro y colonias de anguilas jard&iacute;n, y luego se ahonda hacia mar abierto, a menudo barrida por una corriente suave que la convierte en una deriva preciosa y f&aacute;cil.",
        "Discretamente excelente y casi siempre vac&iacute;a, es un favorito de quien disfruta volando por una ladera y dejando que el arrecife venga a &eacute;l.",
      ],
      "see": [
        "Colonias de anguilas jard&iacute;n meci&eacute;ndose en la arena",
        "Nudibranquios y bichos macro en la ladera",
        "Bancos de peces, barracudas y alg&uacute;n tibur&oacute;n de arrecife m&aacute;s abajo",
        "Rayas y peces planos en la arena",
      ],
      "conditions": "Vale para todos los niveles como deriva relajada, con tramos m&aacute;s profundos para Advanced. Las corrientes suelen ser suaves. Visibilidad 10&ndash;30 metros.",
      "how": "Hacemos Bunutan como deriva f&aacute;cil, dejando que la corriente trabaje mientras se&ntilde;alamos el macro y vigilamos el azul. Cuatro buceadores como m&aacute;ximo, ritmo relajado.",
      "faqs": [
        ("&iquest;Es una inmersi&oacute;n en deriva?", "Normalmente una suave, s&iacute;: una forma f&aacute;cil y disfrutona de recorrer la ladera."),
        ("&iquest;Vale para todos los niveles?", "S&iacute;, como deriva relajada vale para todos, con tramos m&aacute;s profundos para los Advanced que los quieran."),
      ],
      "quote": "Sentimos que no pod&iacute;amos haber elegido un sitio mejor.",
      "quote_by": "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas",
    },
  },
  {
    "slug": "lipah", "img": f"{WP}/2022/09/Rescue_diver-1.webp",
    "en": {
      "name": "Lipah Bay",
      "lede": "A small black-sand bay of coral bommies, relaxed and shallow, and a reef-shark nursing site, as good for snorkellers as divers.",
      "facts": [("5&ndash;20 m", "depth"), ("All levels", "snorkellers too"), ("Shore entry", "Amed"), ("Reef-shark nursery", "highlight"), ("Amed strip", "location")],
      "overview": [
        "Lipah is a small, sheltered black-sand bay scattered with coral bommies on sand, relaxed, shallow and easy. It&rsquo;s a known reef-shark nursing site, so juvenile blacktips are sometimes seen in the shallows.",
        "A classic easy second dive and a lovely spot for snorkellers, sheltered from the strong currents of the Lombok Strait.",
      ],
      "see": [
        "Coral bommies dotted across the sand",
        "Juvenile reef sharks in the nursery shallows",
        "Anthias, parrotfish and angelfish over the coral",
        "Macro on the bommies: nudibranchs, shrimp, gobies",
      ],
      "conditions": "Sheltered, shallow and calm, suitable for all levels and snorkellers. Gentle currents. Visibility 10&ndash;25 metres; warm year-round.",
      "how": "We dive Lipah as a relaxed second dive or an easy day, ideal after something deeper. Four divers maximum, a gentle pace, and time to enjoy the bommies.",
      "faqs": [
        ("Are the sharks dangerous?", "No, these are small, shy juvenile reef sharks using the bay as a nursery. A privilege to see."),
        ("Good for snorkelling?", "Yes, it&rsquo;s shallow and sheltered, lovely from the surface."),
      ],
      "quote": "Welcoming, kind and helpful. An amazing experience from start to finish.",
      "quote_by": "Google review &middot; one of 508 five-star reviews",
    },
    "es": {
      "name": "Bah&iacute;a de Lipah",
      "lede": "Una peque&ntilde;a bah&iacute;a de arena negra con bommies de coral, relajada y somera, y zona de cr&iacute;a de tiburones de arrecife: tan buena para esn&oacute;rquel como para bucear.",
      "facts": [("5&ndash;20 m", "profundidad"), ("Todos los niveles", "esn&oacute;rquel incl."), ("Desde costa", "Amed"), ("Vivero de tiburones", "lo mejor"), ("Tramo de Amed", "ubicaci&oacute;n")],
      "overview": [
        "Lipah es una bah&iacute;a peque&ntilde;a y resguardada de arena negra, salpicada de bommies de coral sobre arena: relajada, somera y f&aacute;cil. Es una conocida zona de cr&iacute;a de tiburones de arrecife, as&iacute; que a veces se ven puntas negras juveniles en lo somero.",
        "Una cl&aacute;sica segunda inmersi&oacute;n f&aacute;cil y un sitio precioso para esn&oacute;rquel, resguardado de las fuertes corrientes del estrecho de Lombok.",
      ],
      "see": [
        "Bommies de coral repartidos por la arena",
        "Tiburones de arrecife juveniles en el vivero somero",
        "Anthias, peces loro y peces &aacute;ngel sobre el coral",
        "Macro en los bommies: nudibranquios, gambas, gobios",
      ],
      "conditions": "Resguardada, somera y tranquila, apta para todos los niveles y esnorquelistas. Corrientes suaves. Visibilidad 10&ndash;25 metros; c&aacute;lida todo el a&ntilde;o.",
      "how": "Buceamos Lipah como segunda inmersi&oacute;n relajada o d&iacute;a tranquilo, ideal despu&eacute;s de algo m&aacute;s profundo. Cuatro buceadores como m&aacute;ximo, ritmo suave y tiempo para disfrutar los bommies.",
      "faqs": [
        ("&iquest;Son peligrosos los tiburones?", "No, son tiburones de arrecife juveniles, peque&ntilde;os y t&iacute;midos, que usan la bah&iacute;a como vivero. Un privilegio verlos."),
        ("&iquest;Buena para esn&oacute;rquel?", "S&iacute;, es somera y resguardada, preciosa desde la superficie."),
      ],
      "quote": "Acogedores, amables y siempre pendientes. Una experiencia incre&iacute;ble de principio a fin.",
      "quote_by": "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas",
    },
  },
  {
    "slug": "japanese-wreck", "img": f"{WP}/2022/09/Open_water_padi.webp",
    "en": {
      "name": "Japanese Wreck",
      "lede": "A small, coral-encrusted wreck in shallow water at Banyuning, so shallow snorkellers can see it, and a macro and nursery haven.",
      "facts": [("6&ndash;12 m", "depth"), ("All levels", "snorkellers too"), ("Shore entry", "Banyuning"), ("Macro nursery", "highlight"), ("~15 min", "by car")],
      "overview": [
        "Tucked into Banyuning Bay, about fifteen minutes east of Jemeluk, the Japanese Wreck is a small vessel (around 20 metres) lying in just 6 to 12 metres of water, shallow enough that snorkellers float right over it. Its exact origin is debated, but the popular name has stuck.",
        "Don&rsquo;t let the modest size fool you: the hull is completely encrusted in coral and sponges, and the lack of current makes the bay a nursery, famous for pygmy seahorses and other macro.",
      ],
      "see": [
        "A coral- and sponge-covered hull teeming with life",
        "Pygmy seahorses on the surrounding sea fans",
        "Nudibranchs, ghost pipefish and juvenile reef fish",
        "Anthias, parrotfish and angelfish over the wreck",
      ],
      "conditions": "Shallow, calm and current-free, ideal for all levels, long bottom times and snorkellers. Visibility 10&ndash;25 metres; warm year-round. A photographer&rsquo;s favourite.",
      "how": "We dive the Japanese Wreck slow and shallow, perfect for a long, relaxed second dive and macro hunting. Four divers maximum, and plenty of time to find the small stuff.",
      "faqs": [
        ("Is it really a Japanese WWII wreck?", "The popular name has stuck, but its exact origin is uncertain, it&rsquo;s a small, old vessel now reclaimed entirely by the reef."),
        ("Good for beginners?", "Excellent, it&rsquo;s shallow, calm and current-free, with huge bottom time."),
      ],
      "quote": "We feel like we could not have picked a better place.",
      "quote_by": "Google review &middot; one of 508 five-star reviews",
    },
    "es": {
      "name": "Pecio Japon&eacute;s",
      "lede": "Un peque&ntilde;o pecio cubierto de coral en aguas someras de Banyuning, tan somero que los esnorquelistas lo ven, y un para&iacute;so macro y de cr&iacute;a.",
      "facts": [("6&ndash;12 m", "profundidad"), ("Todos los niveles", "esn&oacute;rquel incl."), ("Desde costa", "Banyuning"), ("Vivero macro", "lo mejor"), ("~15 min", "en coche")],
      "overview": [
        "Metido en la bah&iacute;a de Banyuning, a unos quince minutos al este de Jemeluk, el Pecio Japon&eacute;s es un peque&ntilde;o barco (de unos 20 metros) tumbado en apenas 6 a 12 metros de agua, tan somero que los esnorquelistas flotan justo por encima. Su origen exacto se debate, pero el nombre popular ha cuajado.",
        "Que el tama&ntilde;o modesto no te enga&ntilde;e: el casco est&aacute; completamente cubierto de coral y esponjas, y la falta de corriente hace de la bah&iacute;a un vivero, famoso por sus caballitos pigmeos y otro macro.",
      ],
      "see": [
        "Un casco cubierto de coral y esponjas rebosante de vida",
        "Caballitos pigmeos en las gorgonias de alrededor",
        "Nudibranquios, peces pipa fantasma y peces de arrecife juveniles",
        "Anthias, peces loro y peces &aacute;ngel sobre el pecio",
      ],
      "conditions": "Somero, tranquilo y sin corriente, ideal para todos los niveles, tiempos de fondo largos y esnorquelistas. Visibilidad 10&ndash;25 metros; c&aacute;lido todo el a&ntilde;o. Favorito de los fot&oacute;grafos.",
      "how": "Buceamos el Pecio Japon&eacute;s despacio y somero, perfecto para una segunda inmersi&oacute;n larga y relajada y para cazar macro. Cuatro buceadores como m&aacute;ximo, y tiempo de sobra para encontrar lo peque&ntilde;o.",
      "faqs": [
        ("&iquest;Es de verdad un pecio japon&eacute;s de la II Guerra Mundial?", "El nombre popular ha cuajado, pero su origen exacto es incierto: es un barco peque&ntilde;o y antiguo ya reclamado por completo por el arrecife."),
        ("&iquest;Bueno para principiantes?", "Excelente: es somero, tranquilo y sin corriente, con much&iacute;simo tiempo de fondo."),
      ],
      "quote": "Sentimos que no pod&iacute;amos haber elegido un sitio mejor.",
      "quote_by": "Rese&ntilde;a de Google &middot; una de las 508 con cinco estrellas",
    },
  },
  {
    "slug": "gili-selang", "img": G3904,
    "en": {
      "name": "Gili Selang",
      "lede": "The little island at Bali&rsquo;s easternmost tip: pristine coral and real pelagic potential, guarded by strong, unpredictable currents.",
      "facts": [("5&ndash;30 m", "depth"), ("Advanced only", "experienced"), ("Mostly shore", "boat occasionally"), ("Currents &amp; pelagics", "highlight"), ("Bali&rsquo;s tip", "location")],
      "overview": [
        "Gili Selang sits at Bali&rsquo;s easternmost point. We usually dive it from the shore, though occasionally a short traditional jukung is needed to reach the best of it. The protected side has big bommies and low, healthy coral; the exposed side can have strong, unpredictable currents, and with them the chance of larger pelagics.",
        "It&rsquo;s the coast&rsquo;s wild card, advanced divers only, on the right day, with the right plan.",
      ],
      "see": [
        "Healthy hard coral and big bommies on the sheltered side",
        "White-tip reef sharks and Napoleon wrasse",
        "Larger pelagics on the exposed side, occasionally even sharks or mola",
        "Pygmy seahorses and nudibranchs on the coral",
      ],
      "conditions": "For experienced, advanced divers only because of strong and unpredictable currents on the exposed side. We dive it only when conditions are right. Visibility can be excellent.",
      "how": "We only run Gili Selang for advanced divers, on a day with the right conditions and a careful plan. Four divers maximum, a thorough briefing, and an honest call, if it&rsquo;s not safe, we go elsewhere. Ask us.",
      "faqs": [
        ("Who can dive Gili Selang?", "Experienced, advanced divers only. The currents on the exposed side are no place to learn."),
        ("Can I request it?", "Yes, ask us, and we&rsquo;ll watch the conditions and tell you honestly whether it&rsquo;s a go."),
      ],
      "quote": "The sea, once it casts its spell, holds one in its net of wonder forever.",
      "quote_by": "Jacques-Yves Cousteau",
    },
    "es": {
      "name": "Gili Selang",
      "lede": "El islote de la punta m&aacute;s oriental de Bali: coral intacto y potencial pel&aacute;gico de verdad, custodiados por corrientes fuertes e impredecibles.",
      "facts": [("5&ndash;30 m", "profundidad"), ("Solo avanzados", "con experiencia"), ("Casi siempre costa", "barco a veces"), ("Corrientes y pel&aacute;gicos", "lo mejor"), ("Punta de Bali", "ubicaci&oacute;n")],
      "overview": [
        "Gili Selang est&aacute; en la punta m&aacute;s oriental de Bali. Lo solemos bucear desde la costa, aunque a veces hace falta un jukung tradicional corto para llegar a lo mejor. El lado protegido tiene grandes bommies y coral bajo y sano; el lado expuesto puede tener corrientes fuertes e impredecibles, y con ellas la opci&oacute;n de pel&aacute;gicos mayores.",
        "Es el comod&iacute;n de la costa: solo buceadores avanzados, el d&iacute;a adecuado y con el plan adecuado.",
      ],
      "see": [
        "Coral duro sano y grandes bommies en el lado resguardado",
        "Tiburones punta blanca y napole&oacute;n",
        "Pel&aacute;gicos mayores en el lado expuesto, a veces incluso tiburones o mola",
        "Caballitos pigmeos y nudibranquios en el coral",
      ],
      "conditions": "Solo para buceadores avanzados y con experiencia por las corrientes fuertes e impredecibles del lado expuesto. Solo lo buceamos cuando las condiciones acompa&ntilde;an. La visibilidad puede ser excelente.",
      "how": "Solo hacemos Gili Selang con buceadores avanzados, un d&iacute;a con las condiciones adecuadas y un plan cuidadoso. Cuatro buceadores como m&aacute;ximo, un briefing a fondo y una decisi&oacute;n honesta: si no es seguro, vamos a otro sitio. Preg&uacute;ntanos.",
      "faqs": [
        ("&iquest;Qui&eacute;n puede bucear Gili Selang?", "Solo buceadores avanzados y con experiencia. Las corrientes del lado expuesto no son sitio para aprender."),
        ("&iquest;Puedo pedirlo?", "S&iacute;, preg&uacute;ntanos: vigilaremos las condiciones y te diremos honestamente si se puede."),
      ],
      "quote": "El mar, una vez lanzado su hechizo, te atrapa para siempre en su red de asombro.",
      "quote_by": "Jacques-Yves Cousteau",
    },
  },
]


def schema_for(lang, s):
    d = s[lang]
    self_url = BASE + (f"site-{s['slug']}.html" if lang == "en" else f"site-{s['slug']}-es.html")
    attraction = {
        "@context": "https://schema.org", "@type": "TouristAttraction",
        "name": clean(d["name"]), "description": clean(d["lede"]),
        "url": self_url,
        "isPartOf": {"@type": "LocalBusiness", "name": "Diving La Vida Loca", "url": BASE},
        "touristType": "Scuba divers",
    }
    faqs = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": clean(q),
                            "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in d["faqs"]]}
    return ('<script type="application/ld+json">' + json.dumps(attraction, ensure_ascii=False) + "</script>\n"
            + '<script type="application/ld+json">' + json.dumps(faqs, ensure_ascii=False) + "</script>\n")


count = 0
for s in SITES:
    for lang, HEAD, FOOT in [("en", HEAD_EN, FOOT_EN), ("es", HEAD_ES, FOOT_ES)]:
        d = s[lang]
        fname = f"site-{s['slug']}.html" if lang == "en" else f"site-{s['slug']}-es.html"
        en_file = f"site-{s['slug']}.html"
        es_file = f"site-{s['slug']}-es.html"
        title = f"{clean(d['name'])} · Amed/Tulamben Dive Site | Diving La Vida Loca" if lang == "en" \
            else f"{clean(d['name'])} · Punto de Inmersión en Amed/Tulamben | Diving La Vida Loca"
        desc = clean(d["lede"])
        idx_in = SITES.index(s)
        prev = SITES[idx_in - 1] if idx_in > 0 else None
        nxt = SITES[idx_in + 1] if idx_in < len(SITES) - 1 else None
        html = (HEAD.replace("{{TITLE}}", title).replace("{{DESC}}", desc) + body(lang, s, prev, nxt) + FOOT)
        html = (html
                .replace("{{SELF}}", BASE + fname)
                .replace("{{EN_ABS}}", BASE + en_file)
                .replace("{{ES_ABS}}", BASE + es_file)
                .replace("{{ES_URL}}", es_file if lang == "en" else en_file)
                .replace("{{EN_URL}}", en_file)
                .replace("{{SCHEMA}}", schema_for(lang, s)))
        with open(os.path.join(OUT, fname), "w") as f:
            f.write(html)
        count += 1
print(f"wrote {count} dive-site article pages")
