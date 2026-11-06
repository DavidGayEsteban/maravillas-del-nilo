# -*- coding: utf-8 -*-
"""Genera egipto.html (guía offline, navegación 100% CSS). Uso: python3 build.py"""
import os, sys
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from photos_data import PHOTOS as P
from content import *
from routemap import route_map_svg

days = build_days(P)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

def maps_url(q):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(q)

RUTA_MAPS_URL = "https://www.google.com/maps/dir/" + "/".join([
    "Luxor,+Egipto", "Edf%C3%BA,+Egipto", "Kom+Ombo,+Egipto", "Asu%C3%A1n,+Egipto",
    "Abu+Simbel,+Egipto", "Asu%C3%A1n,+Egipto", "El+Cairo,+Egipto"])

# ---------------------------------------------------------------------------
# COMPONENTES
# ---------------------------------------------------------------------------
def photo_block(photos, name, h=200):
    if not photos:
        return ""
    main = f'<div class="stop-photo"><img src="{photos[0]}" alt="{name}" loading="lazy" style="height:{h}px"></div>'
    rest = photos[1:]
    if not rest:
        return main
    cols = 2 if len(rest) != 3 else 3
    grid = "".join(f'<img src="{p}" alt="{name}" loading="lazy">' for p in rest)
    return main + f'<div class="stop-grid cols-{cols}">{grid}</div>'

def render_stop(s):
    tag = f'<span class="stop-tag {s["tag"]}">{s["tag"]}</span>' if s["tag"] else ""
    curio = f'<div class="stop-curio">{s["curio"]}</div>' if s["curio"] else ""
    mapa = f'<a class="pill map" href="{maps_url(s["mapq"])}" target="_blank" rel="noopener">📍 Google Maps</a>' if s["mapq"] else ""
    nearby = f'<div class="nearby"><b>Cerca:</b> {s["nearby"]}</div>' if s["nearby"] else ""
    tips = ""
    if s["tips"]:
        tips = '<details class="more tips"><summary>✓ Consejos</summary><ul class="tips-list">' + "".join(f"<li>{t}</li>" for t in s["tips"]) + "</ul></details>"
    more = f'<details class="more"><summary>+ Más información</summary><div class="more-body">{s["more"]}</div></details>' if s["more"] else ""
    cls = "stop" if s["included"] else "stop optional"
    return f"""
    <div class="{cls}"><div class="stop-card">
      {photo_block(s["photos"], s["name"])}
      <div class="stop-time">{s["time"]}{tag}</div>
      <div class="stop-name">{s["name"]}</div>
      <div class="stop-desc">{s["desc"]}</div>
      {curio}
      <div class="stop-meta">{mapa}</div>
      {nearby}
      <div class="stop-actions">{tips}{more}</div>
    </div></div>"""

def render_day(i, d):
    cover = next((s["photos"][0] for s in d["stops"] if s["photos"]), None)
    hero = (f'<div class="hero-wrap hero-photo"><img src="{cover}" alt="{d["title"]}"><div class="hero-fade"></div></div>'
            if cover else '<div class="hero-wrap hero-plain"></div>')
    nxt = (f'<label for="r-day{i+1}" class="day-footer-note"><b>Mañana ›</b> {days[i+1]["title"]}</label>'
           if i < len(days)-1 else '<div class="day-footer-note"><b>¡Fin del viaje!</b> Que lo disfrutéis.</div>')
    return f"""
    <div class="view" id="day{i}">
      {hero}
      <div class="day-heading">
        <div class="day-kicker">{d["kicker"]} · {d["city"]}</div>
        <div class="day-title">{d["title"]}</div>
        <div class="day-date">{d["date"]}</div>
      </div>
      <div class="legend"><span><i class="dot inc"></i> Incluido</span><span><i class="dot opt"></i> Contratado aparte / opcional</span></div>
      <div class="timeline">{"".join(render_stop(s) for s in d["stops"])}</div>
      {nxt}
    </div>"""

def card(title, body, photo=None, badge=None, h=170):
    img = f'<img class="card-img" src="{photo}" alt="" style="height:{h}px">' if photo else ""
    bd = f'<span class="badge-pending">{badge}</span>' if badge else ""
    return f'<div class="card{" has-img" if photo else ""}">{img}<div class="card-body">{bd}<h3>{title}</h3>{body}</div></div>'

