from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='🌟 ПОЛУЧИТЬ PREMIUM',
                request_contact=True
            )
        ]
    ],
    resize_keyboard=True
)
