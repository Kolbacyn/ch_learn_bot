from aiogram import Bot
from aiogram.types import CallbackQuery

from keyboards import hsk_buttons


async def get_hsk_callback(call: CallbackQuery, bot: Bot):
    message = 'Choose level'
    await call.message.answer(message, reply_markup=hsk_buttons)
    await call.answer()
