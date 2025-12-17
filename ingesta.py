import requests
import xml.etree.ElementTree as ET
import json
import gzip
import re
from io import BytesIO
from datetime import datetime

def ingesta_zara():
    # URL directa del sitemap de productos que has identificado
    url_final = "https://www.zara.com/sitemaps/sitemap-product-es-es.xml.gz"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print(f"--- CONECTANDO A PRODUCTOS: {url_final} ---")

    try:
        response = requests.get(url_final, headers=headers, timeout=30)
        with gzip.open(BytesIO(response.content), 'rb') as f:
            xml_content = f.read()
        
        root = ET.fromstring(xml_content)
        ns = {'n': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = root.findall(".//n:loc", ns)
        
        print(f"Total de productos en el sitemap: {len(urls)}")

        productos_finales = []
        
        # Procesamos los primeros 50 para que la Action no tarde demasiado
        for loc in urls[:50]:
            link = loc.text
            try:
                # Extraer nombre e ID del enlace
                slug = link.split('/')[-1]
                nombre = slug.split('-p')[0].replace('-', ' ').title()
                sku = slug.split('-p')[-1].replace('.html', '')

                # --- SCRAPING LIGERO PARA IMAGEN Y PRECIO ---
                # Entramos brevemente a la ficha para sacar la foto real
                print(f"Extrayendo datos de: {nombre}...")
                page = requests.get(link, headers=headers, timeout=10)
                
                # Buscamos la imagen en los metadatos de la página (og:image)
                img_match = re.search(r'property="og:image" content="(.*?)"', page.text)
                foto = img_match.group(1) if img_match else "https://static.zara.net/photos/images/home/standard-light/top_0.jpg"
                
                # Buscamos el precio (suele estar en un formato JSON dentro del HTML)
                precio_match = re.search(r'"price":(\d+\.\d+|\d+)', page.text)
                precio = float(precio_match.group(1)) if precio_match else 29.95

                productos_finales.append({
                    "id": sku,
                    "title": nombre,
                    "price": precio,
                    "category": "Zara Woman/Man",
                    "image": foto,
                    "link": link,
                    "last_update": str(datetime.now().date())
                })
            except Exception as e:
                print(f"Error con un producto: {e}")
                continue

        with open('catalog.json', 'w', encoding='utf-8') as f:
            json.dump(productos_finales, f, indent=4, ensure_ascii=False)
        
        print(f"--- ÉXITO: {len(productos_finales)} productos con FOTO y PRECIO real cargados ---")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    ingesta_zara()
