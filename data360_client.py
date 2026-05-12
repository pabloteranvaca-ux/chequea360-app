import requests
import pandas as pd

BASE_URL = "https://api.worldbank.org/v2"

def fetch_worldbank_data(country_code, indicator_code):
    url = f"{BASE_URL}/country/{country_code}/indicator/{indicator_code}"

    params = {
        "format": "json",
        "per_page": 100
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()

    if len(data) < 2:
        return pd.DataFrame()

    rows = []

    for item in data[1]:
        if item["value"] is not None:
            rows.append({
                "year": int(item["date"]),
                "value": item["value"]
            })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    return df.sort_values("year")