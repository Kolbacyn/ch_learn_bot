from aiogram.fsm.state import State, StatesGroup


class QuizStates(StatesGroup):
    question = State()
    answer = State()
