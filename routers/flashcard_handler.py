import logging

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from utilities import constants
from utilities.utils import generate_flashcard


router = Router(name=__name__)


@router.callback_query(F.data == 'main_menu_btn_2')
async def enter_flashcards(callback: types.CallbackQuery,
                           state: FSMContext,
                           step: int = 0):
    await state.clear()
    if not step:
        await callback.message.answer(constants.WELCOME_MSG)
