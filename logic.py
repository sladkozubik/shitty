import requests


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


def save_json_data(json_data: str, user_id: int):
    user_file = f'data{user_id}.json'
    print(f'saving data to {user_file}')
    with open(user_file, "a", encoding='utf-8') as f:
        f.write(json_data+ '\n')

