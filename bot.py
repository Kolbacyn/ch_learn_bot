import asyncio
import logging
import time
from os import getenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from dotenv import load_dotenv

from callbacks import get_hsk_callback
from keyboards import main_menu, hsk_buttons

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
load_dotenv()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    picture = types.FSInputFile('hey_pic.png')
    await message.answer_photo(picture)
    await message.answer(
        f'你好 <b>{message.from_user.full_name}</b>!',
        parse_mode=ParseMode.HTML
        )
    time.sleep(1)
    await message.answer(
        'Меня зовут Ханью и я твой помощник в изучении китайского',
        reply_markup=main_menu
        )


@dp.callback_query(F.data == 'main_menu_btn_1')
async def send_hsk_buttons(callback: types.CallbackQuery):
    await callback.message.answer('Choose level', reply_markup=hsk_buttons)
    await callback.answer()


async def main():
    bot = Bot(token=getenv('BOT_TOKEN'))
    try:
        await dp.start_polling(bot)
    finally:
        bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
