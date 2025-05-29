import requests
import json

# Palabra clave a buscar
query = "aupaeu"

# Endpoint actualizado de OpenAIRE Graph
url = f"https://api.openaire.eu/graph/v1/projects?search={query}"

# Realiza la solicitud
response = requests.get(url)

# Procesa la respuesta
if response.status_code == 200:
    try:
        data = response.json()
        results = data.get("results", [])
        
        # Mostrar resumen de cada proyecto
        if results:
            print("=== Resultados resumidos ===")
            for project in results:
                print(f"Título: {project.get('title', 'N/A')}")
                print(f"Acrónimo: {project.get('acronym', 'N/A')}")
                print(f"ID: {project.get('id', 'N/A')}")
                print(f"Fecha inicio: {project.get('startDate', 'N/A')}")
                print(f"Fecha fin: {project.get('endDate', 'N/A')}")
                print("-" * 40)
        else:
            print("No se encontraron proyectos con ese término.")

        # Mostrar JSON completo
        print("\n=== JSON completo de la respuesta ===")
        print(json.dumps(data, indent=2, ensure_ascii=False))

    except ValueError:
        print("La respuesta no es un JSON válido.")
else:
    print(f"Error {response.status_code}: {response.text}")
