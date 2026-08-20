import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("ESIOS_TOKEN")

headers = {
    "Accept": "application/json; application/vnd.esios-api-v2+json",
    "Content-Type": "application/json",
    "x-api-key": token
}

INDICATOR_ID = 1293  # Demanda real

def get_demand_data(start_date, end_date):
    url = f"https://api.esios.ree.es/indicators/{INDICATOR_ID}"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "time_trunc": "hour"
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    values = data["indicator"]["values"]
    df = pd.DataFrame(values)
    return df

if __name__ == "__main__":
    df = get_demand_data("2025-01-01T00:00:00", "2025-12-31T23:59:00")
    print(df.head())
    print(f"\nFiles descarregades: {len(df)}")
    df.to_csv("data/demand_2025_hourly.csv", index=False)