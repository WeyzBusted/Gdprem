from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def actions_kb(session_id: int, phone: str):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'🔐 Коды подтверждения',
                    callback_data=f'get_codes|{session_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='🔃 Конвертировать в Telethon',
                    callback_data=f'telethons|{session_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='🗂 Конвертировать в TData',
                    callback_data=f'tdatas|{phone}'
                )
            ],
        ]
    )
    return markup


def get_code(session_id: int):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'🔐 Получить код',
                    callback_data=f'get_codes|{session_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='← Назад',
                    callback_data=f'session|{session_id}'
                )
            ]
        ]
    )
    return markup
