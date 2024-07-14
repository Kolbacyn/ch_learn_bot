import asyncio
import logging
import time
from dataclasses import dataclass, field
from os import getenv
from random import choice

from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.filters.command import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scrapy_hsk.models import Base, Word

import handlers
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


@dataclass
class Answer:
    """"""
    text: str
    is_correct: bool = False


@dataclass
class Question:
    """"""
    text: str
    answers: list[Answer]
    correct_answer: str = field(init=False)

    def __post_init__(self):
        self.correct_answer = next(answer.text for answer in self.answers
                                   if answer.is_correct)


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


def get_word_from_database():
    word = choice(session.query(Word).all())
    return word


def generate_question():
    words = [get_word_from_database() for i in range(4)]
    hanzi = words[0].word
    text = f'Переведите на русский язык: {hanzi}'
    translation = words[0].rus_translation
    ans_one = words[1]
    ans_two = words[2]
    ans_three = words[3]
    question = Question(
        text=text,
        answers=[
            Answer(translation, is_correct=True),
            Answer(ans_one.rus_translation),
            Answer(ans_two.rus_translation),
            Answer(ans_three.rus_translation)
        ],
        resize_keyboard=True
    )
    return question


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
    ans_one = words[1]
    ans_two = words[2]
    ans_three = words[3]
    await callback.message.answer(
        text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=translation),
                    KeyboardButton(text=ans_one.rus_translation)],
                [KeyboardButton(text=ans_two.rus_translation),
                    KeyboardButton(text=ans_three.rus_translation)],
            ],
            resize_keyboard=True,
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
