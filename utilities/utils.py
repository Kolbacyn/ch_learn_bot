import logging
from enum import Enum
from random import choice, sample, shuffle

from aiogram.filters.callback_data import CallbackData
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scrapy_hsk.models import Base, Sentence, User, Word
from utilities.constants import Database, Picture
from utilities.dataclass import Answer, FlashCard, Question

engine = create_engine(Database.SQLITE, echo=False)
Base.metadata.create_all(engine)
session = Session(engine)


def get_word_from_database(level: int) -> Word:
    """Get word from database"""
    return choice(session.query(Word).filter_by(level=level).all())


def get_sentence_from_database() -> Sentence:
    """Get sentence from database"""
    sent_engine = create_engine(Database.SQLITE, echo=False)
    Base.metadata.create_all(sent_engine)
    sent_session = Session(sent_engine)
    return choice(sent_session.query(Sentence).all())


def generate_sep_sentence() -> dict:
    """Generate separated sentence"""
    sentence = get_sentence_from_database()
    parts = list(sentence.sentence.split(' '))
    shuffle(parts)
    sentence_for_construct = {}
    sentence_for_construct[sentence.sentence] = parts
    sentence_for_construct['correct_answer'] = sentence.sentence
    print(sentence_for_construct)
    return sentence_for_construct


def generate_question(level) -> Question:
    """
    Generate a question with a random word from the database and three options.

    Returns:
        Question: A question object with a prompt and four answer options.
    """
    words = [get_word_from_database(level) for _ in range(4)]
    prompt = f'Переведите на русский язык: {words[0].word}'
    correct_answer = Answer(words[0].rus_translation, is_correct=True)
    incorrect_answers = [
        Answer(word.rus_translation) for word in words[1:]
    ]
    answer_options = sample(incorrect_answers + [correct_answer], k=4)
    return Question(text=prompt, answers=answer_options)


def generate_questions(quantity, level) -> list[Question]:
    """Generate questions"""
    questions = []
    for _ in range(quantity):
        questions.append(generate_question(level))
    return questions


def generate_flashcard(level) -> FlashCard:
    """Generate flashcard"""
    word = get_word_from_database(level)
    return FlashCard(
        front_side=word.word,
        back_side=word.rus_translation,
        hint=word.transcription
    )


def generate_flashcards(quantity, level) -> list[FlashCard]:
    """Generate flashcards"""
    flashcards = []
    for _ in range(quantity):
        flashcards.append(generate_flashcard(level))
    return flashcards


def create_image(text) -> None:
    """Create image"""
    width, height = 300, 300
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Deng.ttf', size=62)
    draw.text((150, 150), anchor='mm', text=text, fill='black', font=font)
    image.save(Picture.FLASHCARD, 'PNG')


def check_user_in_database(user_id) -> bool:
    """Check user in database"""
    existing_user = session.query(User).filter_by(user_id=user_id).first()
    if existing_user:
        return True
    return False


def add_user_to_database(user_id) -> None:
    """Add user to database"""
    existing_user = check_user_in_database(user_id)
    if existing_user:
        return
    session.add(User(user_id=user_id))
    session.commit()


def update_user(user_id, new_language=None, new_level=None):
    """Update user data"""
    user = session.query(User).filter_by(user_id=user_id).first()

    if user:
        if new_language is not None:
            user.language = new_language
        if new_level is not None:
            user.level = new_level
        session.commit()
        logging.info(f"Данные пользователя {user_id} обновлены.")
    else:
        logging.error(f"Пользователь с ID {user_id} не найден в базе данных.")


def get_user_level(user_id) -> int:
    """Get user level"""
    user = session.query(User).filter_by(user_id=user_id).first()
    return user.level


def get_user_language(user_id) -> str:
    """Get user language"""
    user = session.query(User).filter_by(user_id=user_id).first()
    return user.language


class AttemptsQuantity(Enum):
    """Attempts quantity"""
    ten = '10'
    twenty = '20'
    fifty = '50'
    hundred = '100'


class AttemptsCallback(CallbackData, prefix='attempts'):
    """Attempts callback"""
    quantity: AttemptsQuantity
