from aiogram import Router
from aiogram.types import Message

from keyboards import main_menu
from database import add_user


router = Router()


@router.message(commands=["start"])
async def start(message: Message):

    add_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        """
☂️ Добро пожаловать в ixxy Codes

🎁 Получай секретные коды
🎲 Испытай удачу
👑 Забирай бонусы

Выбирай действие 👇
        """,
        reply_markup=main_menu()
    )