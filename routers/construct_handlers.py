from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utilities.utils import generate_sep_sentence

router = Router(name=__name__)


def build_sentence_kb(words: list):
    """Adds buttons to the keyboard"""
    inline_keyboard = []
    words_buttons = []
    for word in words:
        words_buttons.append(InlineKeyboardButton(
            callback_data=word, text=word))
    inline_keyboard.append(words_buttons)
    inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data='back'),
        InlineKeyboardButton(text='Выйти', callback_data='leave')
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


@router.callback_query(F.data == 'main_menu_btn_3')
async def main_menu_btn_3(callback: types.CallbackQuery,
                          state: FSMContext,
                          step: int = 0):
    """Starts the construct interaction"""
    await state.clear()
    sentence = generate_sep_sentence()
    values = list(sentence.values())
    print(values)
    await state.update_data(step=step)
    await callback.message.answer(
        'Предложение: ',
        reply_markup=build_sentence_kb(values[0])
    )
    await callback.answer()


# @router.callback_query(F.data.in_(parts))
# async def process_answer_button(callback: types.CallbackQuery,
#                                 state: FSMContext):
#     """Processes the answer"""
#     data = await state.get_data()
#     step = data.get('step') + 1
#     await state.update_data(step=step)
#     await callback.message.answer(
#         text=f'Sentence: {callback.data}',
#         reply_markup=build_sentence_kb(parts)
#     )
#     await callback.answer()
