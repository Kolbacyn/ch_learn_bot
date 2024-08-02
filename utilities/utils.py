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
    translation = word.rus_translation
    flashcard = FlashCard(
        front_side=hanzi,
        back_side=translation,
    )
    return flashcard


def create_image(text):
    width, height = 800, 400
    image = Image.new('RGB', (width, height), 'white')

    # Создаем объект для рисования
    draw = ImageDraw.Draw(image)

    # Определяем шрифт и размер текста
    font_size = 40
    font = ImageFont.load_default()  # Можно использовать свой шрифт

    # Получаем размеры текста
    text_width, text_height = draw.text(text=text, font=font)

    # Вычисляем позицию текста (по центру)
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # Рисуем текст на изображении
    draw.text((x, y), text, fill='black', font=font)

    # Сохраняем изображение в байтовый поток
    byte_io = io.BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)  # Возвращаемся к началу потока

    return byte_io


class AttemptsQuantity(Enum):
    ten = '10'
    twenty = '20'
    fifty = '50'
    hundred = '100'


class AttemptsCallback(CallbackData, prefix='attempts'):
    quantity: AttemptsQuantity
