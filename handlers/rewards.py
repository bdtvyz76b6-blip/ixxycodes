from aiogram import Router
from aiogram.types import Message

import random
import string

from database import save_code, get_codes


router = Router()



def generate_code():

    chars=string.ascii_uppercase+string.digits

    return (
        "IXXY-"
        +
        ''.join(random.choice(chars) for _ in range(4))
        +
        "-"
        +
        ''.join(random.choice(chars) for _ in range(4))
    )



@router.message(lambda m:m.text=="🎁 Получить код")
async def get_code(message:Message):

    code=generate_code()


    reward=random.choice(
        [1,3,7,14]
    )


    save_code(
        code,
        reward,
        message.from_user.id
    )


    await message.answer(
f"""
🎁 Ваш код:

`{code}`

Активируйте его 👑
""",
parse_mode="Markdown"
)



@router.message(lambda m:m.text=="📋 Мои коды")
async def my_codes(message:Message):

    codes=get_codes(
        message.from_user.id
    )


    if not codes:
        await message.answer(
            "У вас нет кодов 😢"
        )
        return


    text="📋 Ваши коды:\n\n"


    for code,reward,used in codes:

        status="✅" if used else "🎁"

        text+=f"{status} `{code}`\n"


    await message.answer(
        text,
        parse_mode="Markdown"
    )