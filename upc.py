import requests
import json

def obtenir_info_upc():
    url = "https://api.openaire.eu/graph/v1/organizations"
    params = {
        "search": "Universitat Politècnica de Catalunya",
        "pageSize": 10
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print("JSON complet rebut de l'API:")
        print(json.dumps(data, indent=2, ensure_ascii=False))  # Print JSON ben formatat i amb accents
        if "results" in data and data["results"]:
            org = data["results"][0]
            print("\nInformació resumida de la UPC:")
            print(f"ID: {org.get('id')}")
            print(f"Nom: {org.get('name')}")
            print(f"Ciutat: {org.get('city')}")
            print(f"País: {org.get('country')}")
            print(f"URL: {org.get('url')}")
            print(f"Descripció: {org.get('description')}")
        else:
            print("No s'ha trobat cap organització.")
    else:
        print(f"Error en la sol·licitud: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    obtenir_info_upc()
