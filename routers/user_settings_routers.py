from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from keyboards import build_language_kb, build_main_menu_kb
from utilities.constants import CommonMessage, Numeric
from utilities.utils import update_user

router = Router(name=__name__)


@router.callback_query(F.data.startswith('hsk_buttons_'))
async def hsk_level(callback: types.CallbackQuery,
                    state: FSMContext) -> None:
    """Checks the HSK level"""
    await state.clear()
    user_id = callback.from_user.id
    level = callback.data[Numeric.LAST_ELEMENT]
    update_user(user_id, new_level=level)
    await callback.message.answer(
            CommonMessage.CHOOSE_LANGUAGE,
            reply_markup=build_language_kb()
        )
    await callback.answer()


@router.callback_query(F.data.startswith('language_'))
async def language(callback: types.CallbackQuery,
                   state: FSMContext) -> None:
    """Checks the language"""
    user_id = callback.from_user.id
    language = callback.data[-2:]
    update_user(user_id, new_language=language)
    await callback.message.edit_text(
            CommonMessage.STARTING,
            reply_markup=build_main_menu_kb()
        )
    await callback.answer()
