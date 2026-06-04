import asyncio
import os
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from logic import current_weather_current_point, save_json_data
import json


load_dotenv('.env')

dp = Dispatcher()

#хендлер, сратабывающий на /start. Создает две кнопки на месте ввода текста
@dp.message(CommandStart())
async def cmd_start(message: Message):
    kb = [[types.KeyboardButton(text="Погода", request_location=True)],
          [types.KeyboardButton(text='Поделиться данными')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Нажмите кнопку ниже:", reply_markup=keyboard)

'''хендлер, срабатывающий на получение локации.
    можно поделиться своей локацией, нажав на кнопку 'Погода',
     либо выбрать точку вручную с помощью встроенных инструментов телеги'''
@dp.message(F.location)
async def get_location(message: Message):
    latitude = round(message.location.latitude, 4)
    longitude = round(message.location.longitude, 4)
    current = current_weather_current_point(latitude, longitude)
    if current == None:
        await message.answer("Ошибка получения данных, попробуйте еще раз.")
    else:
        try:
            await message.answer(f"Погода в регионе: {current}°C ")
        except Exception as e:
            print(f'telegram error: {e}')
    user = message.from_user

    result =(f"{user.id} @{user.username or 'no_username'} использовал геопозицию:\n"
             f"lat: {message.location.latitude}\n"
             f"lon: {message.location.longitude}\n\n")
    print(result)
    os.makedirs("logs", exist_ok=True)
    with open(
        f"./logs/{message.from_user.id}.log","a", encoding="utf-8" ) as f:
        f.write(result)


@dp.message(F.text == "Поделиться данными")
async def get_message_dump(message: Message):
    userid = message.from_user.id
    print(userid)
    temp =json.dumps({'id':userid,
                      'text':message.text}, indent=4, ensure_ascii=False
                     )
    print(temp)

    save_json_data(temp, userid)
    print('handler data works')


@dp.message()
async def register_message(message: Message):
    await message.answer("Откройте контекстное меню рядом с полем ввода сообщения")
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
