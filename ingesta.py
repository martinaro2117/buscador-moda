import requests
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

def ingesta_zara():
    # Sitemap de productos de Zara España
    url_sitemap = "https://www.zara.com/sitemaps/sitemap-es-es.xml"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print("--- INICIANDO EXTRACCIÓN REAL ---")

    try:
        response = requests.get(url_sitemap, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parseo del XML con el namespace de Zara
        root = ET.fromstring(response.content)
        ns = {'n': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        urls = root.findall('n:url', ns)
        print(f"He encontrado {len(urls)} enlaces totales en Zara.")

        lista_productos = []
        
        # Procesamos los primeros 100 enlaces que sean productos (/p/)
        for u in urls:
            link = u.find('n:loc', ns).text
            
            if "/p/" in link and len(lista_productos) < 100:
                try:
                    # Extraer nombre y ID del enlace
                    # Ejemplo: /vestido-punto-p01234567.html
                    parte_final = link.split('/')[-1]
                    nombre = parte_final.split('-p')[0].replace('-', ' ').title()
                    sku = parte_final.split('-p')[-1].replace('.html', '')
                    
                    lista_productos.append({
                        "id": sku,
                        "title": nombre,
                        "price": 29.95, # Precio base (Zara no lo da en el sitemap)
                        "category": "Nueva Colección",
                        "image": "https://static.zara.net/photos/images/home/standard-light/top_0.jpg",
                        "link": link,
                        "last_update": str(datetime.now().date())
                    })
                except:
                    continue

        # GUARDADO: Aquí es donde forzamos que se escriba todo
        archivo = 'catalog.json'
        
        # IMPORTANTE: Si quieres borrar los 2 que escribiste a mano,
        # simplemente guardamos la lista_productos directamente.
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(lista_productos, f, indent=4, ensure_ascii=False)
        
        print(f"--- ÉXITO: {len(lista_productos)} productos guardados en catalog.json ---")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    ingesta_zara()
