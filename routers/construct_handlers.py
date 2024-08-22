from random import shuffle
from aiogram import F, Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utilities.utils import get_sentence_from_database

router = Router(name=__name__)


def build_sentence_kb():
    """Adds buttons to the keyboard"""
    inline_keyboard = []
    sentence = get_sentence_from_database().sentence
    parts = list(sentence.split(' '))
    parts_buttons = []
    for part in parts:
        parts_buttons.append(InlineKeyboardButton(
            callback_data=part, text=part))
    shuffle(parts_buttons)
    inline_keyboard.append(parts_buttons)
    inline_keyboard.append([InlineKeyboardButton(
        text='Выйти', callback_data='leave')])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


@router.callback_query(F.data == 'main_menu_btn_3')
async def main_menu_btn_3(callback: types.CallbackQuery):
    await callback.message.answer(
        'Sentence:',
        reply_markup=build_sentence_kb()
    )
    await callback.answer()
