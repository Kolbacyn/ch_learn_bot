import logging

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utilities.utils import generate_question


router = Router(name=__name__)

QUESTIONS = [generate_question() for _ in range(10)]
markup = ReplyKeyboardBuilder()
markup.add(*[KeyboardButton(text=answer.text) for answer in QUESTIONS[0].answers])


def build_answers_kb(step: int):
    kb = ReplyKeyboardBuilder()
    answers = QUESTIONS[step].answers
    kb.add(*[KeyboardButton(text=answer.text) for answer in answers])
    if step > 0:
        kb.button(text='🔙 Back')
    kb.button(text='🚫 Exit')
    kb.adjust(2)
    return kb


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
    await state.update_data(step=step)
    await callback.message.answer(
        QUESTIONS[step].text,
        reply_markup=build_answers_kb(step).as_markup(resize_keyboard=True)
    )
    logging.info(QUESTIONS[step].answers)
    await callback.answer()


@router.message(F.text != '🚫 Exit', F.text != '🔙 Back')
async def check_answer(message: types.Message,
                       state: FSMContext):
    data = await state.get_data()
    step = data['step']
    if step == len(QUESTIONS) - 1:
        await message.answer('Game over!',
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()
    answers = data.get('answers', {})
    answers[step] = message.text
    await state.update_data(answers=answers)
    await state.update_data(step=step + 1)
    logging.info(answers)
    step = step + 1
    await message.answer(
        QUESTIONS[step].text,
        reply_markup=build_answers_kb(step).as_markup(resize_keyboard=True)
    )


@router.message(F.text == '🚫 Exit')
async def exit_game(message: types.Message,
                    state: FSMContext):
    await message.answer('Game over!',
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await message.answer('Bye!')


@router.message(F.text == '🔙 Back')
async def back_step(message: types.Message,
                    state: FSMContext):
    data = await state.get_data()
    step = data.get('step')
    step -= 1
    await state.update_data(step=step)
    await message.answer(
        QUESTIONS[step].text,
        reply_markup=build_answers_kb(step).as_markup(resize_keyboard=True)
    )
