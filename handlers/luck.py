from aiogram import Router
from aiogram.types import Message
import random

from database import can_daily, save_daily

from vpn_api import give_days


router = Router()


@router.message(lambda m: m.text == "🎲 Удача дня")
async def luck(message: Message):

    uid = message.from_user.id


    if not can_daily(uid):

        await message.answer(
            "⏳ Вы уже крутили удачу сегодня"
        )

        return



    save_daily(uid)


    prize = random.choices(
        [0, 1, 3, 7, 14],
        weights=[40, 35, 20, 4, 1]
    )[0]


    if prize:


        response = give_days(
            uid,
            prize
        )


        if response and response.get("status") == "ok":

            await message.answer(
f"""
🎲 Удача дня!

🎉 Вы выиграли:
+{prize} дней ixxy VPN ☂️

📅 Новая дата:
{response.get("date")}
"""
            )

        else:

            await message.answer(
                "❌ Ошибка начисления. Попробуйте позже."
            )


    else:

        await message.answer(
            "😢 Сегодня без выигрыша"
        )