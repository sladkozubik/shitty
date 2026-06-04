import requests


def current_weather_in_spb(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Ошибка АПИ:{e}')
        return None

    data = response.json()
    temp = data["current"]["temperature_2m"]
    return temp


def save_json_data(json_data: str, user_id: int):
    user_file = f'data{user_id}.json'
    print(f'saving data to {user_file}')
    with open(user_file, "a", encoding='utf-8') as f:
        f.write(json_data)
