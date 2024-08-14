import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from dotenv import load_dotenv

from routers import router as main_router

logging.basicConfig(level=logging.INFO)


def create_dispatcher():
    """Creates the dispatcher"""
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation()
    )
    dispatcher.include_router(main_router)
    return dispatcher


load_dotenv()
dp = create_dispatcher()


async def main():
    """Starts the bot"""
    bot = Bot(token=getenv('BOT_TOKEN'))
    try:
        await dp.start_polling(bot)
    finally:
        bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
