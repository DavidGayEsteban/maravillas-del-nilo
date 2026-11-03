# -*- coding: utf-8 -*-
"""Mapa de la ruta con geografía real (proyección simple lon/lat) y estética tipo Google Maps."""

LON0, LON1, LAT0, LAT1 = 24.6, 37.2, 21.6, 32.0
W, H = 400, 430
SX = W / (LON1 - LON0)
SY = H / (LAT1 - LAT0)

def P(lon, lat):
    return (round((lon - LON0) * SX, 1), round((LAT1 - lat) * SY, 1))

def poly(points, close=True):
    d = "M" + " L".join(f"{x},{y}" for x, y in (P(*pt) for pt in points))
    return d + (" Z" if close else "")

# Contorno de Egipto continental (lon, lat), sentido horario desde Sallum
EGYPT = [(25.0,31.6),(26.3,31.4),(27.5,31.2),(28.6,31.0),(29.6,30.95),(29.9,31.2),(30.4,31.45),(30.9,31.55),(31.5,31.55),(31.9,31.5),(32.3,31.3),
         (32.55,30.9),(32.6,30.2),(32.55,29.97),(32.65,29.3),(32.9,28.6),(33.3,28.0),(33.7,27.4),(34.0,26.8),(34.4,26.0),(35.0,25.0),(35.5,24.1),(35.8,23.2),(36.4,22.5),(36.9,22.0),
         (25.0,22.0),(25.0,29.0),(24.7,30.2),(25.0,31.6)]
SINAI = [(32.55,30.9),(33.5,31.1),(34.2,31.3),(34.55,30.5),(34.9,29.5),(34.6,28.6),(34.3,27.9),(34.0,28.3),(33.6,28.7),(33.25,29.3),(32.95,29.95),(32.75,30.3)]
# Franja verde del valle del Nilo (aprox.)
NILE = [(31.24,30.05),(31.2,29.3),(30.85,28.1),(31.15,27.2),(31.7,26.6),(32.3,26.2),(32.7,26.1),(32.64,25.7),(32.55,25.3),(32.87,24.98),(32.93,24.47),(32.9,24.09)]
NASSER = [(32.9,24.0),(32.85,23.4),(32.6,22.9),(32.0,22.5),(31.6,22.3),(31.2,21.9),(31.45,21.7),(31.9,22.1),(32.4,22.4),(32.85,22.8),(33.1,23.4),(33.05,24.0)]
DELTA = [(31.24,30.05),(30.4,31.4),(31.1,31.5),(31.8,31.5),(31.24,30.05)]
FAYUM = (30.6,29.3)

CITIES = {
    "cairo": (31.24,30.05), "luxor": (32.64,25.70), "edfu": (32.87,24.98), "kom": (32.93,24.47),
    "aswan": (32.90,24.09), "abu": (31.63,22.34), "alex": (29.92,31.20), "hurg": (33.8,27.25), "suez": (32.55,29.97),
}

def pin(x, y, color="#ea4335", r=1.0):
    s = 1.0 * r
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M0,0 C-7,-9 -9,-13 -9,-17 a9,9 0 1,1 18,0 c0,4 -2,8 -9,17 z" fill="{color}" stroke="#fff" stroke-width="1.5"/>'
            f'<circle cx="0" cy="-17" r="3.5" fill="#fff"/></g>')

def label(x, y, text, size=11.5, bold=True, anchor="start", dy=0, color="#202124"):
    fw = ' font-weight="700"' if bold else ""
    halo = f'<text x="{x}" y="{y+dy}" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="{size}"{fw} text-anchor="{anchor}" fill="#fff" stroke="#fff" stroke-width="3" stroke-linejoin="round" opacity=".9">{text}</text>'
    return halo + f'<text x="{x}" y="{y+dy}" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="{size}"{fw} text-anchor="{anchor}" fill="{color}">{text}</text>'

