from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class PasswordState(StatesGroup):
    InputPassword = State()


class EmailState(StatesGroup):
    InputEmail = State()
    EmailFound = State()


class PhoneState(StatesGroup):
    InputPhone = State()
    PhoneFound = State()
