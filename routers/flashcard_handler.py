import logging

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext


router = Router(name=__name__)


@router.callback_query(F.data == 'main_menu_btn_2')
async def enter_flashcards(callback: types.CallbackQuery,
                           state: FSMContext,
                           step: int = 0):
    await state.clear()
    await callback.message.answer('Добро пожаловать!')
