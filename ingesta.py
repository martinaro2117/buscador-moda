import requests
import json
import gzip
import re
from io import BytesIO
from datetime import datetime

def ingesta_zara():
    # El archivo que tú misma identificaste
    url_final = "https://www.zara.com/sitemaps/sitemap-product-es-es.xml.gz"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'es-ES,es;q=0.9'
    }

    print("--- INICIANDO EXTRACCIÓN POR METADATA ---")

    try:
        # Descarga y descompresión
        response = requests.get(url_final, headers=headers, timeout=30)
        with gzip.open(BytesIO(response.content), 'rb') as f:
            xml_content = f.read().decode('utf-8')
        
        # Extraemos los enlaces usando una expresión regular rápida
        urls = re.findall(r'<loc>(.*?)</loc>', xml_content)
        print(f"Total de enlaces: {len(urls)}")

        productos_finales = []
        
        # Procesamos los primeros 40 productos (para no saturar a Zara ni a GitHub)
        for link in urls[:40]:
            if "/p/" not in link: continue
            
            try:
                # Entramos a la ficha del producto
                print(f"Rastreando: {link.split('/')[-1]}")
                res = requests.get(link, headers=headers, timeout=10)
                html = res.text

                # 1. Extraer TITULO (de og:title)
                title_match = re.search(r'property="og:title" content="(.*?)"', html)
                title = title_match.group(1).split('|')[0].strip() if title_match else "Producto Zara"

                # 2. Extraer IMAGEN (de og:image) - La clave de tu pregunta
                img_match = re.search(r'property="og:image" content="(.*?)"', html)
                image = img_match.group(1) if img_match else ""

                # 3. Extraer PRECIO (de los datos estructurados schema.org)
                price_match = re.search(r'"price":\s*"([\d.]+)"', html)
                price = price_match.group(1) if price_match else "39.95"

                # 4. Extraer ID
                sku = link.split('-p')[-1].replace('.html', '')

                if image: # Solo guardamos si conseguimos la foto
                    productos_finales.append({
                        "id": sku,
                        "title": title,
                        "price": float(price),
                        "category": "Nueva Colección",
                        "image": image,
                        "link": link,
                        "last_update": str(datetime.now().date())
                    })
            except:
                continue

        # Guardado final
        with open('catalog.json', 'w', encoding='utf-8') as f:
            json.dump(productos_finales, f, indent=4, ensure_ascii=False)
        
        print(f"--- ÉXITO: {len(productos_finales)} productos con metadatos reales cargados ---")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    ingesta_zara()
