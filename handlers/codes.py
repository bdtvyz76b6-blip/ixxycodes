from aiogram import Router
from aiogram.types import Message

from database import activate_code

from vpn_api import give_days


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



    # отправляем дни в VPN-бот
    response = give_days(
        message.from_user.id,
        result
    )


    if not response or response.get("status") != "ok":

        await message.answer(
            "❌ Не удалось начислить дни.\nПопробуйте позже."
        )

        return



    await message.answer(
f"""
🎉 Код активирован!

☂️ ixxy VPN

🎁 Начислено:
+{result} дней

📅 Новая дата:
{response.get("date")}

Спасибо, что используете ixxy ❤️
"""
    )