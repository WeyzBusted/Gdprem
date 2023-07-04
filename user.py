from aiogram.dispatcher.filters.state import StatesGroup, State


class CodeNumber(StatesGroup):
    number = State()
    password = State()
