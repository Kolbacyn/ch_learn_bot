import asyncio
import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from keyboards import build_main_menu_kb, build_flashcards_kb
from utilities.constants import (ButtonData, CommonMessage, FlashcardMessage,
                                 Numeric, Picture, Rules)
from utilities.utils import create_image, generate_flashcards

router = Router(name=__name__)


def make_summary(crct_answers: int, wrg_answers: int):
    """Creates a summary of correct and wrong answers"""
    return f'Верных ответов: {crct_answers}\nНеверных ответов: {wrg_answers}'


@router.callback_query(F.data == ButtonData.TRAIN_FLASHCARDS)
async def enter_flashcards(callback: types.CallbackQuery,
                           state: FSMContext,
                           step: int = 0):
    """Starts the flashcards interaction"""
    await state.clear()
    flashcards = generate_flashcards(10)
    if not step:
        await callback.message.answer(CommonMessage.WELCOME)
    try:
        flashcards[step]
    except IndexError:
        await callback.message.answer(CommonMessage.GAME_OVER)
        await state.clear()
        return
    await state.update_data(step=step)
    await state.update_data(flashcards=flashcards)
    logging.info(flashcards[step].front_side)
    await callback.message.answer(
        text=Rules.FLASHCARDS_RULES
    )
    await asyncio.sleep(1)
    await callback.message.answer(
        FlashcardMessage.START_FLASHCARDS
    )
    create_image(flashcards[step].front_side)
    await callback.message.answer_photo(
        photo=types.FSInputFile(Picture.FLASHCARD),
        reply_markup=build_flashcards_kb(step, flashcards)
    )
    await asyncio.sleep(0.5)
    await callback.answer()


@router.callback_query(F.data == ButtonData.FLASHCARD_FRONT_SIDE)
async def show_back_side(callback: types.CallbackQuery,
                         state: FSMContext):
    """Shows the back side of the flashcard"""
    data = await state.get_data()
    step = data.get('step')
    flashcards = data.get('flashcards')
    await callback.answer(text=flashcards[step].hint)


@router.callback_query(F.data.in_((ButtonData.FLASHCARD_CORRECT_ANSWER,
                                   ButtonData.FLASHCARD_WRONG_ANSWER)))
async def process_answer(callback: types.CallbackQuery,
                         state: FSMContext):
    """Processes the answer"""
    data = await state.get_data()
    step = data.get('step') + Numeric.ONE
    flashcards = data.get('flashcards')
    try:
        flashcards[step]
    except IndexError:
        await callback.answer()
        await callback.message.answer(CommonMessage.GAME_OVER)
        await state.clear()
        return
    create_image(flashcards[step].front_side)
    if callback.data == 'correct_answer':
        correct_answers = data.get('correct_answers',
                                   Numeric.ZERO) + Numeric.ONE
        await state.update_data(correct_answers=correct_answers)
    else:
        wrong_answers = data.get('wrong_answers',
                                 Numeric.ZERO) + Numeric.ONE
        await state.update_data(wrong_answers=wrong_answers)
    await callback.message.edit_media(
        types.InputMediaPhoto(
            media=types.FSInputFile(Picture.FLASHCARD)
            ),
        reply_markup=build_flashcards_kb(step, flashcards)
    )
    await state.update_data(step=step)
    await callback.answer()


@router.callback_query(F.data == ButtonData.FLASHCARD_LEAVE)
async def leave(callback: types.CallbackQuery,
                state: FSMContext):
    """Abrupts the flashcards interaction"""
    data = await state.get_data()
    correct_answers = data.get('correct_answers', Numeric.ZERO)
    wrong_answers = data.get('wrong_answers', Numeric.ZERO)
    content = make_summary(correct_answers, wrong_answers)
    await callback.message.edit_media(
        types.InputMediaPhoto(
            media=types.FSInputFile(Picture.GREETING),
            caption=content
            ),
        reply_markup=build_main_menu_kb()
        )
