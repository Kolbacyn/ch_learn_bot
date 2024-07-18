from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup, KeyboardButton)


main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Карточки',
            callback_data='main_menu_btn_1'
        ),
        InlineKeyboardButton(
            text='Квиз',
            callback_data='main_menu_btn_2'
        )
    ]
])

hsk_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='HSK1',
            callback_data='hsk_buttons_1'
        )
    ],
    [
        InlineKeyboardButton(
            text='HSK2',
            callback_data='hsk_buttons_2'
        )
    ],
    [
        InlineKeyboardButton(
            text='HSK3',
            callback_data='hsk_buttons_3'
        )
    ],
    [
        InlineKeyboardButton(
            text='HSK4',
            callback_data='hsk_buttons_4'
        )
    ],
    [
        InlineKeyboardButton(
            text='HSK5',
            callback_data='hsk_buttons_5'
        )
    ],
    [
        InlineKeyboardButton(
            text='HSK6',
            callback_data='hsk_buttons_6'
        )
    ]
])


attempts_quantity_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(
            text='10 попыток',
            callback_data='attempts_quantity_1'
        ),
         KeyboardButton(
            text='20 попыток',
            callback_data='attempts_quantity_2'
        ),
         KeyboardButton(
            text='50 попыток',
            callback_data='attempts_quantity_3'
        ),
         KeyboardButton(
            text='100 попыток',
            callback_data='attempts_quantity_4'
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