import asyncio

from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from keyboards import build_language_kb, build_main_menu_kb
from utilities.constants import CommonMessage, Numeric, Picture
from utilities.utils import (add_user_to_database, check_user_in_database,
                             get_user_language, get_user_level)

router = Router(name=__name__)


@router.message(Command('start'))
async def cmd_start(message: types.Message) -> None:
    """Processing start command"""
    await message.delete()
    user_id = message.from_user.id
    current_user = check_user_in_database(user_id)
    picture = types.FSInputFile(Picture.GREETING)
    match current_user:
        case False:
            await message.answer_photo(picture)
            await message.answer(
                f'{CommonMessage.NIHAO} {message.from_user.full_name}!'
                )
            await asyncio.sleep(Numeric.ONE)
            await message.answer(
                CommonMessage.GREETING_NEW
                )
            await asyncio.sleep(Numeric.ONE)
            add_user_to_database(user_id)
            await message.answer(
                CommonMessage.CHOOSE_LANGUAGE,
                reply_markup=build_language_kb())
            await asyncio.sleep(Numeric.ONE)
        case True:
            await message.answer(
                CommonMessage.GREETING_OLD,
                reply_markup=build_main_menu_kb()
            )


@router.message(Command('help'))
async def cmd_help(message: types.Message) -> None:
    """Processing help command"""
    await message.delete()
    await message.answer(
        CommonMessage.HELP
        )
    await message.answer(
        CommonMessage.INSTRUCTIONS
        )


@router.message(Command('cancel'))
async def cmd_cancel(message: types.Message,
                     state: FSMContext) -> None:
    """Processing cancel command"""
    await message.delete()
    await message.answer(CommonMessage.CANCEL)
    await state.clear()
    await message.answer(
        CommonMessage.STARTOVER,
        reply_markup=build_main_menu_kb()
        )


@router.message(Command('profile'))
async def cmd_profile(message: types.Message) -> None:
    """Processing profile command"""
    await message.delete()
    user_id = message.from_user.id
    level = get_user_level(user_id)
    language = get_user_language(user_id)

    await message.answer(
        f'Ваш ID: {user_id}\n'
        f'Язык: {language}\n'
        f'Уровень: {level}\n'
        )
