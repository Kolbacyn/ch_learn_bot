import asyncio
import logging
import time
from os import getenv

from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.scene import SceneRegistry, ScenesManager
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.filters.command import Command
from dotenv import load_dotenv

from callbacks import get_hsk_callback
from keyboards import main_menu, hsk_buttons
from quiz import QuizScene

logging.basicConfig(level=logging.INFO)

quiz_router = Router(name=__name__)
# Add handler that initializes the scene
quiz_router.message.register(QuizScene.as_handler(), Command("quiz"))


def create_dispatcher():
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation()
    )
    dispatcher.include_router(quiz_router)
    scene_registry = SceneRegistry(dispatcher)
    scene_registry.add(QuizScene)
    return dispatcher


load_dotenv()
dp = create_dispatcher()


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
        'Меня зовут Ханью и я твой помощник в изучении китайского'
        )
    time.sleep(1)
    await message.answer(
        'Выбери уровень подготовки',
        reply_markup=hsk_buttons
        )


@dp.callback_query(F.data == 'hsk_buttons_1')
async def send_hsk_buttons(callback: types.CallbackQuery):
    await callback.message.answer(
        'Пока для этого уровня доступны только карточки',
        reply_markup=main_menu)
    await callback.answer()


# @dp.callback_query(F.data == 'main_menu_btn_2')
# async def run_quiz(callback: types.CallbackQuery):


async def main():
    bot = Bot(token=getenv('BOT_TOKEN'))
    try:
        await dp.start_polling(bot)
    finally:
        bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
