from aiogram import Router, types
from aiogram.types import Message
from utils import AttemptsQuantity, AttemptsCallback
import logging

router = Router()


@router.callback_query(AttemptsCallback.filter())
async def send_attempts(callback: types.CallbackQuery,
                        callback_data: AttemptsCallback):
    logging.info(callback_data)
    await callback.answer(
        text=f'Attempts: {callback_data.quantity}'
    )
    await callback.message.answer(
        text=f'Attempts: {callback_data.quantity}'
    )
