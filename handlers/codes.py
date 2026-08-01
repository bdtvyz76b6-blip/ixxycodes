from aiogram import Router
from aiogram.types import Message

from database import activate_code, add_days


router = Router()


@router.message(lambda m: m.text == "👑 Активировать код")
async def activate_start(message: Message):

    await message.answer(
        "👑 Отправьте ваш код:\n\nПример:\nIXXY-AB12-CD34"
    )



@router.message()
async def activate(message: Message):

    text = message.text.strip()


    if not text.startswith("IXXY-"):
        return


    result = activate_code(text)


    if result is None:

        await message.answer(
            "❌ Такой код не найден"
        )

        return



    if result == "used":

        await message.answer(
            "❌ Этот код уже активирован"
        )

        return



    add_days(
        message.from_user.id,
        result
    )


    await message.answer(
f"""
🎉 Код активирован!

☂️ ixxy VPN

🎁 Начислено:
+{result} дней

Спасибо, что используете ixxy ❤️
"""
    )