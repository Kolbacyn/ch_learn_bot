import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

import utilities.constants as constants
from utilities.constants import CommonMessage
from keyboards import build_language_kb, build_main_menu_kb
from routers.command_handlers import users

router = Router(name=__name__)


@router.callback_query(F.data.startswith('hsk_buttons_'))
async def hsk_level(callback: types.CallbackQuery,
                    state: FSMContext):
    """Checks the HSK level"""
    await state.clear()
    data = await state.get_data()
    if not users[callback.from_user.id]:
        await callback.message.answer(
            CommonMessage.CHOOSE_LANGUAGE,
            reply_markup=build_language_kb()
        )
        data['hsk_level'] = callback.data[-1]
    logging.info(users)
    logging.info(data)
    await state.update_data(data)
    await callback.answer()


@router.callback_query(F.data.startswith('language_'))
async def language(callback: types.CallbackQuery,
                   state: FSMContext):
    """Checks the language"""
    data = await state.get_data()
    logging.info(data)
    if not users[callback.from_user.id]:
        await callback.message.edit_text(
            CommonMessage.STARTING,
            reply_markup=build_main_menu_kb()
        )
        data['language'] = callback.data[-2:]
    await state.update_data(data)
    logging.info(users)
    logging.info(data)
    data = await state.get_data()
    users[callback.from_user.id]['language'] = data['language']
    users[callback.from_user.id]['hsk_level'] = data['hsk_level']
    await callback.answer()
