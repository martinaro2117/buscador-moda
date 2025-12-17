import requests
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

def ingesta_zara():
    # URL maestra de Zara
    url_maestra = "https://www.zara.com/sitemaps/sitemap-index.xml"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print("--- INICIANDO EXTRACCIÓN INTELIGENTE ---")

    try:
        # 1. Buscamos el sitemap específico de productos España
        resp_maestra = requests.get(url_maestra, headers=headers, timeout=20)
        resp_maestra.raise_for_status()
        
        root_maestra = ET.fromstring(resp_maestra.content)
        ns = {'n': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Buscamos el sitemap que contenga 'product' y 'es-es' o simplemente el primero de productos
        sitemaps = [loc.text for loc in root_maestra.findall(".//n:loc", ns)]
        
        # Filtramos para encontrar el de España (suelen tener 'es' o ser los primeros de la lista)
        # Intentamos buscar uno de productos de España
        target_sitemap = None
        for s in sitemaps:
            if 'product' in s and '-es-' in s:
                target_sitemap = s
                break
        
        if not target_sitemap:
            # Si no encontramos el de España específico, cogemos el primero de productos
            target_sitemap = [s for s in sitemaps if 'product' in s][0]

        print(f"Sitemap encontrado: {target_sitemap}")

        # 2. Leemos el sitemap de productos
        response = requests.get(target_sitemap, headers=headers, timeout=20)
        root = ET.fromstring(response.content)
        
        urls = root.findall('n:url', ns)
        print(f"Total de enlaces encontrados: {len(urls)}")

        productos_finales = []
        
        for url in urls[:100]:
            loc = url.find('n:loc', ns).text
            
            if "/p/" in loc:
                try:
                    # Extraer ID y Título del enlace
                    nombre_it = loc.split('/')[-1].split('-p')[0].replace('-', ' ').title()
                    sku = loc.split('-p')[-1].replace('.html', '').split('?')[0]
                    
                    productos_finales.append({
                        "id": sku,
                        "title": nombre_it,
                        "price": 39.95, # Precio genérico
                        "category": "Nueva Colección",
                        "image": "https://static.zara.net/photos/images/home/standard-light/top_0.jpg",
                        "link": loc,
                        "last_update": str(datetime.now().date())
                    })
                except:
                    continue

        with open('catalog.json', 'w', encoding='utf-8') as f:
            json.dump(productos_finales, f, indent=4, ensure_ascii=False)
        
        print(f"--- ÉXITO: {len(productos_finales)} productos guardados ---")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    ingesta_zara()