def route_map_svg():
    c = {k: P(*v) for k, v in CITIES.items()}
    nile_d = poly(NILE, close=False)
    cruise = "M" + " L".join(f"{x},{y}" for x, y in (P(*NILE[i]) for i in range(7, 12)))
    fx, fy = c["cairo"]
    ax, ay = c["aswan"]; lx, ly = c["luxor"]; bx, by = c["abu"]
    return f"""<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="route-map" role="img" aria-label="Mapa de la ruta del viaje">
  <defs>
    <filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-color="#000" flood-opacity=".25"/></filter>
    <pattern id="desert" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r=".6" fill="#d9d3c3" opacity=".6"/></pattern>
  </defs>
  <rect width="{W}" height="{H}" fill="#aadaff"/>
  <!-- países vecinos (gris claro) -->
  <rect x="0" y="0" width="{W}" height="{H}" fill="#e8e6e1" clip-path="none" opacity="0"/>
  <path d="{poly([(24.6,32.0),(24.6,21.6),(25.0,21.6),(25.0,31.6)])}" fill="#e8e6e1"/>
  <path d="{poly([(24.6,21.6),(37.2,21.6),(37.2,22.0),(36.9,22.0),(25.0,22.0),(25.0,21.6)])}" fill="#e8e6e1"/>
  <path d="{poly([(34.2,31.3),(34.55,30.5),(34.9,29.5),(37.2,29.5),(37.2,32.0),(34.2,32.0)])}" fill="#e8e6e1"/>
  <path d="{poly([(35.0,29.5),(37.2,29.5),(37.2,22.0),(36.9,22.0),(36.4,22.5),(35.8,23.2),(35.5,24.1),(35.0,25.0),(35.3,26.5),(35.0,27.5),(34.9,29.5)])}" fill="#aadaff"/>
  <!-- Egipto -->
  <path d="{poly(EGYPT)}" fill="#f3f1ea" stroke="#cfcac0" stroke-width="1"/>
  <path d="{poly(EGYPT)}" fill="url(#desert)"/>
  <path d="{poly(SINAI)}" fill="#f3f1ea" stroke="#cfcac0" stroke-width="1"/>
  <path d="{poly(SINAI)}" fill="url(#desert)"/>
  <!-- valle y delta -->
  <path d="{poly(DELTA)}" fill="#c6e5b8"/>
  <path d="{nile_d}" fill="none" stroke="#c6e5b8" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="{P(*FAYUM)[0]}" cy="{P(*FAYUM)[1]}" r="6" fill="#c6e5b8"/>
  <!-- Nilo y lago Nasser -->
  <path d="{nile_d}" fill="none" stroke="#7fbce8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M{fx},{fy} L{P(30.4,31.4)[0]},{P(30.4,31.4)[1]} M{fx},{fy} L{P(31.8,31.5)[0]},{P(31.8,31.5)[1]}" fill="none" stroke="#7fbce8" stroke-width="1.6"/>
  <path d="{poly(NASSER)}" fill="#aadaff" stroke="#7fbce8" stroke-width="1"/>
  <!-- mares -->
  {label(P(29.5,32.0)[0], 14, "MAR MEDITERRÁNEO", 9.5, False, "middle", 0, "#4a6c8c")}
  {label(P(35.9,25.2)[0], P(35.9,25.2)[1], "MAR ROJO", 9.5, False, "middle", 0, "#4a6c8c")}
  {label(P(27.5,26.5)[0], P(27.5,26.5)[1], "DESIERTO OCCIDENTAL", 8.5, False, "middle", 0, "#9a9484")}
  {label(P(34.0,30.0)[0], P(34.0,30.0)[1], "SINAÍ", 8.5, False, "middle", 0, "#9a9484")}
  {label(P(32.2,22.9)[0], P(32.2,22.9)[1], "Lago Nasser", 8.5, False, "middle", 0, "#4a6c8c")}
  <!-- rutas -->
  <path d="M{lx},{ly} C{lx-120},{ly-60} {60},{90} {30},{-10}" fill="none" stroke="#9aa0a6" stroke-width="2" stroke-dasharray="5 5"/>
  <path d="M{ax},{ay} C{ax+70},{ay-40} {fx+80},{fy+60} {fx},{fy}" fill="none" stroke="#9aa0a6" stroke-width="2" stroke-dasharray="5 5"/>
  <path d="M{fx},{fy} C{fx-40},{fy-30} {80},{40} {40},{-10}" fill="none" stroke="#9aa0a6" stroke-width="2" stroke-dasharray="5 5"/>
  <path d="M{ax},{ay} Q{ax-10},{ay+30} {bx},{by}" fill="none" stroke="#f9ab00" stroke-width="3" stroke-dasharray="7 4" stroke-linecap="round"/>
  <path d="{cruise}" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="{cruise}" fill="none" stroke="#4285f4" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
  {label(48, 30, "✈ Madrid", 10, True, "start", 0, "#5f6368")}
  <!-- ciudades secundarias -->
  <circle cx="{c['alex'][0]}" cy="{c['alex'][1]}" r="2.5" fill="#5f6368"/>{label(c['alex'][0]+5, c['alex'][1]+4, "Alejandría", 9, False)}
  <circle cx="{c['hurg'][0]}" cy="{c['hurg'][1]}" r="2.5" fill="#5f6368"/>{label(c['hurg'][0]+5, c['hurg'][1]+4, "Hurghada", 9, False)}
  <circle cx="{c['suez'][0]}" cy="{c['suez'][1]}" r="2.5" fill="#5f6368"/>
  <!-- paradas -->
  <g filter="url(#sh)">
  {pin(*c['abu'], "#f9ab00", .85)}{label(c['abu'][0]+10, c['abu'][1]-8, "Abu Simbel", 11)}{label(c['abu'][0]+10, c['abu'][1]+3, "día 4 · bus", 9, False, "start", 0, "#5f6368")}
  {pin(*c['kom'], "#4285f4", .8)}{label(c['kom'][0]-12, c['kom'][1]-8, "Kom Ombo", 10.5, True, "end")}{label(c['kom'][0]-12, c['kom'][1]+3, "día 3", 9, False, "end", 0, "#5f6368")}
  {pin(*c['edfu'], "#4285f4", .8)}{label(c['edfu'][0]+11, c['edfu'][1]-8, "Edfú", 10.5)}{label(c['edfu'][0]+11, c['edfu'][1]+3, "día 3", 9, False, "start", 0, "#5f6368")}
  {pin(*c['aswan'], "#4285f4", .95)}{label(c['aswan'][0]+12, c['aswan'][1]-4, "Asuán", 12)}{label(c['aswan'][0]+12, c['aswan'][1]+8, "días 4–5", 9, False, "start", 0, "#5f6368")}
  {pin(*c['luxor'], "#4285f4", .95)}{label(c['luxor'][0]+12, c['luxor'][1]-4, "Luxor", 12)}{label(c['luxor'][0]+12, c['luxor'][1]+8, "días 1–2", 9, False, "start", 0, "#5f6368")}
  {pin(*c['cairo'], "#ea4335", 1.0)}{label(c['cairo'][0]+12, c['cairo'][1]-4, "El Cairo", 12)}{label(c['cairo'][0]+12, c['cairo'][1]+8, "días 5–8", 9, False, "start", 0, "#5f6368")}
  </g>
  <!-- leyenda -->
  <g transform="translate(10,{H-62})">
    <rect x="0" y="0" width="128" height="54" rx="8" fill="#fff" filter="url(#sh)"/>
    <line x1="10" y1="14" x2="30" y2="14" stroke="#4285f4" stroke-width="3.5" stroke-linecap="round"/><text x="36" y="18" font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="9.5" fill="#202124">Crucero por el Nilo</text>
    <line x1="10" y1="28" x2="30" y2="28" stroke="#9aa0a6" stroke-width="2" stroke-dasharray="5 5"/><text x="36" y="32" font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="9.5" fill="#202124">Vuelo</text>
    <line x1="10" y1="42" x2="30" y2="42" stroke="#f9ab00" stroke-width="3" stroke-dasharray="7 4"/><text x="36" y="46" font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="9.5" fill="#202124">Excursión en bus</text>
  </g>
</svg>"""
