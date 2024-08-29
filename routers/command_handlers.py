import asyncio
import logging

from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from keyboards import build_hsk_kb, build_main_menu_kb
from utilities.constants import CommonMessage, Numeric, Picture

router = Router(name=__name__)

users: dict[int, dict[str, list]] = {}


@router.message(Command('start'))
async def cmd_start(message: types.Message) -> None:
    """Processing start command"""
    await message.delete()
    picture = types.FSInputFile(Picture.GREETING)
    if not users.get(message.from_user.id):
        users[message.from_user.id] = {}
    await message.answer_photo(picture)
    await message.answer(
        f'{CommonMessage.NIHAO} {message.from_user.full_name}!'
        )
    await asyncio.sleep(Numeric.ONE)
    await message.answer(
        CommonMessage.GREETING
        )
    await asyncio.sleep(Numeric.ONE)
    if not users[message.from_user.id].get('hsk_level'):
        logging.info(users)
        await message.answer(CommonMessage.INTRODUCING)
        await asyncio.sleep(Numeric.ONE)
        await message.answer(
            CommonMessage.CHOOSE_HSK_LEVEL,
            reply_markup=build_hsk_kb()
            )
    else:
        await message.answer(
            CommonMessage.STARTING,
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
        reply_markup=build_hsk_kb()
        )
