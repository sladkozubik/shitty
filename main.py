import asyncio
import os
from importlib.metadata import version

from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from logic import current_weather_in_spb, save_json_data

load_dotenv()


dp = Dispatcher()
@dp.message(CommandStart())
async def cmd_start(message: Message):
    kb = [[types.KeyboardButton(text="Погода",request_location=True)],[types.KeyboardButton(text='Поделиться данными')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Нажмите кнопку ниже:", reply_markup=keyboard)




@dp.message(F.text == 'Поделиться локацией')
async def use_location(message: Message):
    await message.answer("Готово")

@dp.message(F.location)
async def get_location(message: Message):
    latitude = round(message.location.latitude, 4)
    longitude = round(message.location.longitude,4)
    current = current_weather_in_spb(latitude, longitude)
    await message.answer(f"Погода в регионе: {current}°C ")
    print('handler weather works')


@dp.message(F.text =="Поделиться данными")
async def get_message_dump(message: Message):
    userid = message.from_user.id
    print(userid)
    temp = message.model_dump_json(indent=4)
    print("before save")
    save_json_data(temp, userid)
    print("after save")
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