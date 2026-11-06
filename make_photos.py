# -*- coding: utf-8 -*-
"""Optimiza las fotos de /mnt/user-data/uploads y las guarda en base64 en photos_data.py"""
import os, base64, io
from PIL import Image

SRC = "/mnt/user-data/uploads"
MAX_W = 960
JPEG_Q = 62

def optimize(path, max_w=MAX_W, quality=JPEG_Q):
    im = Image.open(path).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * (max_w / im.width))), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=quality, optimize=True)
    data = buf.getvalue()
    return "data:image/jpeg;base64," + base64.b64encode(data).decode("ascii"), len(data)

GROUPS = {
    "karnak": ["01_Templo_Karnak.jpeg", "01_Templo_Karnak_1.jpeg", "01_Templo_Karnak_2.jpeg"],
    "luxor_temple": ["02_Templo_Luxor.jpeg"],
    "valley_kings": ["03_Valle_de_los_Reyes.jpeg"],
    "hatshepsut": ["04_Templo_Hatshepsut.jpeg"],
    "memnon": ["05_Colosos_de_Memnon.jpeg"],
    "edfu": ["06_Templo_Horus_Edfu.jpeg"],
    "kom_ombo": ["07_Templo_Kom_Ombo.jpeg"],
    "abu_simbel": ["08_Templos_Abu_Simbel.jpeg"],
    "philae": ["09_Templo_Philae.jpeg"],
    "felucca": ["10_Faluca_Nilo_Aswan.jpeg", "10_Faluca_Nilo_Aswan_1.jpeg"],
    "giza": ["11_Piramides_Guiza_Esfinge.jpeg", "11_Piramides_Guiza_Esfinge_1.jpeg"],
    "gem": ["12_Gran_Museo_Egipcio.jpeg", "12_Gran_Museo_Egipcio_2.jpeg"],
    "saladin": ["13_Ciudadela_de_Saladino.jpeg", "13_Ciudadela_de_Saladino_2.jpeg"],
    "mezquita_alabastro": ["14_Mezquita_de_Alabastro.jpeg", "14_Mezquita_de_Alabastro_1.jpeg", "14_Mezquita_de_Alabastro_2.jpeg"],
    "barrio_copto": ["15_Barrio_Copto.jpeg", "15_Barrio_Copto_1.jpeg"],
    "khan_el_khalili": ["16_Khan_el_Khalili.jpeg", "16_Khan_el_Khalili_1.jpeg"],
    "saqqara": ["17_Saqqara.jpeg", "17_Saqqara_1.jpeg"],
    "luxor_ciudad": ["18_Luxor_Ciudad_Nilo.jpeg", "18_Luxor_Ciudad_Nilo_1.jpeg"],
    "portada_egipto": ["19_Portada_Egipto.jpeg", "19_Portada_Egipto_1.jpeg"],
    "crucero_nilo": ["20_Crucero_Nilo.jpeg", "20_Crucero_Nilo_2.jpeg"],
    "hoteles_cairo": ["21_Hoteles_Cairo.jpeg", "21_Hoteles_Cairo_2.jpeg"],
    "aswan": ["22_Aswan.jpeg", "22_Aswan1.jpeg", "22_Aswan2.jpeg"],
    "skyline_cairo": ["23_Skyline_Cairo.jpeg", "23_Skyline_Cairo1.jpeg", "23_Skyline_Cairo2.jpeg"],
    "comida_tipica": ["24_Comida_Tipica_Egipto.jpeg", "24_Comida_Tipica_Egipto1.jpeg"],
    "aeropuerto_cairo": ["25_aeropuerto_del_cairo.jpeg"],
}

WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fotos_web")   # capturas de Wikimedia Commons (CC) y webs del barco
PHOTOS, total = {}, 0
for key, files in GROUPS.items():
    uris = []
    for fn in files:
        p = os.path.join(SRC, fn)
        if not os.path.exists(p):
            print("MISSING:", p); continue
        uri, sz = optimize(p); uris.append(uri); total += sz
    PHOTOS[key] = uris
for fn in sorted(os.listdir(WEB)):
    if fn.endswith(".png"):
        uri, sz = optimize(os.path.join(WEB, fn)); PHOTOS["w_" + fn[:-4]] = [uri]; total += sz

print("TOTAL embebido:", round(total/1024/1024, 2), "MB")
with open(os.path.join(os.path.dirname(__file__), "photos_data.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nPHOTOS = {\n")
    for k, uris in PHOTOS.items():
        f.write(f"  {k!r}: [\n" + "".join(f"    {u!r},\n" for u in uris) + "  ],\n")
    f.write("}\n")
print("photos_data.py OK")
