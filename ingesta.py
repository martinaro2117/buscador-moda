import requests
import json
import gzip
import re
from io import BytesIO
from datetime import datetime

def ingesta_zara():
    # URL del sitemap que ya sabemos que sí nos deja descargar
    url_final = "https://www.zara.com/sitemaps/sitemap-product-es-es.xml.gz"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print("--- INICIANDO EXTRACCIÓN DIRECTA (MODO SEGURO) ---")

    try:
        # Paso 1: Descargamos el archivo comprimido (Solo una petición)
        response = requests.get(url_final, headers=headers, timeout=30)
        response.raise_for_status()
        
        with gzip.open(BytesIO(response.content), 'rb') as f:
            xml_content = f.read().decode('utf-8')
        
        # Paso 2: Extraer todos los enlaces usando expresiones regulares
        urls = re.findall(r'<loc>(.*?)</loc>', xml_content)
        print(f"Total de enlaces encontrados en el sitemap: {len(urls)}")

        productos_finales = []
        
        # Paso 3: Procesar los datos a partir de la URL (sin entrar en la web)
        # Vamos a coger 100 productos de golpe
        for link in urls[:100]:
            if "/p/" not in link:
                continue
            
            try:
                # Extraemos la información del propio texto del enlace
                # Ejemplo: .../abrigo-lana-p01234567.html
                slug = link.split('/')[-1]
                nombre_raw = slug.split('-p')[0]
                nombre_limpio = nombre_raw.replace('-', ' ').title()
                sku = slug.split('-p')[-1].replace('.html', '')

                # Como no podemos entrar a por la foto real sin que nos bloqueen,
                # usamos una imagen elegante de "Próximamente" o el logo de Zara
                # para que tu buscador no se vea roto.
                foto_placeholder = "https://brandemia.org/sites/default/files/inline/images/zara_logo_antes_despues.jpg"

                productos_finales.append({
                    "id": sku,
                    "title": nombre_limpio,
                    "price": 39.95, # Precio genérico (el sitemap no da precios)
                    "category": "Nueva Colección",
                    "image": foto_placeholder,
                    "link": link,
                    "last_update": str(datetime.now().date())
                })
            except:
                continue

        # Paso 4: Guardar el catálogo
        with open('catalog.json', 'w', encoding='utf-8') as f:
            json.dump(productos_finales, f, indent=4, ensure_ascii=False)
        
        print(f"--- ÉXITO: {len(productos_finales)} productos guardados en catalog.json ---")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    ingesta_zara()
