from typing import Any

from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, ScenesManager, on
from aiogram.types import KeyboardButton, Message, ReplyKeyboardRemove
from aiogram.utils.formatting import (
    Bold,
    as_key_value,
    as_list,
    as_numbered_list,
    as_section,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import constants
from utils import generate_question

quantity = 10
# # Fake data, in real application you should use a database or something else
QUESTIONS = [generate_question() for i in range(quantity)]


class QuizScene(Scene, state='quiz'):
    '''
    '''

    @on.message.enter()
    async def on_enter(self,
                       message: Message,
                       state: FSMContext,
                       step: int = 0) -> Any:
        '''
        '''
        if not step:
            # This is the first step, so we should greet the user
            await message.answer(constants.WELCOME_TO_QUIZ_MSG)

        try:
            quiz = QUESTIONS[step]
        except IndexError:
            # This error means that the question's list is over
            return await self.wizard.exit()

        markup = ReplyKeyboardBuilder()
        markup.add(*[KeyboardButton(text=answer.text) for answer in quiz.answers])

        if step > 0:
            markup.button(text=constants.CANCEL_QUIZ_BTN)
        markup.button(text=constants.EXIT_QUIZ_BTN)

        await state.update_data(step=step)
        return await message.answer(
            text=QUESTIONS[step].text,
            reply_markup=markup.adjust(2).as_markup(resize_keyboard=True),
        )

    @on.message.exit()
    async def on_exit(self,
                      message: Message,
                      state: FSMContext) -> None:
        '''
        '''
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

    @on.message(F.text == constants.CANCEL_QUIZ_BTN)
    async def back(self,
                   message: Message,
                   state: FSMContext) -> None:
        '''
        '''
        data = await state.get_data()
        step = data['step']

        previous_step = step - 1
        if previous_step < 0:
            # In case when the user tries to go back from the first question,
            # we just exit the quiz
            return await self.wizard.exit()
        return await self.wizard.back(step=previous_step)

    @on.message(F.text == constants.EXIT_QUIZ_BTN)
    async def exit(self, message: Message) -> None:
        '''
        '''
        await self.wizard.exit()

    @on.message(F.text)
    async def answer(self,
                     message: Message,
                     state: FSMContext) -> None:
        '''
        '''
        data = await state.get_data()
        step = data['step']
        answers = data.get('answers', {})
        answers[step] = message.text
        await state.update_data(answers=answers)

        await self.wizard.retake(step=step + 1)

    @on.message()
    async def unknown_message(self,
                              message: Message) -> None:
        '''
        '''
        await message.answer(constants.CHOOSE_ANSWER_MSG)


quiz_router = Router(name=__name__)
# Add handler that initializes the scene
quiz_router.message.register(QuizScene.as_handler(), Command('quiz'))


@quiz_router.message(Command('start'))
async def command_start(message: Message, scenes: ScenesManager):
    await scenes.close()
    await message.answer(
        'Hi! This is a quiz bot. To start the quiz, use the /quiz command.',
        reply_markup=ReplyKeyboardRemove(),
    )
