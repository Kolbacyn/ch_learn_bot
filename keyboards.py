from aiogram.types import (InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)
from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton, ReplyKeyboardBuilder)

from utilities.constants import Button, ButtonData, Numeric
from utilities.utils import AttemptsCallback, AttemptsQuantity


def build_main_menu_kb() -> InlineKeyboardMarkup:
    """Builds the main menu keyboard"""
    inline_keyboard = []
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text='Квиз',
                callback_data='main_menu_btn_1'
            ),
            InlineKeyboardButton(
                text='Карточки',
                callback_data='main_menu_btn_2'
            ),
            InlineKeyboardButton(
                text='Конструктор',
                callback_data='main_menu_btn_3'
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_hsk_kb() -> InlineKeyboardMarkup:
    """Builds the HSK keyboard"""
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


# attempts_quantity_buttons = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(
#             text='10 попыток',
#             callback_data=AttemptsCallback(
#                 quantity=AttemptsQuantity.ten
#             ).pack()
#         ),
#          KeyboardButton(
#             text='20 попыток',
#             callback_data=AttemptsCallback(
#                 quantity=AttemptsQuantity.twenty
#             ).pack()
#         ),
#          KeyboardButton(
#             text='50 попыток',
#             callback_data=AttemptsCallback(
#                 quantity=AttemptsQuantity.fifty
#             ).pack()
#         ),
#          KeyboardButton(
#             text='100 попыток',
#             callback_data=AttemptsCallback(
#                 quantity=AttemptsQuantity.hundred
#             ).pack()
#         )],
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=True
# )


def build_language_kb() -> InlineKeyboardMarkup:
    """Builds the language keyboard"""
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


def build_answers_kb(step: int, questions: list):
    """Creates the answers keyboard"""
    kb = ReplyKeyboardBuilder()
    answers = questions[step].answers
    kb.add(*[KeyboardButton(text=answer.text) for answer in answers])
    if step > Numeric.ZERO:
        kb.button(text=Button.CANCEL)
    kb.button(text=Button.EXIT)
    kb.adjust(Numeric.ADJUSTMENT)
    return kb


def build_flashcards_kb(step, flashcards):
    """Adds buttons to the keyboard"""
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton(
        text=flashcards[step].front_side,
        callback_data=ButtonData.FLASHCARD_FRONT_SIDE)])
    inline_keyboard.append([
        InlineKeyboardButton(
            text=Button.CORRECT,
            callback_data=ButtonData.FLASHCARD_CORRECT_ANSWER
            ),
        InlineKeyboardButton(
            text=Button.WRONG,
            callback_data=ButtonData.FLASHCARD_WRONG_ANSWER
            )])
    inline_keyboard.append([InlineKeyboardButton(
        text=Button.EXIT,
        callback_data=ButtonData.FLASHCARD_LEAVE)])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_sentence_kb(words: list, step: int):
    """Adds buttons to the keyboard"""
    inline_keyboard = []
    words_buttons = []
    for word in words:
        words_buttons.append(InlineKeyboardButton(
            callback_data=f'part_{word}',
            text=word))
    inline_keyboard.append(words_buttons)
    service_buttons = [
        InlineKeyboardButton(
            text=Button.CANCEL,
            callback_data=ButtonData.CONSTRUCT_BACK
            ),
        InlineKeyboardButton(
            text=Button.EXIT,
            callback_data=ButtonData.CONSTRUCT_LEAVE
            )
    ]
    if step > Numeric.ZERO:
        inline_keyboard.append(service_buttons)
    else:
        inline_keyboard.append([service_buttons[-1]])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_final_kb():
    """Adds buttons to the keyboard at the final stage"""
    inline_keyboard = []
    inline_keyboard.append([
        InlineKeyboardButton(
            text=Button.CANCEL,
            callback_data=ButtonData.CONSTRUCT_BACK
            ),
        InlineKeyboardButton(
            text=Button.ACCEPT,
            callback_data=ButtonData.CONSTRUCT_CORRECT
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_result_kb():
    """Adds buttons to the keyboard at the final stage"""
    inline_keyboard = []
    inline_keyboard.append([
        InlineKeyboardButton(
            text=Button.EXIT,
            callback_data=ButtonData.CONSTRUCT_LEAVE
            ),
        InlineKeyboardButton(
            text=Button.REPEAT,
            callback_data=ButtonData.CONSTRUCT_AGAIN
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
