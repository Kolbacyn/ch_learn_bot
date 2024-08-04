import io
from random import choice, sample
from enum import Enum

from aiogram.filters.callback_data import CallbackData
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scrapy_hsk.models import Base, Word
from utilities.dataclass import Answer, FlashCard, Question


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
        answers=sample([Answer(translation, is_correct=True),
                        Answer(ans_one.rus_translation),
                        Answer(ans_two.rus_translation),
                        Answer(ans_three.rus_translation)],
                       k=4),
    )
    return question


def generate_flashcard():
    word = get_word_from_database()
    hanzi = word.word
    transcription = word.transcription
    translation = word.rus_translation
    flashcard = FlashCard(
        front_side=hanzi,
        back_side=translation,
        hint=transcription
    )
    return flashcard


def create_image(text):
    width, height = 300, 300
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Deng.ttf', size=62)
    draw.text((150, 150), anchor='mm', text=text, fill='black', font=font)
    image.save('biffer.png', 'PNG')


class AttemptsQuantity(Enum):
    ten = '10'
    twenty = '20'
    fifty = '50'
    hundred = '100'


class AttemptsCallback(CallbackData, prefix='attempts'):
    quantity: AttemptsQuantity
