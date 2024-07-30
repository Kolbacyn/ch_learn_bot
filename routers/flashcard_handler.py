import logging

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utilities import constants
from utilities.utils import generate_flashcard


router = Router(name=__name__)

FLASHCARDS = [generate_flashcard() for _ in range(10)]


@router.callback_query(F.data == 'main_menu_btn_2')
async def enter_flashcards(callback: types.CallbackQuery,
                           state: FSMContext,
                           step: int = 0):
    if not step:
        await callback.message.answer(constants.WELCOME_MSG)
    try:
        FLASHCARDS[step]
    except IndexError:
        await callback.message.answer(constants.GAME_OVER_MSG)
        await state.clear()
        return
    await state.update_data(step=step)
    logging.info(FLASHCARDS[step].front_side)

    markup = ReplyKeyboardMarkup(
        keyboard=KeyboardButton(FLASHCARDS[step].front_side))
    await callback.message.answer(
        reply_markup=markup,
    )
    await callback.answer()
