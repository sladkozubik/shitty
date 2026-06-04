from dotenv import load_dotenv

import os
import requests

url = "https://api.open-meteo.com/v1/forecast"
response = requests.get(url)

print(response.status_code)


load_dotenv()

token = os.getenv("BOT_TOKEN")

print(token)