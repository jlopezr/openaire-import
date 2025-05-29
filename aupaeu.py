import requests

# Palabra clave a buscar
query = "aupaeu"

# Endpoint actualizado y válido
url = f"https://api.openaire.eu/graph/v1/projects?search={query}"

# Realiza la solicitud GET
response = requests.get(url)

# Procesa la respuesta
if response.status_code == 200:
    data = response.json()
    results = data.get("results", [])
    if results:
        for project in results:
            print(f"Título: {project.get('title', 'N/A')}")
            print(f"Acrónimo: {project.get('acronym', 'N/A')}")
            print(f"ID: {project.get('id', 'N/A')}")
            print(f"Fecha inicio: {project.get('startDate', 'N/A')}")
            print(f"Fecha fin: {project.get('endDate', 'N/A')}")
            print("-" * 40)
    else:
        print("No se encontraron proyectos con ese término.")
else:
    print(f"Error {response.status_code}: {response.text}")
