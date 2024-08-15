import asyncio
import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards import build_main_menu_kb
from utilities import constants
from utilities.utils import create_image, generate_flashcard

router = Router(name=__name__)

FLASHCARDS = [generate_flashcard() for _ in range(5)]


def build_flashcards_kb(step):
    """Adds buttons to the keyboard"""
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton(
        text=FLASHCARDS[step].front_side,
        callback_data='front_side')])
    inline_keyboard.append([
        InlineKeyboardButton(text='✅', callback_data='correct_answer'),
        InlineKeyboardButton(text='❌', callback_data='wrong_answer')])
    inline_keyboard.append([InlineKeyboardButton(
        text='Выйти', callback_data='leave')])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def make_summary(crct_answers: int, wrg_answers: int):
    """Creates a summary of correct and wrong answers"""
    return f'Верных ответов: {crct_answers}\nНеверных ответов: {wrg_answers}'


@router.callback_query(F.data == 'main_menu_btn_2')
async def enter_flashcards(callback: types.CallbackQuery,
                           state: FSMContext,
                           step: int = 0):
    """Starts the flashcards interaction"""
    await state.clear()
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
        text=constants.FLASHCARDS_RULES
    )
    await asyncio.sleep(1)
    await callback.message.answer(
        'Приступим!'
    )
    create_image(FLASHCARDS[step].front_side)
    await callback.message.answer_photo(
        photo=types.FSInputFile('biffer.png'),
        reply_markup=build_flashcards_kb(step)
    )
    await asyncio.sleep(0.5)
    await callback.answer()


@router.callback_query(F.data == 'front_side')
async def show_back_side(callback: types.CallbackQuery,
                         state: FSMContext):
    """Shows the back side of the flashcard"""
    data = await state.get_data()
    step = data.get('step')
    await callback.answer(text=FLASHCARDS[step].hint)


@router.callback_query(F.data.in_(('correct_answer', 'wrong_answer')))
async def process_answer(callback: types.CallbackQuery,
                         state: FSMContext):
    """Processes the answer"""
    data = await state.get_data()
    step = data.get('step') + 1
    try:
        FLASHCARDS[step]
    except IndexError:
        await callback.answer()
        await callback.message.answer(constants.GAME_OVER_MSG)
        await state.clear()
        return
    create_image(FLASHCARDS[step].front_side)
    if callback.data == 'correct_answer':
        correct_answers = data.get('correct_answers', 0) + 1
        await state.update_data(correct_answers=correct_answers)
    else:
        wrong_answers = data.get('wrong_answers', 0) + 1
        await state.update_data(wrong_answers=wrong_answers)
    await callback.message.edit_media(
        types.InputMediaPhoto(
            media=types.FSInputFile('biffer.png')
            ),
        reply_markup=build_flashcards_kb(step)
    )
    await state.update_data(step=step)
    await callback.answer()


@router.callback_query(F.data == 'leave')
async def leave(callback: types.CallbackQuery,
                state: FSMContext):
    """Abrupts the flashcardsinteraction"""
    data = await state.get_data()
    correct_answers = data.get('correct_answers', 0)
    wrong_answers = data.get('wrong_answers', 0)
    content = make_summary(correct_answers, wrong_answers)
    await callback.message.edit_media(
        types.InputMediaPhoto(
            media=types.FSInputFile(constants.GREETING_PICTURE),
            caption=content
            ),
        reply_markup=build_main_menu_kb()
        )