# ---------------------------------------------------------------------------
# SECCIONES
# ---------------------------------------------------------------------------
def sec_resumen():
    rows = "".join(f"""
      <label for="r-day{i}" class="day-row">
        <img class="day-row-img" src="{next((s['photos'][0] for s in d['stops'] if s['photos']), '')}" alt="">
        <div class="day-row-body"><div class="day-row-title">Día {i+1} · {d["title"]}</div><div class="day-row-sub">{d["kicker"].split("·")[-1].strip()} · {d["city"]}</div></div>
        <div class="day-row-arrow">›</div>
      </label>""" for i, d in enumerate(days))
    stats = """<div class="stat-grid">
      <div class="stat"><b>8</b><span>días</span></div><div class="stat"><b>4</b><span>noches en el Nilo</span></div>
      <div class="stat"><b>3</b><span>noches en El Cairo</span></div><div class="stat"><b>17</b><span>monumentos</span></div>
      <div class="stat"><b>7</b><span>Patrimonio UNESCO</span></div><div class="stat"><b>4.700</b><span>años de historia</span></div></div>"""
    return f"""
    <div class="view" id="resumen">
      <div class="hero-wrap hero-photo tall"><img src="{P['portada_egipto'][1]}" alt="Egipto"><div class="hero-fade"></div>
        <div class="hero-text"><div class="hero-kicker">7 → 14 de noviembre de 2026</div><div class="hero-title">Maravillas del Nilo</div></div></div>
      <div class="section-pad">
        {stats}
        <div class="section-title">La ruta</div>
        <div class="section-intro">Mapa con la geografía real de Egipto. Con conexión, el botón abre la ruta en Google Maps.</div>
        <div class="card map-card">{route_map_svg()}</div>
        <a class="pill map wide" href="{RUTA_MAPS_URL}" target="_blank" rel="noopener">🗺️ Ver la ruta completa en Google Maps</a>
        <div class="section-title">Día a día</div>
        <div class="card list-card">{rows}</div>
      </div>
    </div>"""

