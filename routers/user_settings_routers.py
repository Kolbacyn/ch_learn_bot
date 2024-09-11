from aiogram import F, Router, types

from keyboards import build_hsk_kb, build_main_menu_kb
from utilities.constants import CommonMessage, Numeric
from utilities.utils import update_user

router = Router(name=__name__)


@router.callback_query(F.data.startswith('hsk_buttons_'))
async def hsk_level(callback: types.CallbackQuery) -> None:
    """Checks the HSK level"""
    user_id = callback.from_user.id
    level = callback.data[Numeric.LAST_ELEMENT]
    update_user(user_id, new_level=level)
    await callback.message.edit_text(
            CommonMessage.HSK_CHOSEN,
            reply_markup=build_main_menu_kb()
        )
    await callback.answer()


@router.callback_query(F.data.startswith('language_'))
async def language(callback: types.CallbackQuery) -> None:
    """Checks the language"""
    user_id = callback.from_user.id
    language = callback.data[Numeric.LANGUAGE:]
    update_user(user_id, new_language=language)
    await callback.message.edit_text(
            CommonMessage.LANGUAGE_CHOSEN,
            reply_markup=build_hsk_kb()
        )
    await callback.answer()
