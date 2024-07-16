import asyncio
import logging
import time
from os import getenv
from random import choice

from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.filters.command import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scrapy_hsk.models import Base, Word

from keyboards import main_menu, hsk_buttons


logging.basicConfig(level=logging.INFO)

flash_router = Router(name=__name__)

engine = create_engine('sqlite:///sqlite.db', echo=False)
Base.metadata.create_all(engine)
session = Session(engine)


def create_dispatcher():
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation()
    )
    dispatcher.include_router(flash_router)
    # dispatcher.include_router(handlers.router)
    return dispatcher


load_dotenv()
dp = create_dispatcher()


def get_word_from_database():
    word = choice(session.query(Word).all())
    return word



@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    picture = types.FSInputFile('hey_pic.png')
    await message.answer_photo(picture)
    await message.answer(
        f'你好 <b>{message.from_user.full_name}</b>!' 
        )
    time.sleep(1)
    await message.answer(
        'Меня зовут Ханью и я твой помощник в изучении китайского языка'
        )
    time.sleep(1)
    await message.answer(
        'Выбери уровень подготовки',
        reply_markup=hsk_buttons
        )


@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(
        'Это бот-помощник в изучении китайского языка.'
        )
    await message.answer(
        'Для начала тренировки отправьте /start и выберите уровень подготовки.'
        )


@dp.message(Command('cancel'))
async def cmd_cancel(message: types.Message):
    await message.answer('Тренировка отменена')


@dp.callback_query(F.data == 'hsk_buttons_1')
async def send_hsk_buttons(callback: types.CallbackQuery):
    await callback.message.answer(
        'Приступим к тренировке!',
        reply_markup=main_menu)
    await callback.answer()


@dp.callback_query(F.data == 'main_menu_btn_1')
async def run_quiz(callback: types.CallbackQuery, state: FSMContext):
    words = [get_word_from_database() for i in range(4)]
    hanzi = words[0].word
    text = f'Переведите на русский язык: {hanzi}'
    translation = words[0].rus_translation
    ans_one = words[1].rus_translation
    ans_two = words[2].rus_translation
    ans_three = words[3].rus_translation
    await callback.message.answer(
        text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=translation),
                    KeyboardButton(text=ans_one)],
                [KeyboardButton(text=ans_two),
                    KeyboardButton(text=ans_three)],
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        ))
    await callback.answer()


async def main():
    bot = Bot(token=getenv('BOT_TOKEN'))
    try:
        await dp.start_polling(bot)
    finally:
        bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
