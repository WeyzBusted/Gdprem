import asyncio
import shutil
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile
from pathlib import Path

from keyboards.inline.sessions_kb import sessions_kb
from loader import dp
from manager.exceptions import ValidationError
from manager.manager import SessionManager
from utils.db_commands import select_session


@dp.callback_query_handler(Text(startswith='telethons'), state='*')
async def convert_session(call: types.CallbackQuery):
    await call.answer('⏳ Конвертирую сессию в Telethon...')
    session = await select_session(int(call.data.split('|')[1]))
    if session:
        try:
            converter = await SessionManager.from_pyrogram_file(Path(f'sessions/{session.phone}.session'))
            await converter.to_telethon_file(Path(f'telethons/{session.phone}.session'))
            await call.message.answer_document(
                document=InputFile(f'telethons/{session.phone}.session'),
                caption='<b>🐍 Файл сессии (Telethon)</b>'
            )
            await call.message.answer(
                f'<b>🐍 Строка сессии (Telethon):</b>\n<code>{converter.to_telethon_string()}</code>'
            )
        except ValidationError:
            await call.message.answer(
                '<b>❌ Произошла ошибка при конвертации сессии!</b>'
            )
    else:
        await call.message.delete()
        await call.message.answer(
            '<b>❗️ Такой сессии не существует!</b>'
        )
        await call.message.answer(
            '<b>⚡️ Список сессий:</b>',
            reply_markup=await sessions_kb()
        )


@dp.callback_query_handler(Text(startswith='tdatas'), state='*')
async def convert_to_tdata(call: types.CallbackQuery):
    await call.answer('⏳ Конвертирую сессию в TData...')
    phone = call.data.split('|')[1]
    try:
        converter = await SessionManager.from_pyrogram_file(Path(f'sessions/{phone}.session'))
        await converter.to_tdata_folder(Path(f'tdatas/{phone}'))
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, shutil.make_archive, f'tdatas/{phone}', 'zip', f'tdatas/{phone}')
        await call.message.answer_document(
            document=InputFile(f'tdatas/{phone}.zip'),
            caption='<b>🗂 Архив сессии TData</b>'
        )
    except ValidationError:
        await call.message.answer(
            '<b>❌ Произошла ошибка при конвертации сессии!</b>'
        )
