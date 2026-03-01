import os
import json
from dotenv import load_dotenv

load_dotenv()

GRAPH_API_URL = os.getenv("GRAPH_API_URL")
NO_OF_DAYS = int(os.getenv("NO_OF_DAYS"))
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

BASE_DIR = os.path.dirname(__file__)
RESTRICTED_PATH = os.path.join(
    BASE_DIR,
    "config",
    "restricted_meetings.json"
)

with open(RESTRICTED_PATH, "r") as file:
    RESTRICTED_USERS = json.load(file)
