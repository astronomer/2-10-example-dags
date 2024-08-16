import requests
from requests.auth import HTTPBasicAuth

USERNAME = "admin"
PASSWORD = "admin"
HOST = "http://localhost:8080"
DATASET_URI = "dataset0"
EXTRA = {"foo": "bar"}

event_payload = {"dataset_uri": DATASET_URI, "extra": EXTRA}

url = f"{HOST}/api/v1/datasets/queuedEvent/x-dataset1"

response = requests.get(
    url, json=event_payload, auth=HTTPBasicAuth(USERNAME, PASSWORD)
)

print(response.json())