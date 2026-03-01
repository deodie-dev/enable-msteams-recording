import requests
from app.settings import GRAPH_API_URL, CLIENT_ID, CLIENT_SECRET


def get_global_graph_token():
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default"
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(GRAPH_API_URL, data=payload, headers=headers)

    if response.ok:
        return response.json().get("access_token")

    raise Exception(f"Graph Auth Failed: {response.status_code} - {response.text}")