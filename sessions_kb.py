from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_commands import select_sessions


async def sessions_kb():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'{session.phone}',
                    callback_data=f'session|{session.id}'
                )
            ] for session in await select_sessions()
        ]
    )
    return markup
