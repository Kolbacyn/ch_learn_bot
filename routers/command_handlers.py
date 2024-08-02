import asyncio

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from keyboards import build_hsk_kb
import utilities.constants as constants
from utilities.utils import create_image


router = Router(name=__name__)


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    picture = types.FSInputFile(constants.GREETING_PICTURE)
    await message.answer_photo(picture)
    await message.answer(
        f'你好 {message.from_user.full_name}!'
        )
    await asyncio.sleep(1)
    await message.answer(
        'Меня зовут Ханью и я твой помощник в изучении китайского языка'
        )
    await asyncio.sleep(1)
    await message.answer(
        'Выбери уровень подготовки',
        reply_markup=build_hsk_kb()
        )


@router.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(
        'Это бот-помощник в изучении китайского языка.'
        )
    await message.answer(
        'Для начала тренировки отправьте /start и выберите уровень подготовки.'
        )


@router.message(Command('cancel'))
async def cmd_cancel(message: types.Message,
                     state: FSMContext):
    await message.answer(constants.CANCEL_MESSAGE)
    await state.clear()
    await message.answer('Начнем сначала!', reply_markup=build_hsk_kb())


@router.message(Command('image'))
async def cmd_image(message: types.Message):
    text = "Привет, мир!"  # Вы можете изменить текст или получать его из сообщения
    image_bytes = create_image(text)
    
    # Отправляем изображение пользователю
    await message.answer_photo(photo=image_bytes)
