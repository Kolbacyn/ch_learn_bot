from aiogram import types, F, Router

from keyboards import build_main_menu_kb
import utilities.constants as constants


router = Router(name=__name__)


@router.callback_query(F.data.startswith('hsk_buttons_'))
async def hsk_level(callback: types.CallbackQuery):
    await callback.message.answer(
        constants.START_TRAINING_MESSAGE,
        reply_markup=build_main_menu_kb()
    )
    await callback.answer()
