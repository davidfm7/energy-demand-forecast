import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("ESIOS_TOKEN")

headers = {
    "Accept": "application/json; application/vnd.esios-api-v2+json",
    "Content-Type": "application/json",
    "x-api-key": token
}

response = requests.get("https://api.esios.ree.es/indicators", headers=headers)

print("Status code:", response.status_code)
print(response.json()["indicators"][:5])  