import requests
import json

def obtener_organizaciones_paginadas():
    url = "https://api.openaire.eu/graph/v1/organizations"
    page_size = 5
    cursor = "*"  # cursor inicial para la primera página

    for pagina in range(1, 4):  # 3 páginas
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

        # Obtener el siguiente cursor
        cursor = data.get("header", {}).get("nextCursor")
        if not cursor:
            print("No hay más páginas.")
            break

if __name__ == "__main__":
    obtener_organizaciones_paginadas()
