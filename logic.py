import json

import requests
from pprint import pprint

def current_weather_in_spb(lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"


    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()

        temp = data["current"]["temperature_2m"]
        return temp
    else:
        return "Нет ответа от сервера"

def save_json_data(json_data: str, user_id: int):

    user_file = f'data{user_id}.json'
    print(f'saving data to {user_file}')
    with open(user_file, "w", encoding='utf-8') as f:
        f.write(json_data)
