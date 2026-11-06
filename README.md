# Maravillas del Nilo · Guía de viaje offline

Guía personal para el viaje a Egipto (7–14 nov 2026): itinerario día a día con fotos, líneas temporales de los monumentos y de la historia de Egipto, mapa de la ruta, guía práctica, teléfonos útiles y vocabulario árabe con audio.

**`egipto.html` es la guía completa en un solo archivo**: funciona sin conexión y en cualquier navegador (móvil o PC). La navegación por pestañas es CSS puro, así que también funciona en visores que bloquean JavaScript (por ejemplo, la vista rápida de iPhone). Solo el audio del vocabulario necesita JavaScript.

## Cómo usarla en el móvil
1. Descarga `egipto.html`.
2. Ábrelo con Safari o Chrome ("Abrir con…"). En iPhone, desde la vista previa usa Compartir → Safari.
3. Añádelo a la pantalla de inicio para tenerlo como una app.

## Estructura del proyecto
| Archivo | Qué es |
|---|---|
| `content.py` | Todo el contenido: itinerario, textos, líneas temporales, guía práctica, vocabulario |
| `styles.css` | Estilos |
| `app.js` | Audio del vocabulario (mejora progresiva) |
| `build.py` | Genera `egipto.html` a partir de los anteriores |
| `make_photos.py` | Optimiza las fotos y las incrusta en `photos_data.py` (base64) |

## Regenerar la guía
```bash
python3 make_photos.py   # solo si cambian las fotos (necesita Pillow)
python3 build.py         # genera egipto.html
```

## Pendiente de completar
- Hora del vuelo interno Asuán → El Cairo (11 nov)
- Nombre y móvil del guía (se conoce el día 1)
- Número de camarote del Kahila
- Fotos de las excursiones opcionales (globo, poblado nubio, Noche Cairota) y del JW Marriott
## Versión web
La guía está publicada en https://davidgayesteban.github.io/maravillas-del-nilo/ (`index.html`, generado por `build.py`).
