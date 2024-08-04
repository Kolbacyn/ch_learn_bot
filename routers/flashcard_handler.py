import asyncio
import logging

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards import build_main_menu_kb
from utilities import constants
from utilities.utils import generate_flashcard, create_image


router = Router(name=__name__)

FLASHCARDS = [generate_flashcard() for _ in range(100)]


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


def make_summary(correct_answers: int, wrong_answers: int):
    return f'Верных ответов: {correct_answers}\nНеверных ответов: {wrong_answers}'


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
    data = await state.get_data()
    step = data.get('step')
    await callback.answer(text=FLASHCARDS[step].hint)


@router.callback_query(F.data == 'correct_answer')
async def correct_answer(callback: types.CallbackQuery,
                         state: FSMContext):
    data = await state.get_data()
    step = data.get('step') + 1
    correct_answers = data.get('correct_answers', 0) + 1
    create_image(FLASHCARDS[step].front_side)
    await state.update_data(correct_answers=correct_answers)
    await callback.message.edit_media(
        types.InputMediaPhoto(
            media=types.FSInputFile('biffer.png')
            ),
        reply_markup=build_flashcards_kb(step)
    )
    await state.update_data(step=step)
    await callback.answer()


@router.callback_query(F.data == 'wrong_answer')
async def wrong_answer(callback: types.CallbackQuery,
                       state: FSMContext):
    data = await state.get_data()
    step = data.get('step') + 1
    wrong_answers = data.get('wrong_answers', 0) + 1
    create_image(FLASHCARDS[step].front_side)
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
