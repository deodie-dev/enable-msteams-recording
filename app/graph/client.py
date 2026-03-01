import requests

GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


class GraphClient:
    def __init__(self, access_token: str):
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def get(self, endpoint: str, params: dict | None = None):
        url = f"{GRAPH_BASE_URL}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)

        if not response.ok:
            raise Exception(
                f"Graph API Error: {response.status_code} - {response.text}"
            )

        return response.json() 