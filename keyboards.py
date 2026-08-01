from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎁 Получить код"),
                KeyboardButton(text="🎲 Удача дня")
            ],
            [
                KeyboardButton(text="📋 Мои коды"),
                KeyboardButton(text="👑 Активировать код")
            ]
        ],
        resize_keyboard=True
    )