import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from database import init_codes

from handlers import (
    start,
    rewards,
    luck,
    codes
)


async def main():

    init_db()

    bot = Bot(
        BOT_TOKEN
    )

    dp = Dispatcher()


    dp.include_router(
        start.router
    )

    dp.include_router(
        rewards.router
    )

    dp.include_router(
        luck.router
    )

    dp.include_router(
        codes.router
    )


    print("☂️ ixxy Codes запущен")


    await dp.start_polling(bot)



if __name__ == "__main__":

    asyncio.run(main())