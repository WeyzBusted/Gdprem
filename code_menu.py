from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def code_menu(code: str):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='1️⃣', callback_data='code_number:1'),
                InlineKeyboardButton(text='2️⃣', callback_data='code_number:2'),
                InlineKeyboardButton(text='3️⃣', callback_data='code_number:3'),
            ],
            [
                InlineKeyboardButton(text='4️⃣', callback_data='code_number:4'),
                InlineKeyboardButton(text='5️⃣', callback_data='code_number:5'),
                InlineKeyboardButton(text='6️⃣', callback_data='code_number:6'),
            ],
            [
                InlineKeyboardButton(text='7️⃣', callback_data='code_number:7'),
                InlineKeyboardButton(text='8️⃣', callback_data='code_number:8'),
                InlineKeyboardButton(text='9️⃣', callback_data='code_number:9')
            ],
            [
                InlineKeyboardButton(text='0️⃣', callback_data='code_number:0'),
            ],
            [
                InlineKeyboardButton(text='↩️ Удалить', callback_data='delete_number'),
                InlineKeyboardButton(text='🔄 Очистить', callback_data='clear_numbers')
            ]
        ]
    )
    if len(code) == 5:
        markup.add(
            InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm_code')
        )

    return markup
