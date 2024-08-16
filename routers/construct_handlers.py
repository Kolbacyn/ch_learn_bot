from aiogram import F, Router, types

router = Router(name=__name__)


@router.callback_query(F.data == 'main_menu_btn_3')
async def main_menu_btn_3(callback: types.CallbackQuery):
    await callback.message.answer(
        'В разработке...'
    )
    await callback.answer()
