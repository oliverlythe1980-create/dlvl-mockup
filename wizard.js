// Trip builder — client-side, prices from the shop's published price list (incl. 10% tax)
(function () {
  const el = document.getElementById('wizard');
  if (!el) return;
  const ES = document.documentElement.lang === 'es';
  const WA = 'https://wa.me/6282145538716';
  const RATE = 19400; // IDR per EUR, approximate

  const P = {
    dsd1: 1050000, dsd2: 1450000, dsd2acc: 1700000,
    ow: 5400000, ow2: 4950000, owacc: 6300000, owaow: 9900000,
    aow: 4900000, aow2: 4550000, aowacc: 5500000,
    resc: 7400000, rescacc: 8300000,
    dm: 19000000, dmu: 26000000,
    funday: 990000, night: 790000,
  };

  const T = ES ? {
    step: 'Paso', of: 'de', back: '← Atrás', start: 'Empezar de nuevo',
    q1: '¿Qué te apetece?',
    g_try: 'Probar el buceo', g_try_s: 'Bautizo, sin experiencia',
    g_cert: 'Sacarme la titulación', g_cert_s: 'PADI Open Water, 3 días',
    g_level: 'Subir de nivel', g_level_s: 'Advanced o Rescue',
    g_fun: 'Inmersiones', g_fun_s: 'Ya tengo titulación',
    g_pro: 'Hacerme pro', g_pro_s: 'Divemaster, hasta 2 meses',
    q_dsd: '¿Una o dos inmersiones?',
    dsd1: '1 inmersión', dsd1_s: 'Media jornada', dsd2: '2 inmersiones', dsd2_s: 'La experiencia completa',
    q_people: '¿Cuántos sois?', p1: 'Solo yo', p2_s: 'precio por persona reducido', p5: '5 o más', p5_s: 'guías en paralelo, nunca en manada',
    q_owpack: 'Redondea el plan',
    ow_solo: 'Solo el Open Water', ow_acc: '+ 3 noches con desayuno', ow_aow: '+ curso Advanced', ow_aow_s: '5 días, hasta 30 m y el pecio',
    q_level: '¿Qué curso?',
    aow: 'Advanced Open Water', aow_s: '2 días · 5 inmersiones', resc: 'Rescue + EFR', resc_s: '3 días · primeros auxilios incl.',
    q_acc: '¿Te quedas a dormir?', acc_y: 'Sí, con desayuno', acc_n: 'No, solo el curso',
    q_days: '¿Cuántos días de buceo?', day: 'día', days: 'días', dives_s: '2 inmersiones/día',
    q_cert: '¿Qué titulación tienes?',
    lv_ow: 'Open Water', lv_ow_s: 'hasta 18 m', lv_aow: 'Advanced', lv_aow_s: 'hasta 30 m',
    lv_resc: 'Rescue o superior', lv_pro: 'Divemaster / Instructor',
    q_logged: '¿Cuántas inmersiones llevas, más o menos?',
    db1: 'Menos de 20', db2: '20–50', db3: '50–200', db4: 'Más de 200',
    l_cert: (lv, db) => `Titulación: ${lv} · ${db} inmersiones`,
    note_ow: 'Planearemos puntos dentro de tu límite de 18 m; si te tienta la parte honda del pecio, el Advanced encaja perfecto.',
    note_rusty: '¿Hace tiempo de tu última inmersión? El refresco ReActivate (IDR 900.000, media jornada) es la vuelta al agua más amable.',
    q_accq: '¿Necesitas alojamiento con desayuno?',
    accq_y: 'Sí, con vosotros', accq_y_s: 'bungalós entre los arrozales', accq_n: 'No, ya lo tengo',
    q_equip: '¿Necesitas equipo?',
    eq_full: 'Equipo completo', eq_full_s: 'incluido en nuestros precios', eq_own: 'Traigo el mío', eq_own_s: 'botellas y plomos los ponemos nosotros',
    l_accq: 'Alojamiento con desayuno: sí', l_eq_full: 'Equipo: completo (incluido)', l_eq_own: 'Equipo: propio',
    note_accask: 'Te pasamos opciones y tarifas de habitación para tus fechas por WhatsApp.',
    note_group: '¿Sois más de cuatro? Nunca buceréis en manada: montamos guías en paralelo y cerramos la logística por WhatsApp.',
    disc3: '5% dto. aplicado', disc5: '10% dto. aplicado',
    q_night: '¿Añadimos una nocturna?', night_y: 'Sí, una nocturna', night_n: 'Esta vez no',
    q_dm: '¿Qué programa?', dm: 'Divemaster', dm_s: 'inmersiones de formación incl.', dmu: 'Divemaster ilimitado', dmu_s: 'cada botella libre es tuya',
    sum: 'Tu plan', perp: 'por persona', total: 'Total estimado',
    eur: 'aprox.', taxes: 'impuestos y equipo incluidos',
    note_est: 'Es una estimación para orientarte; lo confirmamos todo por WhatsApp antes de reservar nada.',
    note_dm: 'Cuota anual de PADI y Crew Pack no incluidos. Alojamiento de larga estancia: pregúntanos.',
    note_funacc: '¿Alojamiento para varios días? Pregúntanos tarifas de habitación.',
    dates: 'Tus fechas (opcional)', arr: 'Llegada', dep: 'Salida',
    contact: 'Tus datos', fname: 'Nombre', femail: 'Email',
    req: 'Dinos tu nombre y un email para saber quién escribe.',
    wa_name: 'Nombre', wa_email: 'Email',
    send: 'Enviar mi plan por WhatsApp',
    wa_hi: 'Hola! He montado mi plan en la web:', wa_dates: 'Fechas',
    l_dsd1: 'Bautizo de buceo · 1 inmersión', l_dsd2: 'Bautizo de buceo · 2 inmersiones',
    l_acc1: '+ 1 noche con desayuno', l_acc3: '+ 3 noches con desayuno', l_acc2: '+ 2 noches con desayuno',
    l_ow: 'Curso Open Water', l_owaow: 'Pack Open Water + Advanced',
    l_aow: 'Curso Advanced', l_resc: 'Rescue + EFR',
    l_fun: (d) => `Inmersiones · ${d} ${d > 1 ? 'días' : 'día'} (2/día)`,
    l_night: '+ inmersión nocturna', l_dm: 'Divemaster', l_dmu: 'Divemaster ilimitado',
    l_people: (n) => `${n} personas`,
  } : {
    step: 'Step', of: 'of', back: '← Back', start: 'Start over',
    q1: 'What are you here for?',
    g_try: 'Try diving', g_try_s: 'First time, no experience',
    g_cert: 'Get certified', g_cert_s: 'PADI Open Water, 3 days',
    g_level: 'Level up', g_level_s: 'Advanced or Rescue',
    g_fun: 'Fun dives', g_fun_s: "I'm already certified",
    g_pro: 'Go pro', g_pro_s: 'Divemaster, up to 2 months',
    q_dsd: 'One dive or two?',
    dsd1: '1 dive', dsd1_s: 'Half a day', dsd2: '2 dives', dsd2_s: 'The full experience',
    q_people: 'How many of you?', p1: 'Just me', p2_s: 'lower price per person', p5: '5 or more', p5_s: 'parallel guides, never a crowd',
    q_owpack: 'Round out the plan',
    ow_solo: 'Just the Open Water', ow_acc: '+ 3 nights with breakfast', ow_aow: '+ Advanced course', ow_aow_s: '5 days, to 30 m and the wreck',
    q_level: 'Which course?',
    aow: 'Advanced Open Water', aow_s: '2 days · 5 dives', resc: 'Rescue + EFR', resc_s: '3 days · first aid incl.',
    q_acc: 'Staying with us?', acc_y: 'Yes, with breakfast', acc_n: 'No, course only',
    q_days: 'How many days of diving?', day: 'day', days: 'days', dives_s: '2 dives/day',
    q_cert: 'What are you certified to?',
    lv_ow: 'Open Water', lv_ow_s: 'to 18 m', lv_aow: 'Advanced', lv_aow_s: 'to 30 m',
    lv_resc: 'Rescue or higher', lv_pro: 'Divemaster / Instructor',
    q_logged: 'Roughly how many dives have you logged?',
    db1: 'Fewer than 20', db2: '20–50', db3: '50–200', db4: '200+',
    l_cert: (lv, db) => `Certified: ${lv} · ${db} dives`,
    note_ow: "We'll plan sites within your 18 m limit; if you fancy the deep side of the wreck, the Advanced course slots right in.",
    note_rusty: 'Been a while since your last dive? The ReActivate refresher (IDR 900.000, half a day) is the kindest way back in.',
    q_accq: 'Do you need accommodation + breakfast?',
    accq_y: 'Yes, with you', accq_y_s: 'bungalows by the rice fields', accq_n: "No, I'm sorted",
    q_equip: 'Do you need equipment?',
    eq_full: 'Full equipment, please', eq_full_s: 'included in our prices', eq_own: 'I bring my own', eq_own_s: "we'll sort tanks & weights",
    l_accq: 'Accommodation + breakfast: yes, please', l_eq_full: 'Equipment: full set (included)', l_eq_own: 'Equipment: brings own',
    note_accask: "We'll send room options and rates for your dates on WhatsApp.",
    note_group: "More than four? You'll never dive in a crowd: we run parallel guides and sort the logistics on WhatsApp.",
    disc3: '5% discount applied', disc5: '10% discount applied',
    q_night: 'Add a night dive?', night_y: 'Yes, one night dive', night_n: 'Not this time',
    q_dm: 'Which program?', dm: 'Divemaster', dm_s: 'training dives included', dmu: 'Unlimited Divemaster', dmu_s: 'every spare tank is yours',
    sum: 'Your plan', perp: 'per person', total: 'Estimated total',
    eur: 'approx.', taxes: 'taxes & equipment included',
    note_est: 'This is an estimate to get you oriented; we confirm everything on WhatsApp before you book a thing.',
    note_dm: "PADI's annual fee and Crew Pack not included. Long-stay accommodation: ask us.",
    note_funacc: 'Accommodation for several days? Ask us for room rates.',
    dates: 'Your dates (optional)', arr: 'Arrival', dep: 'Departure',
    contact: 'Your details', fname: 'Name', femail: 'Email',
    req: 'Add your name and an email so we know who is writing.',
    wa_name: 'Name', wa_email: 'Email',
    send: 'Send my plan on WhatsApp',
    wa_hi: 'Hi! I built my plan on the website:', wa_dates: 'Dates',
    l_dsd1: 'Discover Scuba · 1 dive', l_dsd2: 'Discover Scuba · 2 dives',
    l_acc1: '+ 1 night with breakfast', l_acc3: '+ 3 nights with breakfast', l_acc2: '+ 2 nights with breakfast',
    l_ow: 'Open Water course', l_owaow: 'Open Water + Advanced pack',
    l_aow: 'Advanced course', l_resc: 'Rescue + EFR',
    l_fun: (d) => `Fun dives · ${d} ${d > 1 ? 'days' : 'day'} (2/day)`,
    l_night: '+ night dive', l_dm: 'Divemaster', l_dmu: 'Unlimited Divemaster',
    l_people: (n) => `${n} people`,
  };

  const idr = (n) => 'IDR ' + n.toLocaleString('de-DE');
  const eur = (n) => '€' + Math.round(n / RATE);
  const st = { history: [], labels: [], picks: [] };
  const SKEY = 'dlvl-wiz';
  function saveState() {
    const f = {};
    ['wiz-from', 'wiz-to', 'wiz-name', 'wiz-email'].forEach((id) => {
      const e = document.getElementById(id);
      if (e && e.value) f[id] = e.value;
    });
    try { sessionStorage.setItem(SKEY, JSON.stringify({ p: st.picks, f })); } catch (e) {}
  }
  const today = () => new Date().toISOString().slice(0, 10);
  const fmtDate = (iso) => new Date(iso + 'T12:00:00').toLocaleDateString(ES ? 'es-ES' : 'en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

  function opts(list) {
    return '<div class="wiz-grid">' + list.map((o) =>
      `<button type="button" class="wiz-opt" data-v="${o.v}"><strong>${o.t}</strong>${o.s ? `<span>${o.s}</span>` : ''}</button>`
    ).join('') + '</div>';
  }

  function crumbs() {
    if (!st.labels.length) return '';
    return '<div class="wiz-crumbs">' + st.labels.map((l) => `<span class="wiz-crumb">${l}</span>`).join('') + '</div>';
  }

  function header(q) {
    return crumbs() + `<p class="wiz-prog">${T.step} ${st.history.length + 1}</p><h3 class="wiz-q">${q}</h3>`;
  }

  const steps = {
    goal: () => header(T.q1) + opts([
      { v: 'try', t: T.g_try, s: T.g_try_s }, { v: 'cert', t: T.g_cert, s: T.g_cert_s },
      { v: 'level', t: T.g_level, s: T.g_level_s }, { v: 'fun', t: T.g_fun, s: T.g_fun_s },
      { v: 'pro', t: T.g_pro, s: T.g_pro_s },
    ]),
    dsd: () => header(T.q_dsd) + opts([
      { v: '1', t: T.dsd1, s: T.dsd1_s }, { v: '2', t: T.dsd2, s: T.dsd2_s },
    ]),
    dsdacc: () => header(T.q_acc) + opts([{ v: 'y', t: T.acc_y }, { v: 'n', t: T.acc_n }]),
    people: () => header(T.q_people) + opts([
      { v: '1', t: T.p1 }, { v: '2', t: '2', s: T.p2_s }, { v: '3', t: '3', s: T.p2_s },
      { v: '4', t: '4', s: T.p2_s }, { v: '5', t: T.p5, s: T.p5_s },
    ]),
    owpack: () => header(T.q_owpack) + opts([
      { v: 'solo', t: T.ow_solo }, { v: 'acc', t: T.ow_acc }, { v: 'aow', t: T.ow_aow, s: T.ow_aow_s },
    ]),
    levelcourse: () => header(T.q_level) + opts([
      { v: 'aow', t: T.aow, s: T.aow_s }, { v: 'resc', t: T.resc, s: T.resc_s },
    ]),
    levelacc: () => header(T.q_acc) + opts([{ v: 'y', t: T.acc_y }, { v: 'n', t: T.acc_n }]),
    cert: () => header(T.q_cert) + opts([
      { v: 'ow', t: T.lv_ow, s: T.lv_ow_s }, { v: 'aow', t: T.lv_aow, s: T.lv_aow_s },
      { v: 'resc', t: T.lv_resc }, { v: 'pro', t: T.lv_pro },
    ]),
    logged: () => header(T.q_logged) + opts([
      { v: 'db1', t: T.db1 }, { v: 'db2', t: T.db2 }, { v: 'db3', t: T.db3 }, { v: 'db4', t: T.db4 },
    ]),
    days: () => header(T.q_days) + opts(
      [1, 2, 3, 4, 5, 6].map((d) => ({ v: String(d), t: `${d} ${d > 1 ? T.days : T.day}`, s: T.dives_s }))
    ),
    night: () => header(T.q_night) + opts([{ v: 'y', t: T.night_y }, { v: 'n', t: T.night_n }]),
    accq: () => header(T.q_accq) + opts([
      { v: 'y', t: T.accq_y, s: T.accq_y_s }, { v: 'n', t: T.accq_n },
    ]),
    equip: () => header(T.q_equip) + opts([
      { v: 'full', t: T.eq_full, s: T.eq_full_s }, { v: 'own', t: T.eq_own, s: T.eq_own_s },
    ]),
    dm: () => header(T.q_dm) + opts([
      { v: 'dm', t: T.dm, s: T.dm_s }, { v: 'dmu', t: T.dmu, s: T.dmu_s },
    ]),
  };

  function compute() {
    const lines = [];
    let per = 0, note = T.note_est;
    const people = parseInt(st.people || '1', 10);
    if (st.goal === 'try') {
      if (st.dsd === '1') { lines.push([T.l_dsd1, P.dsd1]); per = P.dsd1; }
      else if (st.dsdacc === 'y') { lines.push([T.l_dsd2, P.dsd2], [T.l_acc1, P.dsd2acc - P.dsd2]); per = P.dsd2acc; }
      else { lines.push([T.l_dsd2, P.dsd2]); per = P.dsd2; }
    } else if (st.goal === 'cert') {
      if (st.owpack === 'aow') { lines.push([T.l_owaow, P.owaow]); per = P.owaow; }
      else if (st.owpack === 'acc') { const base = people > 1 ? P.ow2 : P.ow; lines.push([T.l_ow, base], [T.l_acc3, P.owacc - P.ow]); per = base + (P.owacc - P.ow); }
      else { per = people > 1 ? P.ow2 : P.ow; lines.push([T.l_ow, per]); }
    } else if (st.goal === 'level') {
      if (st.levelcourse === 'aow') {
        const base = people > 1 ? P.aow2 : P.aow;
        if (st.levelacc === 'y') { lines.push([T.l_aow, base], [T.l_acc2, P.aowacc - P.aow]); per = base + (P.aowacc - P.aow); }
        else { lines.push([T.l_aow, base]); per = base; }
      } else {
        if (st.levelacc === 'y') { lines.push([T.l_resc, P.resc], [T.l_acc3, P.rescacc - P.resc]); per = P.rescacc; }
        else { lines.push([T.l_resc, P.resc]); per = P.resc; }
      }
    } else if (st.goal === 'fun') {
      const LV = { ow: T.lv_ow, aow: T.lv_aow, resc: T.lv_resc, pro: T.lv_pro };
      const DB = { db1: T.db1, db2: T.db2, db3: T.db3, db4: T.db4 };
      lines.push([T.l_cert(LV[st.cert], DB[st.logged]), 0]);
      const d = parseInt(st.days, 10);
      let base = P.funday * d;
      if (d >= 5) { base = Math.round(base * 0.9); }
      else if (d >= 3) { base = Math.round(base * 0.95); }
      lines.push([T.l_fun(d), base]);
      if (d >= 5) lines.push([T.disc5, 0]); else if (d >= 3) lines.push([T.disc3, 0]);
      if (st.night === 'y') { lines.push([T.l_night, P.night]); base += P.night; }
      per = base;
      note = T.note_est;
      if (st.cert === 'ow') note += ' ' + T.note_ow;
      if (st.logged === 'db1') note += ' ' + T.note_rusty;
    } else if (st.goal === 'pro') {
      per = st.dm === 'dmu' ? P.dmu : P.dm;
      lines.push([st.dm === 'dmu' ? T.l_dmu : T.l_dm, per]);
      note = T.note_dm;
    }
    if (st.accq === 'y') { lines.push([T.l_accq, 0]); note += ' ' + T.note_accask; }
    if (people >= 5) note += ' ' + T.note_group;
    lines.push([st.equip === 'own' ? T.l_eq_own : T.l_eq_full, 0]);
    return { lines, per, people, note };
  }

  function summary() {
    const { lines, per, people, note } = compute();
    const total = per * people;
    const rows = lines.map(([l, v]) =>
      `<div class="wiz-row"><span>${l}</span><span>${v ? idr(v) : ''}</span></div>`
    ).join('');
    const disp = people >= 5 ? '5+' : String(people);
    const ppl = people > 1 ? `<div class="wiz-row"><span>${T.l_people(disp)}</span><span>&times; ${people}</span></div>` : '';
    el.innerHTML = `
      <div class="wiz-step">
      <div class="wiz-sumhead"><h3>${T.sum}</h3><img src="assets/logo-mark.png" alt=""></div>
      <div class="wiz-summary">${rows}${ppl}
        <div class="wiz-total"><span>${T.total}</span><span>${idr(total)}</span></div>
        <p class="wiz-eur">${T.eur} ${eur(total)} · ${T.taxes}</p>
      </div>
      <p class="wiz-note">${note}</p>
      <p class="wiz-dates-label">${T.dates}</p>
      <div class="wiz-dates">
        <div class="form-field"><label for="wiz-from">${T.arr}</label><input id="wiz-from" type="date" min="${today()}"></div>
        <div class="form-field"><label for="wiz-to">${T.dep}</label><input id="wiz-to" type="date" min="${today()}"></div>
      </div>
      <p class="wiz-dates-label">${T.contact}</p>
      <div class="wiz-dates">
        <div class="form-field" id="wf-name"><label for="wiz-name">${T.fname}</label><input id="wiz-name" type="text" autocomplete="name"></div>
        <div class="form-field" id="wf-email"><label for="wiz-email">${T.femail}</label><input id="wiz-email" type="email" autocomplete="email"></div>
      </div>
      <p class="wiz-req" hidden>${T.req}</p>
      <a class="pill-btn pill-btn--whatsapp wiz-send" href="#" target="_blank" rel="noopener">${T.send}</a>
      <button type="button" class="wiz-restart">${T.start}</button>
      </div>`;
    ['wiz-from', 'wiz-to', 'wiz-name', 'wiz-email'].forEach((id) => {
      document.getElementById(id).addEventListener('input', saveState);
    });
    const fromEl = document.getElementById('wiz-from');
    const toEl = document.getElementById('wiz-to');
    fromEl.addEventListener('change', () => { toEl.min = fromEl.value || today(); if (toEl.value && toEl.value < fromEl.value) toEl.value = fromEl.value; });
    el.querySelector('.wiz-send').addEventListener('click', (e) => {
      const name = document.getElementById('wiz-name').value.trim();
      const email = document.getElementById('wiz-email').value.trim();
      const reqEl = el.querySelector('.wiz-req');
      document.getElementById('wf-name').classList.toggle('wiz-err', !name);
      document.getElementById('wf-email').classList.toggle('wiz-err', !email.includes('@'));
      if (!name || !email.includes('@')) {
        e.preventDefault();
        reqEl.hidden = false;
        return;
      }
      reqEl.hidden = true;
      let dates = '';
      if (fromEl.value && toEl.value) dates = fmtDate(fromEl.value) + ' – ' + fmtDate(toEl.value);
      else if (fromEl.value) dates = fmtDate(fromEl.value);
      const msg = [T.wa_hi, `${T.wa_name}: ${name}`, `${T.wa_email}: ${email}`]
        .concat(lines.filter(([, v]) => v || true).map(([l, v]) => `· ${l}${v ? ' — ' + idr(v) : ''}`))
        .concat(people > 1 ? [`· ${T.l_people(people >= 5 ? '5+' : people)}`] : [])
        .concat([`${T.total}: ${idr(total)} (${T.eur} ${eur(total)})`])
        .concat(dates ? [`${T.wa_dates}: ${dates}`] : [])
        .join('\n');
      e.currentTarget.href = WA + '?text=' + encodeURIComponent(msg);
    });
    el.querySelector('.wiz-restart').addEventListener('click', () => { try { sessionStorage.removeItem(SKEY); } catch (e) {} for (const k in st) delete st[k]; st.history = []; st.labels = []; st.picks = []; show('goal'); });
  }

  const flow = {
    goal: (v) => ({ try: 'dsd', cert: 'people', level: 'levelcourse', fun: 'cert', pro: 'dm' }[v]),
    dsd: (v) => (v === '2' ? 'dsdacc' : 'accq'),
    dsdacc: () => 'equip',
    people: () => (st.goal === 'cert' ? 'owpack' : st.goal === 'fun' ? 'days' : null),
    owpack: (v) => (v === 'aow' ? 'accq' : 'equip'),
    levelcourse: () => 'levelpeople',
    levelpeople: () => 'levelacc',
    levelacc: () => 'equip',
    cert: () => 'logged',
    logged: () => 'people',
    days: () => 'night',
    night: () => 'accq',
    accq: () => 'equip',
    equip: () => null,
    dm: () => 'accq',
  };
  steps.levelpeople = steps.people;

  function show(step) {
    el.innerHTML = '<div class="wiz-step">' + steps[step]() +
      (st.history.length ? `<button type="button" class="wiz-back">${T.back}</button>` : '') + '</div>';
    el.querySelectorAll('.wiz-opt').forEach((b) => {
      b.addEventListener('click', () => {
        st[step === 'levelpeople' ? 'people' : step] = b.dataset.v;
        st.history.push(step);
        st.labels.push(b.querySelector('strong').textContent);
        st.picks.push(b.dataset.v);
        saveState();
        const next = flow[step](b.dataset.v);
        if (next) show(next); else summary();
      });
    });
    const back = el.querySelector('.wiz-back');
    if (back) back.addEventListener('click', () => { st.labels.pop(); st.picks.pop(); saveState(); show(st.history.pop()); });
  }

  show('goal');

  // restore state (e.g. after a language switch): replay picks, refill fields
  try {
    const saved = JSON.parse(sessionStorage.getItem(SKEY) || 'null');
    if (saved && Array.isArray(saved.p) && saved.p.length) {
      let ok = true;
      for (const v of saved.p) {
        const btn = el.querySelector('.wiz-opt[data-v="' + v + '"]');
        if (!btn) { ok = false; break; }
        btn.click();
      }
      if (ok && saved.f) {
        Object.keys(saved.f).forEach((id) => {
          const e = document.getElementById(id);
          if (e) e.value = saved.f[id];
        });
        const fe = document.getElementById('wiz-from');
        if (fe) fe.dispatchEvent(new Event('change'));
      }
      if (!ok) sessionStorage.removeItem(SKEY);
    }
  } catch (e) {}
})();
