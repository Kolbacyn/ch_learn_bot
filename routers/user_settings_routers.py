import logging

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from routers.command_handlers import users
from keyboards import build_main_menu_kb, build_language_kb
import utilities.constants as constants


router = Router(name=__name__)


@router.callback_query(F.data.startswith('hsk_buttons_'))
async def hsk_level(callback: types.CallbackQuery,
                    state: FSMContext):
    await state.clear()
    data = await state.get_data()
    if not users[callback.from_user.id]:
        await callback.message.answer(
            constants.CHOOSE_LANGUAGE_MSG,
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
    data = await state.get_data()
    logging.info(data)
    if not users[callback.from_user.id]:
        await callback.message.edit_text(
            constants.START_TRAINING_MESSAGE,
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
