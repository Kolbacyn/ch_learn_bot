import asyncio
import logging

from aiogram import F, Router, html, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.formatting import (Bold, as_key_value, as_list,
                                      as_numbered_list, as_section)

from keyboards import build_main_menu_kb, build_answers_kb
from utilities.constants import (Button, ButtonData, CommonMessage, Numeric,
                                 Rules)
from utilities.utils import generate_questions

router = Router(name=__name__)


def make_summary(answers: dict, questions: list):
    """Creates a summary of correct and wrong answers"""
    correct = 0
    incorrect = 0
    user_answers = []
    for step, quiz in enumerate(questions):
        answer = answers.get(step)
        is_correct = answer == quiz.correct_answer
        if is_correct:
            correct += Numeric.ONE
            icon = '✅'
        else:
            incorrect += Numeric.ONE
            icon = '❌'
        if answer is None:
            answer = 'нет ответа'
        user_answers.append(f'{icon} (Ваш ответ: {html.quote(answer)})')

    return as_list(
        as_section(
            Bold('Результаты:'),
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


@router.callback_query(F.data == ButtonData.TRAIN_QUIZ)
async def enter_quiz(callback: types.CallbackQuery,
                     state: FSMContext,
                     step: int = 0
                     ):
    """Starts the quiz"""
    questions = generate_questions(10)
    if not step:
        await callback.message.answer(CommonMessage.WELCOME)

    try:
        questions[step]
    except IndexError:
        await callback.message.answer(CommonMessage.GAME_OVER)
        await state.clear()
        return

    await state.update_data(step=step)
    await state.update_data(questions=questions)
    await callback.message.answer(
        text=Rules.QUIZ_RULES
    )
    await asyncio.sleep(Numeric.QUIZ_SLEEP)
    await callback.message.answer(
        CommonMessage.STARTING
    )
    await asyncio.sleep(Numeric.ONE)
    await callback.message.answer(
        questions[step].text,
        reply_markup=build_answers_kb(step, questions).
        as_markup(resize_keyboard=True)
    )
    await callback.answer()


@router.message(F.text != Button.CANCEL,
                F.text != Button.EXIT)
async def check_answer(message: types.Message,
                       state: FSMContext):
    """Checks if the user's answer is correct"""
    data = await state.get_data()
    step = data['step']
    answers = data.get('answers', {})
    answers[step] = message.text
    questions = data.get('questions')
    await state.update_data(answers=answers)
    await state.update_data(step=step + Numeric.ONE)
    logging.info(answers)
    step = step + Numeric.ONE
    if step == len(questions):
        content = make_summary(answers, questions)
        await message.answer(**content.as_kwargs(),
                             reply_markup=build_main_menu_kb())
        await message.answer(
            CommonMessage.GOOD_JOB,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
    else:
        await message.answer(
            questions[step].text,
            reply_markup=build_answers_kb(step, questions).
            as_markup(resize_keyboard=True)
        )


@router.message(F.text == Button.EXIT)
async def exit_game(message: types.Message,
                    state: FSMContext):
    """Exits the quiz"""
    data = await state.get_data()
    answers = data.get('answers', {})
    questions = data.get('questions')

    content = make_summary(answers, questions)
    await message.answer(**content.as_kwargs(),
                         reply_markup=build_main_menu_kb())
    await state.set_data({})
    await message.answer(
        CommonMessage.GOOD_JOB,
        reply_markup=ReplyKeyboardRemove()
        )


@router.message(F.text == Button.CANCEL)
async def back_step(message: types.Message,
                    state: FSMContext):
    """Returns to previous step"""
    data = await state.get_data()
    step = data.get('step')
    step -= Numeric.ONE
    questions = data.get('questions')
    await state.update_data(step=step)
    await message.answer(
        questions[step].text,
        reply_markup=build_answers_kb(step, questions).
        as_markup(resize_keyboard=True)
    )
