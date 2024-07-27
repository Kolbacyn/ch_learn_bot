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

from routers import router as main_router
import utilities.constants as constants

logging.basicConfig(level=logging.INFO)

users: dict[int, dict[str, list]] = {}


def create_dispatcher():
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation()
    )
    dispatcher.include_router(main_router)
    # dispatcher.include_router(quiz_router)
    # dispatcher.include_router(handlers.router)
    # scene_registry = SceneRegistry(dispatcher)
    # ... and then register a scene in the registry
    # by default, Scene will be mounted to the router that passed to the SceneRegistry,
    # but you can specify the router explicitly using the `router` argument
    # scene_registry.add(QuizScene)
    return dispatcher


load_dotenv()
dp = create_dispatcher()


async def main():
    bot = Bot(token=getenv('BOT_TOKEN'))
    try:
        await dp.start_polling(bot)
    finally:
        bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