def sec_alojamiento():
    vuelos = "".join(f'<div class="flight-row"><div class="flight-leg">{t}</div><div><b>{r}</b><br><span class="muted">{f} · {h} · {n}</span></div></div>' for t,f,r,h,n in VUELOS)
    return f"""
    <div class="view" id="alojamiento"><div class="section-pad">
      <div class="section-title">Vuelos y alojamiento</div>
      <div class="section-intro">Datos de la documentación definitiva de la reserva (DTR041251). Solo falta la hora del vuelo interno Asuán → El Cairo.</div>
      {card("✈️ Vuelos · Nile Air", f'<img class="card-img" src="{P["w_nileair"][0]}" style="height:150px;margin:-14px -15px 12px;width:calc(100% + 30px)"><div class="flights">{vuelos}</div><p class="muted">Localizador: <b>DTR041251</b> · 4 adultos · 2 habitaciones dobles · Equipaje por persona: 1 × 20 kg facturado + 1 × 5 kg de mano · Los vuelos no son reembolsables y los horarios pueden cambiar a última hora.</p>')}
      {card("🚢 M/S Kahila · crucero por el Nilo · 4 noches", "<p><b>Del 7 al 11 de noviembre</b>, Luxor → Asuán, pensión completa (categoría D).</p><p>Motonave de 5★ locales con 72 camarotes (68 dobles de 22 m² y 4 suites) con ventanal panorámico, aire acondicionado, caja fuerte, minibar y hervidor. Restaurante en la cubierta inferior, salón-bar panorámico con biblioteca, piscina y solárium en la cubierta superior, boutique, sala de masajes, lavandería y wifi de pago. Bebidas no incluidas: se cargan al camarote y se liquidan al desembarcar (efectivo o tarjeta).</p><p class='muted'>Pendiente: número de camarote y teléfono de recepción (se anotan al embarcar).</p>", P["w_kahila_exterior"][0], "Confirmado")}
      <div class="stop-grid cols-3" style="margin:0 0 12px"><img src="{P['w_kahila_camarote'][0]}"><img src="{P['w_kahila_piscina'][0]}"><img src="{P['w_kahila_restaurante'][0]}"></div>
      {card("🏨 JW Marriott Hotel Cairo · 3 noches", "<p><b>Del 11 al 14 de noviembre</b>, alojamiento y desayuno (categoría D).</p><p><b>Dirección:</b> Ring Road, Mirage City, New Cairo, Cairo 11757.<br><b>Teléfono:</b> <a href='tel:+20224115588'>+20 2 2411 5588</a></p><p>Resort de 5★ junto al aeropuerto (3 km, 10–15 min): piscinas exterior e interior, playa artificial con parque acuático, spa Mandara, campo de golf de 18 hoyos, gimnasio y diez restaurantes (libanés, italiano, asiático, steakhouse). A 5 min del centro comercial Cairo Festival City. Lejos del centro histórico (45–60 min de Guiza o Khan el-Khalili), así que para salir por libre lo práctico es Uber.</p><a class='pill map' href='https://www.google.com/maps/search/?api=1&query=JW+Marriott+Hotel+Cairo+Mirage+City' target='_blank' rel='noopener'>📍 Google Maps</a>", P["hoteles_cairo"][1], "Confirmado")}
      {card("🎟️ Excursiones contratadas y opcionales", "<p><b>Contratadas para los 4</b> (ya pagadas): Día completo en El Cairo con Saqqara (día 7) · Abu Simbel en bus (día 4) · Gran Museo Egipcio con almuerzo (día 6).</p><p><b>Incluidas en el viaje:</b> Guiza y la Esfinge; en el crucero, Karnak, Luxor, Valle de los Reyes, Hatshepsut, Colosos de Memnón, Edfú, Kom Ombo, Philae y paseo en faluca.</p><p><b>Opcionales no contratadas</b> (se deciden y pagan con el guía): paseo en globo en Luxor (día 2) · poblado nubio en Asuán (día 4) · posibles opcionales en Asuán la mañana del día 5 según el vuelo · Noche Cairota (día 6).</p>")}
      {card("💳 Pagos pendientes en destino", "<p>• Visado: <b>36 USD por persona</b> en el aeropuerto de Luxor.<br>• Cuota de servicios, propinas generales y tasas: <b>75 € por persona</b>.<br>• Propina del guía: recomendada 3 € por persona y día, mínimo 20 € por la semana.<br>• Bebidas a bordo y en restaurantes, y excursiones opcionales que contratéis.</p><p class='muted'>Precio del viaje ya pagado: 6.140 € para 4 personas, incluidas las tres excursiones contratadas y el seguro básico de viaje.</p>")}
    </div></div>"""

def sec_info():
    emg = """<div class="emg-grid">
      <div class="emg-item"><div class="label">Emergencias generales</div><div class="num"><a href="tel:112">112</a></div></div>
      <div class="emg-item"><div class="label">Policía</div><div class="num"><a href="tel:122">122</a></div></div>
      <div class="emg-item"><div class="label">Policía turística</div><div class="num"><a href="tel:126">126</a></div></div>
      <div class="emg-item"><div class="label">Ambulancia</div><div class="num"><a href="tel:123">123</a></div></div>
    </div>"""
    return f"""
    <div class="view" id="info"><div class="section-pad">
      <div class="section-title">Información general</div>
      <div class="section-intro">Teléfonos útiles. Guárdalos también en el móvil antes de salir.</div>
      {emg}
      {card("🇪🇸 Embajada de España en El Cairo", "<p><b>Emergencias consulares</b> (accidentes, desapariciones, peligro): <a href='tel:+201231183783'>+20 12 31 83 783</a></p><p>Centralita: <a href='tel:+20227353551'>+20 2 2735 3551</a> · 41 Ismail Mohamed St., Zamalek</p><p class='muted'>El teléfono de emergencia es solo para asuntos graves.</p>")}
      {card("🧳 Receptivo en Egipto · Vamos Travel", "<p><b>Teléfono de urgencia 24 h:</b> <a href='tel:+201282149499'>+20 128 214 9499</a><br>30 Old Hadayek Al Ahram St., Flat 1, Giza.</p><p class='muted'>Es la agencia local que organiza traslados, guía y excursiones. El nombre y móvil del guía se añadirán cuando lo conozcáis el día 1.</p>")}
      {card("🛡️ Seguro de viaje · AXA", "<p><b>Asistencia 24 h / 365 días:</b> <a href='tel:+34934968333'>+34 93 496 83 33</a><br><b>Póliza nº 9422001867</b>, contratada por Dynamic Tours.</p><p>Al llamar hay que indicar el nombre del asegurado, el número de póliza, dónde estáis y un teléfono de contacto. Coberturas principales: gastos médicos en el extranjero hasta 3.000 €, repatriación incluida, prolongación de estancia hasta 500 €, demora de equipaje 100 €, robo o daños al equipaje 300 €.</p><p class='muted'>Condiciones completas: dynamic-tours.com/doc/seguros/dynamic-tours-seguro-inclusion-axa.pdf</p>")}
      {card("✈️ Agencia · Dynamic Tours / Viajes Carrefour", "<p><b>Urgencias Dynamic Tours 24 h:</b> <a href='tel:+34690125031'>+34 690 125 031</a><br>Dynamic Tours: <a href='tel:+34915521443'>+34 91 552 14 43</a> · reservas@dynamic-tours.com<br>Viajes Carrefour S.S. de los Reyes: <a href='tel:+34914906818'>+34 91 490 68 18</a> · es.viajes.sansebastianreyes@carrefour.com<br>Localizador: <b>DTR041251</b></p>")}
      {card("🕐 Datos útiles", "<p>• Hora: GMT+2 todo el año → 1 h más que en España en noviembre.<br>• Prefijo: +20. Para llamar a España desde Egipto: +34.<br>• Electricidad: 220 V, enchufe europeo (C/F). No hace falta adaptador.<br>• Fin de semana: viernes y sábado.<br>• Moneda: libra egipcia (EGP). Ver pestaña Guía práctica.</p>")}
    </div></div>"""

