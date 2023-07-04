from environs import Env

env = Env()

env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
API_ID = env.int('API_ID')
API_HASH = env.str('API_HASH')

ADMINS_ID = [1537002204]

#СЛИТ В https://t.me/end_soft
