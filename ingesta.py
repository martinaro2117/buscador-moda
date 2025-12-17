import requests
import json
import gzip
import re
import time
from io import BytesIO
from datetime import datetime

def ingesta_zara():
    url_final = "https://www.zara.com/sitemaps/sitemap-product-es-es.xml.gz"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Referer': 'https://www.google.com/' # Engañamos al servidor
    }

    print("--- INICIANDO EXTRACCIÓN SIGILOSA ---")

    try:
        response = requests.get(url_final, headers=headers, timeout=30)
        with gzip.open(BytesIO(response.content), 'rb') as f:
            xml_content = f.read().decode('utf-8')
        
        urls = re.findall(r'<loc>(.*?)</loc>', xml_content)
        print(f"Total de enlaces en sitemap: {len(urls)}")

        productos_finales = []
        
        # Procesamos solo 20 para evitar bloqueos por ahora
        for link in urls[:20]:
            if "/p/" not in link: continue
            
            try:
                print(f"Visitando: {link.split('/')[-1]}...")
                res = requests.get(link, headers=headers, timeout=10)
                
                if res.status_code == 403:
                    print("Bloqueado por Zara (403). Saltando...")
                    continue

                html = res.text

                # Extraer Título
                title_match = re.search(r'property="og:title" content="(.*?)"', html)
                title = title_match.group(1).split('|')[0].strip() if title_match else "Producto Zara"

                # Extraer Imagen (Intentamos og:image y si no la imagen de Twitter)
                img_match = re.search(r'property="og:image" content="(.*?)"', html)
                if not img_match:
                    img_match = re.search(r'name="twitter:image" content="(.*?)"', html)
                
                image = img_match.group(1) if img_match else ""

                # Extraer Precio
                price_match = re.search(r'"price":\s*"([\d.]+)"', html)
                if not price_match:
                    price_match = re.search(r'priceCurrency" content="EUR" />\s*<meta content="([\d.]+)"', html)
                
                price = price_match.group(1) if price_match else "39.95"

                sku = link.split('-p')[-1].replace('.html', '')

                if image:
                    productos_finales.append({
                        "id": sku,
                        "title": title,
                        "price": float(price),
                        "category": "Nueva Colección",
                        "image": image,
                        "link": link,
                        "last_update": str(datetime.now().date())
                    })
                    print(f"✅ Guardado: {title}")
                
                # PAUSA DE SEGURIDAD: 2 segundos entre peticiones
                time.sleep(20)

            except Exception as e:
                print(f"Error en este producto: {e}")
                continue

        with open('catalog.json', 'w', encoding='utf-8') as f:
            json.dump(productos_finales, f, indent=4, ensure_ascii=False)
        
        print(f"--- PROCESO FINALIZADO: {len(productos_finales)} productos cargados ---")

    except Exception as e:
        print(f"ERROR GENERAL: {e}")

if __name__ == "__main__":
    ingesta_zara()