def sec_practica():
    blocks = "".join(f'<details class="acc" {"open" if i==0 else ""}><summary>{t}</summary><ul class="tips-list">' + "".join(f"<li>{x}</li>" for x in items) + "</ul></details>" for i,(t,items) in enumerate(PRACTICAL))
    return f"""
    <div class="view" id="practica"><div class="section-pad">
      <div class="section-title">Guía práctica</div>
      <div class="section-intro">Lo que conviene saber antes y durante el viaje. Toca cada bloque para desplegarlo.</div>
      <div class="card acc-card">{blocks}</div>
    </div></div>"""

def sec_egipto():
    gods = "".join(f'<div class="glo-row"><b>{n}</b><span>{t}</span></div>' for n,t in GODS)
    phs = "".join(f'<div class="glo-row"><b>{n}<small>{y}</small></b><span>{t}</span></div>' for n,y,t in PHARAOHS)
    return f"""
    <div class="view" id="egipto">
      <div class="hero-wrap hero-photo"><img src="{P['portada_egipto'][0]}" alt="Egipto"><div class="hero-fade"></div></div>
      <div class="section-pad">
        <div class="section-title">Egipto</div>
        <div class="emg-grid">
          <div class="emg-item"><div class="label">Población</div><div class="num sm">≈120 millones</div></div>
          <div class="emg-item"><div class="label">Superficie</div><div class="num sm">1.001.450 km²</div></div>
          <div class="emg-item"><div class="label">Capital</div><div class="num sm">El Cairo</div></div>
          <div class="emg-item"><div class="label">Idioma</div><div class="num sm">Árabe egipcio</div></div>
        </div>
        {card("🗺️ El país", "<p>Dos veces España en superficie, pero el 96% es desierto: casi todos los egipcios viven en el 4% del territorio que ocupan el valle y el delta del Nilo, una franja verde de apenas 10–20 km de ancho. Es el país más poblado del mundo árabe y el tercero de África, con una población muy joven (edad media de 25 años).</p><p>Limita con el Mediterráneo, Libia, Sudán, el mar Rojo e Israel/Gaza. El canal de Suez, que une el Mediterráneo con el mar Rojo, mueve el 12% del comercio mundial.</p>")}
        {card("🌊 El Nilo", "<p>6.650 km desde el lago Victoria hasta el Mediterráneo; en Egipto recorre 1.500 km de sur a norte, por lo que «subir» el Nilo es ir hacia el sur. Hasta la presa de Asuán se desbordaba cada verano y dejaba un limo negro fertilísimo: por eso los egipcios llamaban a su país <i>Kemet</i>, «la tierra negra», frente a <i>Deshret</i>, el desierto rojo. El calendario, los impuestos y la religión giraban en torno a la crecida. Heródoto lo resumió: «Egipto es un don del Nilo».</p>", P["aswan"][1])}
        {card("🕌 Religión y sociedad", "<p>Un 90% de musulmanes suníes y un 10% de cristianos coptos, una de las iglesias más antiguas del mundo. Se habla árabe egipcio, el dialecto más entendido del mundo árabe gracias al cine y la música de El Cairo. La familia, la hospitalidad y el humor (los egipcios se llaman a sí mismos «hijos de la broma») son el centro de la vida social. El té con mucho azúcar es la bebida nacional.</p>")}
        {card("🍲 Gastronomía", "<p><b>Koshari</b>: el plato nacional, arroz, lentejas, macarrones, garbanzos, salsa de tomate y cebolla frita. <b>Ful medames</b>: habas guisadas, el desayuno de todo el país. <b>Taameya</b>: falafel de habas, verde por dentro. <b>Molokheya</b>: sopa espesa de hojas de yute con ajo. <b>Mahshi</b>: verduras rellenas de arroz. <b>Kofta y kebab</b> de cordero. <b>Fattah</b>: arroz, pan y carne con salsa de ajo, plato de fiesta. Dulces: <b>kunafa</b>, <b>basbousa</b>, <b>om ali</b>. Bebidas: té (shai), <b>karkadé</b> (hibisco, frío o caliente), zumo de caña, de mango y de guayaba.</p>", P["comida_tipica"][0])}
        {card("🌡️ Clima en noviembre", "<p>La mejor época del año. Luxor y Asuán: 28–32 °C de día, 15–18 °C de noche, cielo despejado. El Cairo: 24–27 °C de día, 15 °C de noche, alguna bruma. Lluvia prácticamente inexistente. Abu Simbel al amanecer: fresco (12–15 °C).</p>")}
        {card("📜 Jeroglíficos en 2 minutos", "<p>Unos 700 signos que funcionan de tres maneras a la vez: <b>fonogramas</b> (suenan: el buitre es «a», el pie es «b», el agua ondulada es «n»), <b>ideogramas</b> (significan lo que dibujan) y <b>determinativos</b> (signos mudos al final que indican la categoría: un hombre sentado = persona, unas piernas = movimiento). Se leen hacia donde miran los animales y las personas. Los nombres de los reyes van dentro de un <b>cartucho</b>, un óvalo con una cuerda anudada. Champollion los descifró en 1822 gracias a los cartuchos de Ptolomeo y Cleopatra en la Piedra Rosetta, hoy en el Museo Británico.</p>")}
        <div class="section-title">Dioses que vais a encontrar</div>
        <div class="card glo-card">{gods}</div>
        <div class="section-title">Faraones y reyes clave</div>
        <div class="card glo-card">{phs}</div>
      </div>
    </div>"""

