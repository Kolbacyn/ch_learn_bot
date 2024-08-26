import asyncio
import logging

from aiogram import F, Router, html, types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.formatting import (Bold, as_key_value, as_list,
                                      as_numbered_list, as_section)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from keyboards import build_main_menu_kb
from utilities import constants
from utilities.constants import Button, Rules, CommonMessage, QuizMessage
from utilities.utils import generate_question

router = Router(name=__name__)

QUESTIONS = [generate_question() for _ in range(10)]


def build_answers_kb(step: int):
    """Creates the answers keyboard"""
    kb = ReplyKeyboardBuilder()
    answers = QUESTIONS[step].answers
    kb.add(*[KeyboardButton(text=answer.text) for answer in answers])
    if step > 0:
        kb.button(text=Button.CANCEL)
    kb.button(text=Button.EXIT)
    kb.adjust(2)
    return kb


def make_summary(answers: dict):
    """Creates a summary of correct and wrong answers"""
    correct = 0
    incorrect = 0
    user_answers = []
    for step, quiz in enumerate(QUESTIONS):
        answer = answers.get(step)
        is_correct = answer == quiz.correct_answer
        if is_correct:
            correct += 1
            icon = '✅'
        else:
            incorrect += 1
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


@router.callback_query(F.data == Button.QUIZ)
async def enter_quiz(callback: types.CallbackQuery,
                     state: FSMContext,
                     step: int = 0
                     ):
    """Starts the quiz"""
    if not step:
        await callback.message.answer(CommonMessage.WELCOME)
    try:
        QUESTIONS[step]
    except IndexError:
        await callback.message.answer(CommonMessage.GAME_OVER)
        await state.clear()
        return
    await state.update_data(step=step)
    await callback.message.answer(
        text=Rules.QUIZ_RULES
    )
    await asyncio.sleep(5)
    await callback.message.answer(
        CommonMessage.STARTING
    )
    await asyncio.sleep(0.3)
    await callback.message.answer(
        QUESTIONS[step].text,
        reply_markup=build_answers_kb(step).as_markup(resize_keyboard=True)
    )
    logging.info(QUESTIONS[step].answers)
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
    await state.update_data(answers=answers)
    await state.update_data(step=step + 1)
    logging.info(answers)
    step = step + 1
    if step == len(QUESTIONS):
        content = make_summary(answers)
        await message.answer(**content.as_kwargs(),
                             reply_markup=build_main_menu_kb())
        await message.answer(
            constants.GOOD_JOB_MSG,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
    else:
        await message.answer(
            QUESTIONS[step].text,
            reply_markup=build_answers_kb(step).as_markup(resize_keyboard=True)
        )


@router.message(F.text == Button.EXIT)
async def exit_game(message: types.Message,
                    state: FSMContext):
    """Exits the quiz"""
    data = await state.get_data()
    answers = data.get('answers', {})

    content = make_summary(answers)
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
    step -= 1
    await state.update_data(step=step)
    await message.answer(
        QUESTIONS[step].text,
        reply_markup=build_answers_kb(step).as_markup(resize_keyboard=True)
    )
