import logging

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utilities import constants
from utilities.utils import generate_flashcard


router = Router(name=__name__)

FLASHCARDS = [generate_flashcard() for _ in range(10)]


def build_flashcards_kb(step):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=FLASHCARDS[step].front_side,
                                     callback_data=f'{FLASHCARDS[step].front_side}')
            ],
            [
                InlineKeyboardButton(text='✅',
                                     callback_data='correct_answer'),
            ],
            [
                InlineKeyboardButton(text='❌',
                                     callback_data='wrong_answer'),
            ]
        ]
    )
    return kb


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
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=FLASHCARDS[step].back_side,
                                     callback_data=f'{FLASHCARDS[step].back_side}')
            ]
        ]
    )
    await callback.message.answer(
        'Flashcard',
        reply_markup=build_flashcards_kb(step)
    )
    await callback.answer()
