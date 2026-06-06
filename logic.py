import json

import requests
import os
from aiogram.types import Message


def fetch_current_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f'Ошибка АПИ:{e}')
        return None, None, None

    data = response.json()
    current = data.get("current", {})
    temp = current.get("temperature_2m")
    pre_wind = current.get("wind_speed_10m")
    wind = round((pre_wind / 3.6), 2) if pre_wind is not None else None
    humidity = current.get("relative_humidity_2m")

    return temp, wind, humidity


def get_weather(lat: float, lon: float):
    c_temp, c_wind, c_humidity = fetch_current_weather(lat, lon)
    data = {
        "temperature": c_temp,
        "wind": c_wind,
        "humidity": c_humidity,
    }
    if None in (c_temp, c_wind, c_humidity):
        failed = [name for name, value in data.items() if value is None]
        return f"Ошибка в обработке данных. Обратобать не удалось: {failed}"
    return (
        f"Погода в регионе:\n"
        f"Температура: {c_temp}°C\n"
        f"Скорость ветра: {c_wind} м/с\n"
        f"Относительная влажность: {c_humidity}%"
    )


def save_call(msg: Message):
    user = msg.from_user
    location = msg.location
    result = (
        f"{user.id} @{user.username or 'no_username'} использовал геопозицию:\n"
        f"lat: {location.latitude}\n"
        f"lon: {location.longitude}\n\n"
    )
    print(result)
    os.makedirs("logs", exist_ok=True)
    with open(
            f"./logs/{user.id}.log", "a", encoding="utf-8") as f:
        f.write(result)


def save_json_data(json_data: dict, user_id: int):
    user_file = f'data_{user_id}.json'

    print(f'saving data to {user_file}')

    with open(user_file, "a", encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
        f.write('\n')
