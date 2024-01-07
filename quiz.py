from dataclasses import dataclass, field
from random import random
from typing import Any

from aiogram import F, html, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import KeyboardButton, Message, ReplyKeyboardRemove
from aiogram.utils.formatting import (
    Bold,
    as_list,
    as_key_value,
    as_numbered_list,
    as_section
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from scrapy_hsk.models import Word


@dataclass
class Answer:
    """"""
    text: str
    is_correct: bool = False


@dataclass
class Question:
    """"""
    text: str
    answers: list[Answer]
    correct_answer: str = field(init=False)

    def __post_init__(self):
        self.correct_answer = next(answer.text for answer in self.answers
                                   if answer.is_correct)

    def generate_question():
        pass


QUESTIONS = [
    Question(
        text="What is the capital of France?",
        answers=[
            Answer("Paris", is_correct=True),
            Answer("London"),
            Answer("Berlin"),
            Answer("Madrid"),
        ],
    ),
    Question(
        text="What is the capital of Spain?",
        answers=[
            Answer("Paris"),
            Answer("London"),
            Answer("Berlin"),
            Answer("Madrid", is_correct=True),
        ],
    ),
    Question(
        text="What is the capital of Germany?",
        answers=[
            Answer("Paris"),
            Answer("London"),
            Answer("Berlin", is_correct=True),
            Answer("Madrid"),
        ],
    ),
    Question(
        text="What is the capital of England?",
        answers=[
            Answer("Paris"),
            Answer("London", is_correct=True),
            Answer("Berlin"),
            Answer("Madrid"),
        ],
    ),
    Question(
        text="What is the capital of Italy?",
        answers=[
            Answer("Paris"),
            Answer("London"),
            Answer("Berlin"),
            Answer("Rome", is_correct=True),
        ],
    ),
]


class QuizScene(Scene, state='quiz'):
    """"""
    @on.message.enter()
    async def on_enter(self,
                       message: Message,
                       state: FSMContext,
                       step: int or None = 0) -> Any:
        """"""
        if not step:
            await message.answer('Добро пожаловать в игру')
        try:
            quiz = QUESTIONS[step]
        except IndexError:
            return await self.wizard.exit()

        markup = ReplyKeyboardBuilder()
        markup.add(*[KeyboardButton(text=answer.text)
                     for answer in quiz.answers])

        if step > 0:
            markup.button(text="🔙 Back")
        markup.button(text="🚫 Exit")

        await state.update_data(step=step)
        return await message.answer(
            text=QUESTIONS[step].text,
            reply_markup=markup.adjust(2).as_markup(resize_keyboard=True)
        )

    @on.message.exit()
    async def on_exit(self,
                      message: Message,
                      state: FSMContext) -> None:
        """"""
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
                answer = 'No answer'
            user_answers.append(f'{quiz.text} ({icon} {html.quote(answer)})')

        content = as_list(
            as_section(
                Bold('YOUR ANSWERS:'),
                as_numbered_list(*user_answers)
            ),
            '',
            as_section(
                Bold('SUMMARY:'),
                as_list(
                    as_key_value('Correct', correct),
                    as_key_value('Incorrect', incorrect)
                )
            )
        )

        await message.answer(**content.as_kwargs(),
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state({})

    @on.message(F.text == '🔙 Back')
    async def back(self, message: Message, state: FSMContext) -> None:
        """"""
        data = await state.get_data()
        step = data['step']

        previous_step = step - 1
        if previous_step < 0:
            return await self.wizard.exit()
        return await self.wizard.back(step=previous_step)

    @on.message(F.text == '🚫 Exit')
    async def exit(self, message: Message) -> None:
        """"""
        await self.wizard.exit()

    @on.message(F.text)
    async def answer(self, message: Message, state: FSMContext) -> None:
        """"""
        data = await state.get_data()
        step = data['step']
        answers = data.get('answers', {})
        answers[step] = message.text
        await state.update_data(answers=answers)
        await self.wizard.retake(step=step + 1)

    @on.message()
    async def unknown_message(self, message: Message) -> None:
        """"""
        await message.answer('Please select an answer.')
