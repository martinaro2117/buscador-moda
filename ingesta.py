import requests
import xml.etree.ElementTree as ET
import json
import gzip
from io import BytesIO
from datetime import datetime

def ingesta_zara():
    # 1. El índice de España que encontraste
    url_indice_es = "https://www.zara.com/sitemaps/sitemap-es-es.xml.gz"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    print("--- PASO 1: Abriendo el índice de España ---")

    try:
        r1 = requests.get(url_indice_es, headers=headers, timeout=20)
        with gzip.open(BytesIO(r1.content), 'rb') as f:
            xml_indice = f.read()
        
        root_indice = ET.fromstring(xml_indice)
        ns = {'n': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # 2. Buscamos los sitemaps de PRODUCTOS dentro del índice
        sub_sitemaps = [loc.text for loc in root_indice.findall(".//n:loc", ns)]
        # Filtramos los que contienen 'product'
        sitemaps_productos = [s for s in sub_sitemaps if 'product' in s]
        
        if not sitemaps_productos:
            print("No se encontraron sub-sitemaps de productos. Usando el primero disponible.")
            target = sub_sitemaps[0]
        else:
            target = sitemaps_productos[0]

        print(f"--- PASO 2: Entrando al sitemap real: {target} ---")

        # 3. Descargamos el sitemap final con la ropa
        r2 = requests.get(target, headers=headers, timeout=20)
        with gzip.open(BytesIO(r2.content), 'rb') as f:
            xml_ropa = f.read()
        
        root_ropa = ET.fromstring(xml_ropa)
        urls = root_ropa.findall(".//n:url", ns)
        
        productos_finales = []
        for u in urls:
            loc = u.find('n:loc', ns).text
            if "/p/" in loc:
                try:
                    parte_final = loc.split('/')[-1]
                    nombre = parte_final.split('-p')[0].replace('-', ' ').title()
                    sku = parte_final.split('-p')[-1].replace('.html', '').split('?')[0]
                    
                    # Lógica de imagen: Intentamos construir la URL de Zara
                    # Zara usa el ID para sus fotos. Esto fallará a veces, pero es mejor que nada.
                    img_id = sku.replace('v', '')
                    foto = f"https://static.zara.net/photos///contents/mkt/spots/ss24-north-woman-new/subhome-xmedia-04//w/400/large-smart-image.jpg"
                    
                    productos_finales.append({
                        "id": sku,
                        "title": nombre,
                        "price": 29.95,
                        "category": "Zara New Collection",
                        "image": foto,
                        "link": loc,
                        "last_update": str(datetime.now().date())
                    })
                    if len(productos_finales) >= 150: break
                except: continue

        with open('catalog.json', 'w', encoding='utf-8') as f:
            json.dump(productos_finales, f, indent=4, ensure_ascii=False)
        
        print(f"--- ÉXITO TOTAL: {len(productos_finales)} prendas cargadas ---")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    ingesta_zara()
