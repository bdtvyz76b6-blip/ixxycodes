from aiogram import Router
from aiogram.types import Message

from keyboards import main_menu


router = Router()


@router.message(commands=["start"])
async def start(message: Message):

    await message.answer(
"""
☂️ Добро пожаловать в ixxy Codes

🎁 Получай секретные коды
🎲 Испытай удачу дня
👑 Получай бонусы для ixxy VPN

Выбирай действие 👇
""",
        reply_markup=main_menu()
    )