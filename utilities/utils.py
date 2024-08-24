from enum import Enum
from random import choice, sample, shuffle

from aiogram.filters.callback_data import CallbackData
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scrapy_hsk.models import Base, Sentence, Word
from utilities.dataclass import Answer, FlashCard, Question

engine = create_engine('sqlite:///sqlite.db', echo=False)
Base.metadata.create_all(engine)
session = Session(engine)


def get_word_from_database():
    """Get word from database"""
    return choice(session.query(Word).all())


def get_sentence_from_database():
    """Get sentence from database"""
    sent_engine = create_engine('sqlite:///sqlite_sentences.db', echo=False)
    Base.metadata.create_all(sent_engine)
    sent_session = Session(sent_engine)
    return choice(sent_session.query(Sentence).all())


def generate_sep_sentence():
    """Generate separated sentence"""
    sentence = get_sentence_from_database()
    parts = list(sentence.sentence.split(' '))
    shuffle(parts)
    sentence_for_construct = {}
    sentence_for_construct[sentence.sentence] = parts
    print(sentence_for_construct)
    return sentence_for_construct


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
