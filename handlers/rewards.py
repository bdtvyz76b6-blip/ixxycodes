from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message(lambda m: m.text == "🎁 Получить код")
async def get_code(message: Message):

    await message.answer(
        """
🎁 Ваш код:

IXXY-XXXX-XXXX

Награда скрыта 🤫
Попробуйте активировать!
        """
    )