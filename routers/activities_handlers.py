import logging

from aiogram import types, html, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.formatting import (
    Bold,
    as_key_value,
    as_list,
    as_numbered_list,
    as_section,
)

from utilities.utils import generate_question

router = Router(name=__name__)

QUESTIONS = [generate_question() for _ in range(10)]


def build_answers_kb(step: int):
    kb = ReplyKeyboardBuilder()
    answers = QUESTIONS[step].answers
    kb.add(*[KeyboardButton(text=answer.text) for answer in answers])
    if step > 0:
        kb.button(text='🔙 Назад')
    kb.button(text='🚫 Выход')
    kb.adjust(2)
    return kb


def make_summary(answers: dict):
    correct = 0
    incorrect = 0
    user_answers = []
    for step, quiz in enumerate(QUESTIONS):
        answer = answers.get(step)
        is_correct = answer == quiz.correct_answer
        if is_correct:
            correct += 1
            icon = "✅"
        else:
            incorrect += 1
            icon = "❌"
        if answer is None:
            answer = 'нет ответа'
        user_answers.append(f'{quiz.text} ({icon} {html.quote(answer)})')

    content = as_list(
        as_section(
            Bold('Ваши ответы:'),
            as_numbered_list(*user_answers),
        ),
        '',
        as_section(
            Bold('Итого:'),
            as_list(
                as_key_value('Правильно', correct),
                as_key_value('Неправильно', incorrect),
            ),
        ),
    )
    return content


@router.callback_query(F.data == 'main_menu_btn_1')
async def enter_quiz(callback: types.CallbackQuery,
                     state: FSMContext,
                     step: int = 0
                     ):
    if not step:
        await callback.message.answer('Добро пожаловать в игру!')
    try:
        QUESTIONS[step]
    except IndexError:
        await callback.message.answer('Игра окончена!')
        await state.clear()
        return
    await state.update_data(step=step)
    await callback.message.answer(
        QUESTIONS[step].text,
        reply_markup=build_answers_kb(step).as_markup(resize_keyboard=True)
    )
    logging.info(QUESTIONS[step].answers)
    await callback.answer()


@router.message(F.text != '🚫 Выход', F.text != '🔙 Назад')
async def check_answer(message: types.Message,
                       state: FSMContext):
    data = await state.get_data()
    step = data['step']
    answers = data.get('answers', {})
    if step == len(QUESTIONS) - 1:
        content = make_summary(answers)
        await message.answer(**content.as_kwargs(),
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()
    answers[step] = message.text
    await state.update_data(answers=answers)
    await state.update_data(step=step + 1)
    logging.info(answers)
    step = step + 1
    await message.answer(
        QUESTIONS[step].text,
        reply_markup=build_answers_kb(step).as_markup(resize_keyboard=True)
    )


@router.message(F.text == '🚫 Выход')
async def exit_game(message: types.Message,
                    state: FSMContext):
    data = await state.get_data()
    answers = data.get('answers', {})

    content = make_summary(answers)
    await message.answer(**content.as_kwargs(),
                         reply_markup=ReplyKeyboardRemove())
    await state.set_data({})
    await message.answer('Пока!')


@router.message(F.text == '🔙 Назад')
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
