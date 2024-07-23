import asyncio
import logging
import time
from os import getenv

from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.filters.command import Command
from aiogram.fsm.scene import SceneRegistry, ScenesManager
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv

import constants
from handlers import router as attempts_router
from keyboards import build_hsk_kb, build_main_menu_kb, build_attempts_kb
from services.quizgame import quiz_router, QuizScene
from utils import get_word_from_database, AttemptsCallback


logging.basicConfig(level=logging.INFO)

flash_router = Router(name=__name__)

users: dict[int, dict[str, list]] = {}


def create_dispatcher():
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation()
    )
    dispatcher.include_router(flash_router)
    dispatcher.include_router(quiz_router)
    dispatcher.include_router(attempts_router)
    # dispatcher.include_router(handlers.router)
    scene_registry = SceneRegistry(dispatcher)
    # ... and then register a scene in the registry
    # by default, Scene will be mounted to the router that passed to the SceneRegistry,
    # but you can specify the router explicitly using the `router` argument
    scene_registry.add(QuizScene)
    return dispatcher


load_dotenv()
dp = create_dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {}
    picture = types.FSInputFile(constants.GREETING_PICTURE)
    await message.answer_photo(picture)
    await message.answer(
        f'你好 {message.from_user.full_name}!'
        )
    time.sleep(1)
    await message.answer(
        'Меня зовут Ханью и я твой помощник в изучении китайского языка'
        )
    time.sleep(1)
    await message.answer(
        'Выбери уровень подготовки',
        reply_markup=build_hsk_kb()
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
    await message.answer(constants.CANCEL_MESSAGE)


@dp.callback_query(F.data == 'hsk_buttons_1')
async def send_hsk_buttons(callback: types.CallbackQuery):
    await callback.message.answer(
        constants.START_TRAINING_MESSAGE,
        reply_markup=build_main_menu_kb())
    await callback.answer()


@dp.callback_query(F.data == 'main_menu_btn_1')
async def run_flashcards(callback: types.CallbackQuery, state: FSMContext):
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


# @dp.callback_query(AttemptsCallback.filter())
# async def set_attempts(callback: types.CallbackQuery,
#                        callback_data: AttemptsCallback):
#     logging.info(callback_data)
#     data = callback_data.quantity
#     await callback.message.answer(
#         'h'
#     )
#     print(data)
#     await callback.answer()


@dp.callback_query(F.data == 'main_menu_btn_2')
async def run_quiz(callback: types.CallbackQuery,
                   scenes: ScenesManager,
                   state: FSMContext = None):
    await callback.message.answer(
        'Выберете количество попыток:',
        reply_markup=build_attempts_kb(),
        )
    await state.update_data(step=-1)
    await scenes.enter(QuizScene)
    await callback.answer()


async def main():
    bot = Bot(token=getenv('BOT_TOKEN'))
    try:
        await dp.start_polling(bot)
    finally:
        bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
