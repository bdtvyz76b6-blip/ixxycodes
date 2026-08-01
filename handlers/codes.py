from aiogram import Router
from aiogram.types import Message

from database import activate_code, add_days


router=Router()



@router.message(lambda m:m.text=="👑 Активировать код")
async def ask(message:Message):

    await message.answer(
        "Отправьте код IXXY-XXXX-XXXX"
    )



@router.message()
async def activate(message:Message):

    if not message.text.startswith("IXXY-"):
        return


    result=activate_code(
        message.text
    )


    if result=="used":

        await message.answer(
        "❌ Код уже использован"
        )


    elif result:

        add_days(
            message.from_user.id,
            result
        )

        await message.answer(
f"""
🎉 Код активирован!

☂️ ixxy VPN

+{result} дней добавлено
"""
        )


    else:

        await message.answer(
        "❌ Код не найден"
        )