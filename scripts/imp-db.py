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
    if 'attributes' in event and 'dtstart' in event['attributes']:
        dtstart = event['attributes']['dtstart']
        dt = datetime.datetime.fromtimestamp(dtstart)
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
        print("Date de début de l'événement : ", formatted_date)
    else:
        print("La date de début n'est pas disponible pour cet événement.")


else:
    print("Erreur lors de la récupération de la liste des événements : code ", response.status_code)
