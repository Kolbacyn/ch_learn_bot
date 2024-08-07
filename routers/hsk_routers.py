import logging

from aiogram import types, F, Router

from routers.command_handlers import users
from keyboards import build_main_menu_kb
import utilities.constants as constants


router = Router(name=__name__)


@router.callback_query(F.data.startswith('hsk_buttons_'))
async def hsk_level(callback: types.CallbackQuery):
    if not users[callback.from_user.id]:
        await callback.message.answer(
            constants.START_TRAINING_MESSAGE,
            reply_markup=build_main_menu_kb()
        )
        users[callback.from_user.id]['hsk_level'] = callback.data[-1]
    logging.info(users)
    await callback.answer()
