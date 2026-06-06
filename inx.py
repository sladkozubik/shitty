import json

from dotenv import load_dotenv

import os
import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
        "latitude": 60.0000,
        "longitude": 30.0000,
        "timezone": "Europe/Moscow",
        "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",

    }
response = requests.get(url, params=params, timeout=10)
data = response.json()
with open('testfile.json', 'w') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
print(response.status_code)


load_dotenv()

token = os.getenv("BOT_TOKEN")

print(token)