def era_chip(key):
    name, color = EPOCAS[key]
    return f'<span class="era-chip" style="background:{color}">{name}</span>'

def sec_tl_monumentos():
    items = "".join(f"""
      <div class="tl-item" style="--era:{EPOCAS[m['era']][1]}">
        <div class="tl-year">{m['year']}</div>
        <div class="tl-card">
          {era_chip(m['era'])}
          <div class="tl-name">{m['name']}</div>
          <div class="tl-who">{m['who']}</div>
          <div class="tl-text">{m['text']}</div>
          <label for="r-day{m['day']}" class="tl-link">Lo visitáis el día {m['day']+1} ›</label>
        </div>
      </div>""" for m in MONUMENTS)
    legend = "".join(era_chip(k) for k in EPOCAS)
    return f"""
    <div class="view" id="tlmon"><div class="section-pad">
      <div class="section-title">Los monumentos del viaje, en orden cronológico</div>
      <div class="section-intro">Casi 4.700 años separan la pirámide de Zoser del Gran Museo Egipcio. Cada color es una época; toca un enlace para ir al día de la visita.</div>
      <div class="era-legend">{legend}</div>
      <div class="tl">{items}</div>
    </div></div>"""

def sec_tl_historia():
    items = "".join(f"""
      <div class="tl-item" style="--era:{EPOCAS[h['era']][1]}">
        <div class="tl-year">{h['year']}</div>
        <div class="tl-card">
          {era_chip(h['era'])}
          <div class="tl-name">{h['name']}</div>
          <div class="tl-text">{h['text']}</div>
          {f'<div class="tl-see">Lo veréis en: {h["see"]}</div>' if h.get('see') else ''}
        </div>
      </div>""" for h in HISTORY)
    return f"""
    <div class="view" id="tlhist"><div class="section-pad">
      <div class="section-title">Historia de Egipto en una línea</div>
      <div class="section-intro">De los primeros agricultores del Nilo al Egipto de hoy: 31 dinastías, griegos, romanos, árabes, mamelucos, otomanos y dos siglos de Egipto moderno. Las épocas usan los mismos colores que la línea de monumentos.</div>
      <div class="era-legend">{"".join(era_chip(k) for k in EPOCAS)}</div>
      <div class="tl">{items}</div>
    </div></div>"""

