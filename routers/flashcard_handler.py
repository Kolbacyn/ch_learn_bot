import logging

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards import build_main_menu_kb
from utilities import constants
from utilities.utils import generate_flashcard


router = Router(name=__name__)

FLASHCARDS = [generate_flashcard() for _ in range(10)]


def build_flashcards_kb(step):
    first_button = InlineKeyboardButton(text=FLASHCARDS[step].front_side,
                                        callback_data='front_side')
    second_button = InlineKeyboardButton(text='✅',
                                         callback_data='correct_answer')
    third_button = InlineKeyboardButton(text='❌',
                                        callback_data='wrong_answer')
    fourth_button = InlineKeyboardButton(text='Выйти', callback_data='leave')
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [first_button],
            [second_button, third_button],
            [fourth_button]
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
    await callback.message.answer(
        f'Flashcard # {step}',
        reply_markup=build_flashcards_kb(step)
    )
    await callback.answer()


@router.callback_query(F.data == 'front_side')
async def show_back_side(callback: types.CallbackQuery,
                         state: FSMContext):
    data = await state.get_data()
    step = data.get('step')
    await callback.message.answer(FLASHCARDS[step].back_side)
    await callback.answer()


@router.callback_query(F.data == 'correct_answer')
async def correct_answer(callback: types.CallbackQuery,
                         state: FSMContext):
    data = await state.get_data()
    step = data.get('step') + 1
    await callback.message.edit_text(f'flashcard # {step}',
                                     reply_markup=build_flashcards_kb(step))
    await state.update_data(step=step)
    await callback.answer()


@router.callback_query(F.data == 'wrong_answer')
async def wrong_answer(callback: types.CallbackQuery,
                       state: FSMContext):
    data = await state.get_data()
    step = data.get('step') + 1
    await callback.message.edit_text(f'flashcard # {step}',
                                     reply_markup=build_flashcards_kb(step))
    await state.update_data(step=step)
    await callback.answer()


@router.callback_query(F.data == 'leave')
async def leave(callback: types.CallbackQuery,
                state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text='constants.GAME_OVER_MSG',
                                     reply_markup=build_main_menu_kb())
