from aiogram.types import (InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utilities.utils import AttemptsCallback, AttemptsQuantity


def build_main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Квиз',
        callback_data='main_menu_btn_1'
    )
    builder.button(
        text='Карточки',
        callback_data='main_menu_btn_2'
    )
    builder.button(
        text='Конструктор',
        callback_data='main_menu_btn_3'
    )
    return builder.as_markup()


def build_hsk_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='HSK1',
        callback_data='hsk_buttons_1'
    )
    builder.button(
        text='HSK2',
        callback_data='hsk_buttons_2'
    )
    builder.button(
        text='HSK3',
        callback_data='hsk_buttons_3'
    )
    builder.button(
        text='HSK4',
        callback_data='hsk_buttons_4'
    )
    builder.button(
        text='HSK5',
        callback_data='hsk_buttons_5'
    )
    builder.button(
        text='HSK6',
        callback_data='hsk_buttons_6'
    )
    builder.adjust(1)
    return builder.as_markup()


def build_attempts_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='10 попыток',
        callback_data=AttemptsCallback(
            quantity='10').pack()
            )
    builder.button(
        text='20 попыток',
        callback_data=AttemptsCallback(
            quantity='20').pack()
            )
    builder.button(
        text='50 попыток',
        callback_data=AttemptsCallback(
            quantity='50').pack()
            )
    builder.button(
        text='100 попыток',
        callback_data=AttemptsCallback(
            quantity='100').pack()
            )
    return builder.as_markup(
        one_time_keyboard=True
    )


def build_attempts_kb2() -> ReplyKeyboardMarkup:
    keyboard = [[
        KeyboardButton(
            text='10 попыток',
            callback_data=AttemptsCallback(
                quantity=AttemptsQuantity.ten.value
            ).pack()
        ),
        KeyboardButton(
            text='20 попыток',
            callback_data=AttemptsCallback(
                quantity=AttemptsQuantity.twenty.value
            ).pack()
        ),
        KeyboardButton(
            text='50 попыток',
            callback_data=AttemptsCallback(
                quantity=AttemptsQuantity.fifty.value
            ).pack()
        ),
        KeyboardButton(
            text='100 попыток',
            callback_data=AttemptsCallback(
                quantity=AttemptsQuantity.hundred.value
            ).pack()
        ),
    ]]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


attempts_quantity_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(
            text='10 попыток',
            callback_data=AttemptsCallback(
                quantity=AttemptsQuantity.ten
            ).pack()
        ),
         KeyboardButton(
            text='20 попыток',
            callback_data=AttemptsCallback(
                quantity=AttemptsQuantity.twenty
            ).pack()
        ),
         KeyboardButton(
            text='50 попыток',
            callback_data=AttemptsCallback(
                quantity=AttemptsQuantity.fifty
            ).pack()
        ),
         KeyboardButton(
            text='100 попыток',
            callback_data=AttemptsCallback(
                quantity=AttemptsQuantity.hundred
            ).pack()
        )],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


def build_language_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Русский',
        callback_data='language_ru'
    )
    builder.button(
        text='English',
        callback_data='language_en'
    )
    return builder.as_markup()
