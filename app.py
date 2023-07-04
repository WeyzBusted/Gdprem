import logging
from aiogram import executor

from handlers import dp
from utils import set_default_commands
from utils.database import create_base


async def on_startup(dp):
    await set_default_commands(dp)
    await create_base()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, on_startup=on_startup)
