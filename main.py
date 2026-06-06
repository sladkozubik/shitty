import os, asyncio, json
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from logic import save_json_data, get_weather, save_call


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

    result = get_weather(latitude, longitude)

    save_call(message)

    await message.answer(result)


@dp.message()
async def register_message(message: Message):
    data = {'id': message.from_user.id,
            'nickname': message.from_user.username or 'no_username',
            'text': message.text
            }
    print(data)

    save_json_data(data, message.from_user.id)
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
