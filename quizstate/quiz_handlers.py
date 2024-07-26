import logging

from aiogram import types, Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.formatting import (
    Bold,
    as_key_value,
    as_list,
    as_numbered_list,
    as_section,
)

import constants
from quizstate.states import QuizState
from utils import generate_question


router = Router(name='quizstate')


quantity = 10
# # Fake data, in real application you should use a database or something else
QUESTIONS = [generate_question() for i in range(quantity)]


@router.callback_query(F.data == 'main_menu_btn_2')
async def send_question(callback: types.CallbackQuery,                    
                        state: FSMContext,
                        step: int = 0):
    if not step:
        # This is the first step, so we should greet the user
        await callback.message.answer(constants.WELCOME_TO_QUIZ_MSG)
        step += 1
    try:
        quiz = QUESTIONS[step]
        logging.info(quiz)
    except IndexError:
        # This error means that the question's list is over
        return await callback.message.answer(
            text='sorry, but there are no more questions',
        )

    markup = ReplyKeyboardBuilder()
    markup.add(*[KeyboardButton(text=answer.text) for answer in quiz.answers])

    if step > 0:
        markup.button(text=constants.CANCEL_QUIZ_BTN)
    markup.button(text=constants.EXIT_QUIZ_BTN)

    await state.update_data(step=step)
    return await callback.message.answer(
        text=QUESTIONS[step].text,
        reply_markup=markup.adjust(2).as_markup(resize_keyboard=True),
    )


@router.message(F.text == constants.CANCEL_QUIZ_BTN)
async def back(message: types.Message, state: FSMContext):
    data = await state.get_data()
    step = data['step']
    previous_step = step - 1
    if previous_step < 0:
        # In case when the user tries to go back from the first question,
        # we just exit the quiz
        return await state.finish()
    return await state.update_data(step=previous_step)


@router.message(F.text == constants.EXIT_QUIZ_BTN)
async def exit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answers = data.get('answers', {})
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
        user_answers.append(f"{quiz.text} ({icon} {html.quote(answer)})")

    content = as_list(
        as_section(
            Bold('Ваши ответы:'),
            as_numbered_list(*user_answers),
        ),
        '',
        as_section(
            Bold('Итог:'),
            as_list(
                as_key_value('Верно', correct),
                as_key_value('Неверно', incorrect),
            ),
        ),
    )

    await message.answer(
        **content.as_kwargs(),
        reply_markup=ReplyKeyboardRemove()
        )
    await state.set_data({})


@router.message()
async def handle_answer(message: types.Message,
                        state: FSMContext):
    '''
    '''
    data = await state.get_data()
    step = data['step']
    answers = data.get('answers', {})
    answers[step] = message.text
    await state.update_data(answers=answers)
    step = step + 1
