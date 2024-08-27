import asyncio

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardRemove)

from keyboards import build_main_menu_kb
from utilities.constants import (Button, ButtonData, ConstructMessage,
                                 Numeric, Picture, Rules)
from utilities.utils import generate_sep_sentence

router = Router(name=__name__)


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


@router.callback_query(F.data.in_((ButtonData.TRAIN_CONSTRUCTOR,
                                   ButtonData.CONSTRUCT_AGAIN)))
async def main_menu_btn_3(callback: types.CallbackQuery,
                          state: FSMContext,
                          step: int = 0):
    """Starts the construct interaction"""
    await state.clear()
    if callback.data == ButtonData.TRAIN_CONSTRUCTOR:
        await callback.message.answer(
            Rules.CONSTRUCT_RULES
        )
        asyncio.sleep(Numeric.ONE)
    sentence = generate_sep_sentence()
    correct_answer = sentence['correct_answer']
    values = list(sentence.values())
    await state.update_data(step=step)
    await state.update_data(correct_answer=correct_answer)
    await callback.message.answer(
        ConstructMessage.INITIAL,
        reply_markup=build_sentence_kb(values[Numeric.ZERO], step)
    )
    await state.update_data(parts=values[Numeric.ZERO])
    await callback.answer()


@router.callback_query(F.data.startswith('part_'))
async def process_answer_button(callback: types.CallbackQuery,
                                state: FSMContext):
    """Processes the answer"""
    data = await state.get_data()
    step = data['step'] + Numeric.ONE
    answers = data.get('answers', [])
    parts = data.get('parts', [])
    answers.append(callback.data.lstrip('part_'))
    await state.update_data(step=step)
    await state.update_data(answers=answers)
    parts.remove(callback.data.lstrip('part_'))
    await state.update_data(parts=parts)
    if len(parts) > Numeric.ZERO:
        await callback.message.edit_text(
            text=f'{ConstructMessage.INTERIM_ANSWER}{" ".join(answers)}',
            reply_markup=build_sentence_kb(parts, step)
        )
    else:
        if len(parts) == Numeric.ZERO:
            await callback.message.edit_text(
                text=f'{ConstructMessage.FINAL_ANSWER}{" ".join(answers)}',
                reply_markup=build_final_kb()
            )
    await callback.answer()


@router.callback_query(F.data == ButtonData.CONSTRUCT_CORRECT)
async def correct_answer(callback: types.CallbackQuery,
                         state: FSMContext):
    """Confirms the correct answer"""
    data = await state.get_data()
    correct_answer = data.get('correct_answer')
    answers = data.get('answers', [])
    user_answer = ' '.join(answers)
    if correct_answer == user_answer:
        await callback.message.edit_text(
            text=ConstructMessage.CORRECT,
            reply_markup=build_result_kb()
        )
    else:
        await callback.message.edit_text(
            text=f'{ConstructMessage.INCORRECT}{correct_answer}',
            reply_markup=build_result_kb()
        )
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == ButtonData.CONSTRUCT_LEAVE)
async def exit_construct(callback: types.CallbackQuery):
    """Exits the construct game"""
    await callback.message.answer(
        ConstructMessage.RETURN_TO_MENU,
        reply_markup=ReplyKeyboardRemove()
        )
    await callback.answer()
    await asyncio.sleep(Numeric.ONE)
    await callback.message.answer_photo(
        photo=types.FSInputFile(Picture.GREETING),
        reply_markup=build_main_menu_kb()
        )
    await callback.answer()


@router.callback_query(F.data == ButtonData.CONSTRUCT_BACK)
async def step_back(callback: types.CallbackQuery,
                    state: FSMContext):
    """Returns to the previous step"""
    data = await state.get_data()
    step = data.get('step')
    step -= Numeric.ONE
    await state.update_data(step=step)
    answers = data.get('answers', [])
    parts = data.get('parts', [])
    returning_part = answers.pop(Numeric.LAST_ELEMENT)
    parts.append(returning_part)
    await state.update_data(answers=answers)
    await state.update_data(parts=parts)
    if step > Numeric.ZERO:
        await callback.message.edit_text(
            text=' '.join(answers),
            reply_markup=build_sentence_kb(parts, step)
            )
    else:
        await callback.message.edit_text(
            text=ConstructMessage.INITIAL,
            reply_markup=build_sentence_kb(parts, step)
            )
    await callback.answer()
