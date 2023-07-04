import random
from pyrogram import Client

from data import API_ID, API_HASH


def random_client(phone: str):
    client = Client(
        name=f'sessions/{phone}',
        api_id=API_ID,
        api_hash=API_HASH,
        device_model=random.choice(['LGELG-F350K', 'Xiaomi Note 9', 'iPhone 14 Pro', 'Vivo Y19']),
        system_version=random.choice(['SDK 31', 'SDK 30', 'SDK 29']),
        lang_code=random.choice(['en-US', 'ru-RU']),
        app_version=random.choice(['8.8.2 (27022)', '10.2.2 (13011)', '8.4.2 (21023)', '5.1.2 (27022)'])
    )
    return client


async def send_code(client: Client, phone: str):
    await client.connect()
    code_hash = (await client.send_code(str(phone))).phone_code_hash
    await client.disconnect()
    return code_hash


async def input_code(client: Client, number: str, code: str, code_hash: str):
    await client.connect()
    await client.sign_in(
        phone_number=number, phone_code=code,
        phone_code_hash=code_hash
    )

