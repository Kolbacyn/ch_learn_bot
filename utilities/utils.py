from enum import Enum
from random import choice, sample

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
    """Get word from database"""
    return choice(session.query(Word).all())


def generate_question():
    """
    Generate a question with a random word from the database and three options.

    Returns:
        Question: A question object with a prompt and four answer options.
    """
    words = [get_word_from_database() for _ in range(4)]
    prompt = f'Переведите на русский язык: {words[0].word}'
    correct_answer = Answer(words[0].rus_translation, is_correct=True)
    incorrect_answers = [
        Answer(word.rus_translation) for word in words[1:]
    ]
    answer_options = sample(incorrect_answers + [correct_answer], k=4)
    return Question(text=prompt, answers=answer_options)


def generate_flashcard():
    """Generate flashcard"""
    word = get_word_from_database()
    return FlashCard(
        front_side=word.word,
        back_side=word.rus_translation,
        hint=word.transcription
    )


def create_image(text):
    """Create image"""
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
