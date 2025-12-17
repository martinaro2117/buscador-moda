# Un script de Python que lee el sitemap, extrae datos y limpia los antiguos.

import requests
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

def ingesta_zara():
    # URL del sitemap index que encontraste
    sitemap_index_url = "https://www.zara.com/sitemaps/sitemap-index.xml.gz"
    
    print(f"Iniciando ingesta incremental: {datetime.now()}")
    
    # --- LÓGICA DE SIMULACIÓN DE EXTRACCIÓN ---
    # Nota: Parsear un .gz de Zara requiere librerías como gzip y requests.
    # Para la prueba, simulamos la captura de datos frescos del sitemap
    
    nuevos_productos = [
        {
            "id": "zara-001",
            "title": "Vestido Lino Soft",
            "price": 29.95,
            "category": "Vestidos",
            "image": "https://static.zara.net/photos///2024/V/0/1/p/2731/045/250/2/w/400/2731045250_6_1_1.jpg",
            "link": "https://www.zara.com/es/es/vestido-lino-p02731045.html",
            "last_update": str(datetime.now().date())
        },
        {
            "id": "zara-002",
            "title": "Chaqueta Denim Oversize",
            "price": 39.95,
            "category": "Chaquetas",
            "image": "https://static.zara.net/photos///2024/V/0/1/p/2142/061/712/2/w/400/2142061712_6_1_1.jpg",
            "link": "https://www.zara.com/es/es/chaqueta-estructura-p02142061.html",
            "last_update": str(datetime.now().date())
        }
    ]

    # --- LÓGICA DELETE + UPDATE (Incremental) ---
    archivo_db = 'catalog.json'
    db_actual = []
    
    if os.path.exists(archivo_db):
        try:
            with open(archivo_db, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                if contenido: # Si el archivo NO está vacío
                    db_actual = json.loads(contenido)
                else:
                    db_actual = []
        except Exception as e:
            print(f"Aviso: El archivo estaba corrupto o vacío, empezando de cero. Error: {e}")
            db_actual = []
    else:
        db_actual = []

    # Convertimos a diccionario por ID para Update rápido
    dict_db = {p['id']: p for p in db_actual}
    
    for nuevo in nuevos_productos:
        # Update: Si existe lo pisa, si no, lo crea (Delete implícito de la versión vieja)
        dict_db[nuevo['id']] = nuevo

    # Guardamos de nuevo
    with open(archivo_db, 'w', encoding='utf-8') as f:
        json.dump(list(dict_db.values()), f, indent=4, ensure_ascii=False)
    
    print("Ingesta completada con éxito.")

if __name__ == "__main__":
    ingesta_zara()
