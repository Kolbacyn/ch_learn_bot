from aiogram import Router, types
# from aiogram.types import Message
from keyboards import build_attempts_kb
from utils import AttemptsCallback
import logging

router = Router()


# @router.callback_query(AttemptsCallback.filter())
# async def send_attempts(callback: types.CallbackQuery,
#                         callback_data: AttemptsCallback):
#     logging.info(callback_data)
#     await callback.message.answer(
#         'Выберете количество попыток:',
#         reply_markup=build_attempts_kb(),
#         )
#     await callback.message.answer(
#         'h',
#         reply_markup=types.ReplyKeyboardRemove()
#     )
