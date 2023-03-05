import requests

# Configuration de l'URL de base et des informations d'authentification
base_url = "http://localhost:8000/api"
auth = ("admin", "opencast")

# Récupération de la liste des événements
events_endpoint = "/events"
response = requests.get(base_url + events_endpoint, auth=auth)
if response.status_code == 200:
    events = response.json()
    print("Liste des événements :")
    for event in events["data"]:
        print(event["attributes"]["title"])
else:
    print("Erreur lors de la récupération de la liste des événements : code ", response.status_code)

