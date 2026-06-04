from urllib import response

import requests


url = "https://api.open-meteo.com/v1/forecast"
response = requests.get(url)

print(response.status_code)