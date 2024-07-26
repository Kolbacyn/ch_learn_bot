from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import AttemptsCallback, AttemptsQuantity


def build_main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Карточки',
        callback_data='main_menu_btn_1'
    )
    builder.button(
        text='Квиз',
        callback_data='main_menu_btn_2'
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
    attempts_kb = ReplyKeyboardMarkup(
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
    )
    return attempts_kb


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

# exit_to_menu_button = InlineKeyboardMarkup(inline_keyboard=[
#     InlineKeyboardButton(
#         text='В меню',
#         callback_data='exit_to_menu'
#     )
# ])


# def get_hsk_levels_keybord():
#     keyboar_builder = InlineKeyboardBuilder()
#     keyboar_builder.button(text='HSK1', callback_data='hsk_buttons_1')
#     keyboar_builder.button(text='HSK2', callback_data='hsk_buttons_2')
#     keyboar_builder.button(text='HSK3', callback_data='hsk_buttons_3')
#     return keyboar_builder.as_markup()