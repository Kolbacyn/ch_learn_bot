from random import choice

from aiogram.filters.callback_data import CallbackData
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scrapy_hsk.models import Base, Word
from dataclass import Answer, Question


engine = create_engine('sqlite:///sqlite.db', echo=False)
Base.metadata.create_all(engine)
session = Session(engine)


def get_word_from_database():
    word = choice(session.query(Word).all())
    return word


def generate_question():
    words = [get_word_from_database() for i in range(4)]
    hanzi = words[0].word
    text = f'Переведите на русский язык: {hanzi}'
    translation = words[0].rus_translation
    ans_one = words[1]
    ans_two = words[2]
    ans_three = words[3]
    question = Question(
        text=text,
        answers=[
            Answer(translation, is_correct=True),
            Answer(ans_one.rus_translation),
            Answer(ans_two.rus_translation),
            Answer(ans_three.rus_translation)
        ],
    )
    return question


class AttemptsCallback(CallbackData, prefix='attempts'):
    quantity: int
