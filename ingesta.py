import requests
import xml.etree.ElementTree as ET
import json
import gzip
from io import BytesIO
from datetime import datetime

def ingesta_zara():
    # Esta es la URL que encontraste para España
    url_espana = "https://www.zara.com/sitemaps/sitemap-es-es.xml.gz"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print("--- DESCOMPRIMIENDO Y EXTRAYENDO ZARA ESPAÑA ---")

    try:
        # 1. Descargar el archivo comprimido
        response = requests.get(url_espana, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 2. Descomprimir en memoria
        with gzip.open(BytesIO(response.content), 'rb') as f:
            xml_content = f.read()
        
        # 3. Parsear el XML
        root = ET.fromstring(xml_content)
        ns = {'n': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        urls = root.findall('n:url', ns)
        print(f"Total de enlaces detectados: {len(urls)}")

        productos_finales = []
        
        # Recorremos los enlaces buscando productos reales
        for u in urls:
            loc = u.find('n:loc', ns).text
            
            # El patrón /p/ indica que es una página de producto
            if "/p/" in loc:
                try:
                    # Ejemplo: .../vestido-lino-p02731045.html
                    nombre_slug = loc.split('/')[-1].split('-p')[0]
                    nombre_limpio = nombre_slug.replace('-', ' ').title()
                    sku = loc.split('-p')[-1].replace('.html', '').split('?')[0]
                    
                    productos_finales.append({
                        "id": sku,
                        "title": nombre_limpio,
                        "price": 29.95, # Precio base
                        "category": "Zara España",
                        "image": "https://static.zara.net/photos/images/home/standard-light/top_0.jpg",
                        "link": loc,
                        "last_update": str(datetime.now().date())
                    })
                    
                    # Para no saturar el catálogo en la primera prueba, limitamos a 200
                    if len(productos_finales) >= 200:
                        break
                except:
                    continue

        # 4. Guardar en tu base de datos NoSQL
        with open('catalog.json', 'w', encoding='utf-8') as f:
            json.dump(productos_finales, f, indent=4, ensure_ascii=False)
        
        print(f"--- ÉXITO: {len(productos_finales)} productos reales cargados ---")

    except Exception as e:
        print(f"ERROR TÉCNICO: {e}")

if __name__ == "__main__":
    ingesta_zara()