def sec_vocab():
    groups = ""
    for title, items in VOCAB:
        rows = "".join(f"""
          <div class="vocab-item">
            <div class="vocab-es">{es}</div>
            <div class="vocab-mid"><div class="phrase">{ar}</div><div class="translit">{tr}</div><div class="pron">{pr}</div></div>
            <button type="button" class="play-btn" onclick="speakArabic('{ar}', this)" aria-label="Escuchar">🔊</button>
          </div>""" for es,tr,pr,ar in items)
        groups += f'<details class="acc" open><summary>{title}</summary><div class="vocab-list">{rows}</div></details>'
    return f"""
    <div class="view" id="vocab"><div class="section-pad">
      <div class="section-title">Vocabulario</div>
      <div class="section-intro">Árabe egipcio de la calle. Toca 🔊 para oír la pronunciación (usa la voz del teléfono; funciona sin conexión si tiene instalado el árabe). Las letras entre comillas (') son una pequeña pausa en la garganta.</div>
      <div class="card acc-card">{groups}</div>
    </div></div>"""

# ---------------------------------------------------------------------------
# ENSAMBLADO
# ---------------------------------------------------------------------------
TABS = [("resumen","Resumen",True)] + [(f"day{i}", f"Día {i+1}", False) for i in range(len(days))] + [
    ("tlmon","Monumentos",True), ("tlhist","Historia",True), ("egipto","Egipto",True),
    ("practica","Guía práctica",True), ("alojamiento","Vuelos y hotel",True), ("info","Teléfonos",True), ("vocab","Vocabulario",True)]

radios = "".join(f'<input type="radio" name="tabs" id="r-{t}" class="tab-radio"{" checked" if t=="resumen" else ""}>' for t,_,_ in TABS)
tabbar = '<div class="tabbar">' + "".join(f'<label for="r-{t}" class="tab{" util" if u else ""}">{l}</label>' for t,l,u in TABS) + '</div>'
views = sec_resumen() + "".join(render_day(i,d) for i,d in enumerate(days)) + sec_tl_monumentos() + sec_tl_historia() + sec_egipto() + sec_practica() + sec_alojamiento() + sec_info() + sec_vocab()
active_css = "\n".join(
    f'#r-{t}:checked ~ #views #{t}{{display:block;}}\n#r-{t}:checked ~ .tabbar label[for="r-{t}"]{{background:var(--nile-night);color:#fff;border-color:var(--nile-night);}}'
    for t,_,u in TABS)

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.css"), encoding="utf-8").read()
JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.js"), encoding="utf-8").read()

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#0b2e3a">
<title>Maravillas del Nilo · Guía de viaje</title>
<style>{CSS}
/* Navegación 100% CSS: funciona sin JavaScript */
{active_css}
</style>
</head>
<body>
<div class="app-header">
  <div class="eyebrow">Dynamic Tours · Reserva DTR041251</div>
  <div class="app-title">Maravillas del Nilo</div>
  <div class="app-sub">El Cairo · Crucero Luxor–Asuán · Abu Simbel · 4 viajeros</div>
  <div class="locator"><span>07 → 14 nov 2026</span><span>8 días / 7 noches</span><span>funciona sin conexión</span></div>
</div>
{radios}
{tabbar}
<div id="views">{views}</div>
<footer class="credit">Guía personal de viaje · guarda esta página en tu dispositivo</footer>
<script>{JS}</script>
</body>
</html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("OK", OUT, round(len(HTML)/1024/1024, 2), "MB")
