import os
from dotenv import load_dotenv

load_dotenv()

GRAPH_API_URL = os.getenv("GRAPH_API_URL")
NO_OF_DAYS = int(os.getenv("NO_OF_DAYS"))
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
