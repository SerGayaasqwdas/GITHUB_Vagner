from aiogram import Router, types, F
from data import ANSWER_MESSAGE_AND_FILE, ANSWER_FILE, ANSWER_MESSAGE, TEXT_BOT
from Middlewares import UserSettings
import logging

loger = logging.getLogger(__name__)

router_set_settings_user = Router()


async def answer_users_set_settings(callback: types.CallbackQuery, values):
    loger.debug(f'Set Settings User {UserSettings}, user - {callback.from_user.id}')
    if callback.from_user.id in UserSettings:
        UserSettings[callback.from_user.id] = values
    else:
        await callback.message.answer(TEXT_BOT.SettingsMessage['error_set_users'])
        return
    await callback.message.answer(TEXT_BOT.SettingsMessage['success_set_users'])
    await callback.answer()


@router_set_settings_user.callback_query(F.data == 'all')
async def set_users_all(callback: types.CallbackQuery):
    await answer_users_set_settings(callback, ANSWER_MESSAGE_AND_FILE)


@router_set_settings_user.callback_query(F.data == 'chat')
async def set_users_chat(callback: types.CallbackQuery):
    await answer_users_set_settings(callback, ANSWER_MESSAGE)


@router_set_settings_user.callback_query(F.data == 'file')
async def set_user_file(callback: types.CallbackQuery):
    await answer_users_set_settings(callback, ANSWER_FILE)
