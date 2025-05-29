import requests
import argparse
from pymongo import MongoClient
import itertools

def obtener_organizaciones_paginadas(db, per_page=10, total_pages=None):
    url = "https://api.openaire.eu/graph/v1/organizations"
    page_size = per_page
    cursor = "*"  # cursor inicial para la primera página

    if total_pages is None or total_pages <= 0:
        it = itertools.count(1)
    else:
        it = range(1, total_pages + 1)

    for pagina in it:
        params = {
            "pageSize": page_size,
            "cursor": cursor
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error en la solicitud: {response.status_code}")
            print(response.text)
            break

        data = response.json()

        print(f"\n--- Página {pagina} ---")
        for org in data.get("results", []):
            print(f"ID: {org.get('id')}, Nombre: {org.get('legalName')}")
            # Guardar la organización en MongoDB
            db.organizaciones.insert_one(org)

        # Obtener el siguiente cursor
        cursor = data.get("header", {}).get("nextCursor")
        if not cursor:
            print("No hay más páginas.")
            break

def abrir_conexion_mongo():
    # abre una conexión a MongoDB en localhost:27017
    client = MongoClient("mongodb://localhost:27017/")
    db = client["openaire"]
    return db
    
def main():
    parser = argparse.ArgumentParser(description="Procesa elementos por páginas.")
    parser.add_argument('--per-page', type=int, default=10, help='Número de elementos por página')
    parser.add_argument('--total-pages', type=int, default=None, help='Número total de páginas a procesar (si no se especifica, procesa todas)')
    parser.add_argument('--drop', action='store_true', help='Vacía la colección antes de empezar')
    args = parser.parse_args()


    # Abrir conexión a MongoDB
    db = abrir_conexion_mongo()

    # Si se especifica --drop, vaciar la colección
    if args.drop:
        print("Vaciando la colección 'organizaciones'...")
        db.organizaciones.drop()

    print("Obteniendo organizaciones paginadas...")
    obtener_organizaciones_paginadas(db, args.per_page, args.total_pages)

    # Mostrar el número total de organizaciones guardadas
    total_organizaciones = db.organizaciones.count_documents({})
    print(f"\nTotal de organizaciones guardadas: {total_organizaciones}")

    # Cerrar la conexión a MongoDB
    db.client.close()

if __name__ == "__main__":
    main()
