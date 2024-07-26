from aiogram.fsm.state import State, StatesGroup


class QuizState(StatesGroup):
    question = State()
    answer = State()
