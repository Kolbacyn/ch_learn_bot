from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

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


def build_final_kb():
    """Adds buttons to the keyboard at the final stage"""
    inline_keyboard = []
    inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data='back'),
        InlineKeyboardButton(text='Подтвердить', callback_data='correct')
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


@router.callback_query(F.data == 'main_menu_btn_3')
async def main_menu_btn_3(callback: types.CallbackQuery,
                          state: FSMContext,
                          step: int = 0):
    """Starts the construct interaction"""
    await state.clear()
    sentence = generate_sep_sentence()
    correct_answer = sentence['correct_answer']
    values = list(sentence.values())
    await state.update_data(step=step)
    await state.update_data(correct_answer=correct_answer)
    await callback.message.answer(
        'Предложение: ',
        reply_markup=build_sentence_kb(values[0])
    )
    await state.update_data(parts=values[0])
    await callback.answer()


@router.callback_query(F.data != 'back',
                       F.data != 'leave')
async def process_answer_button(callback: types.CallbackQuery,
                                state: FSMContext):
    """Processes the answer"""
    data = await state.get_data()
    step = data['step']
    answers = data.get('answers', [])
    parts = data.get('parts', [])
    parts.remove(callback.data)
    answers.append(callback.data)
    
    await state.update_data(step=step + 1)
    if len(parts) == 0:
        await callback.message.answer(
            text=f'Ваше предложение: {"".join(answers)}',
            reply_markup=build_final_kb()
        )
    else:
        await callback.message.answer(
            text=f'{"".join(answers)}',
            reply_markup=build_sentence_kb(parts)
        )
        await state.update_data(answers=answers)
        await state.update_data(parts=parts)
    await callback.answer()


@router.callback_query(F.data == 'correct')
async def correct_answer(callback: types.CallbackQuery,
                         state: FSMContext):
    """Confirms the correct answer"""
    data = await state.get_data()
    correct_answer = data.get('correct_answer')
    answers = data.get('answers', [])
    user_answer = ' '.join(answers)
    if correct_answer == user_answer:
        await callback.message.answer(
            text='Верно!',
            reply_markup=build_final_kb()
        )
    else:
        await callback.message.answer(
            text=f'Неверно!\nПравильное предложение: {correct_answer}',
            reply_markup=build_final_kb()
        )


@router.message(F.text == 'leave')
async def exit_game(message: types.Message):
    """Exits the quiz"""
    await message.answer(
        'good job',
        reply_markup=ReplyKeyboardRemove()
        )
