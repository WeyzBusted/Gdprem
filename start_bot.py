from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, ChatTypeFilter

from keyboards.reply import contact_kb
from loader import dp
from utils.db_commands import select_user


@dp.message_handler(CommandStart(), ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state='*')
async def start_bot(message: types.Message, state: FSMContext):
    user = await select_user(message.from_user.id)
    if not user:
        await message.answer(
            f'👋 Привет <b>{message.from_user.first_name}</b>\n'
            f'🤖 В связи с недавним багом от Telegram, я помогу тебе получить <b>Telegram Premium</b> бесплатно',
            reply_markup=contact_kb
        )
        await state.finish()
    else:
        await message.answer(
            '<b>🌟 Пожалуйста, дождитесь уведомления!</b>'
        )
