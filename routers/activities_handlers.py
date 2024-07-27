import logging

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utilities.utils import generate_question


router = Router(name=__name__)

QUESTIONS = [generate_question() for _ in range(10)]
markup = ReplyKeyboardBuilder()
markup.add(*[KeyboardButton(text=answer.text) for answer in QUESTIONS[0].answers])


@router.callback_query(F.data == 'main_menu_btn_1')
async def enter_quiz(callback: types.CallbackQuery,
                     state: FSMContext,
                     step: int = 0
                     ):
    if not step:
        await callback.message.answer(
            'Welcome to the game!'
        )
    try:
        QUESTIONS[step]
    except IndexError:
        await callback.message.answer('Game over!')
        await state.clear()
        return
    if step > 0:
        markup.button(text="🔙 Back")
    markup.button(text="🚫 Exit")
    await state.update_data(step=step)
    await callback.message.answer(
        QUESTIONS[step].text,
        reply_markup=markup.adjust(2).as_markup(resize_keyboard=True)
    )
    await callback.answer()


@router.message(F.text)
async def check_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    step = data['step']
    answers = data.get('answers', {})
    answers[step] = message.text
    await state.update_data(answers=answers)
    await state.update_data(step=step + 1)
    logging.info(answers)


