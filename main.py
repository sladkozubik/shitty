import asyncio
import os
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from logic import fetch_current_weather, save_json_data
import json

load_dotenv('.env')

dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    kb = [[types.KeyboardButton(text="Погода", request_location=True)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Нажмите кнопку ниже:", reply_markup=keyboard)


@dp.message(F.location)
async def get_location(message: Message):
    location = message.location
    latitude = round(location.latitude, 4)
    longitude = round(location.longitude, 4)
    c_temp, c_wind, c_humidity = fetch_current_weather(latitude, longitude)
    data = {
        "temperature": c_temp,
        "wind": c_wind,
        "humidity": c_humidity,
    }
    if None in (c_temp, c_wind, c_humidity):

        failed = [name for name, value in data.items() if value is None]
        await message.answer(f"Ошибка в обработке данных. Обратобать не удалось: {failed}")


    else:
        try:
            await message.answer(
                f"Погода в регионе:\n"
                f"Температура: {c_temp}°C\n"
                f"Скорость ветра: {c_wind} м/с\n"
                f"Относительная влажность: {c_humidity}%"
            )
        except Exception as e:
            print(f'telegram error: {e}')
    user = message.from_user

    result = (f"{user.id} @{user.username or 'no_username'} использовал геопозицию:\n"
              f"lat: {message.location.latitude}\n"
              f"lon: {message.location.longitude}\n\n")
    print(result)
    os.makedirs("logs", exist_ok=True)
    with open(
            f"./logs/{message.from_user.id}.log", "a", encoding="utf-8") as f:
        f.write(result)


@dp.message()
async def register_message(message: Message):
    temp = json.dumps({'id': message.from_user.id,
                       'nickname': message.from_user.username or 'no_username',
                       'text': message.text}, indent=4, ensure_ascii=False
                      )
    print(temp)

    save_json_data(temp, message.from_user.id)
    await message.answer(
        "Откройте контекстное меню рядом с полем ввода сообщения\n"
        "или выберите точку на карте с помощью встроенного инструмента Telegram.")
    print('handler random text works')


async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        error = 'not token provided'
        raise ValueError(error)
    bot = Bot(token=token)

    print('starting bot...')
    try:
        await dp.start_polling(bot)
    finally:
        print('closing bot...')


if __name__ == '__main__':
    asyncio.run(main())
