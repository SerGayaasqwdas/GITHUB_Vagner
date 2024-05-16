from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import Command, StateFilter, CommandObject
from FsmMachine import EmailState, PhoneState
from utils import BDConnect, format_answer_user, answer_users
from settings import config
from data import TEXT_BOT
import logging


loger = logging.getLogger(__name__)

router_bd = Router()
emails_command_insert_bd = ('INSERT INTO emails (user_id, found_emails) VALUES ({0!r}, {1!r}) '
                            'ON CONFLICT (user_id) DO UPDATE SET found_emails = {1!r}')
phones_command_insert_bd = ('INSERT INTO phones (user_id, found_numbers_phone) VALUES ({0!r}, {1!r}) '
                            'ON CONFLICT (user_id) DO UPDATE SET found_numbers_phone = {1!r}')
select_all = 'SELECT * FROM {0}'
select_id = 'Select * FROM {0} WHERE user_id={1!r}'


async def interaction_bd(command: str, method: str):
    params_connect = {'host': config.HOST_IP_BD, 'user': config.USERNAME_BD, 'db': config.DATABASES,
                      'port': config.PORT_BD, 'password': config.PASSWORD_BD}
    values = await BDConnect.interface_bd(command, method, params_connect)
    if isinstance(values, Exception):
        return TEXT_BOT.BDMessage['failed'].format(values)
    if method == 'write':
        return TEXT_BOT.BDMessage['success']
    else:
        return values


async def get_values(message: types.Message, table: str):
    if message.from_user.id in config.ADMINS:
        values = await interaction_bd(select_all.format(table), 'read')
    else:
        values = await interaction_bd(select_id.format(table, str(message.from_user.id)), 'read')
    if not values:
        await message.answer(TEXT_BOT.BDMessage['empty_answer_bd'])
        return
    elif type(values) == str:
        await message.answer(values)
        return
    return values


@router_bd.callback_query(F.data == 'insert', StateFilter(EmailState.EmailFound, PhoneState.PhoneFound))
async def set_users_all(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    emails = data.get('emails')
    phones = data.get('phones')
    if emails:
        command = emails_command_insert_bd.format(str(callback.from_user.id), ', '.join(emails))
    elif phones:
        command = phones_command_insert_bd.format(str(callback.from_user.id), ', '.join(phones))
    else:
        loger.error(f'Emails and Phones None, state_data - {data}')
        return
    await callback.message.answer(await interaction_bd(command, 'write'))
    await callback.answer()
    await state.clear()


@router_bd.callback_query(F.data == 'not_insert', StateFilter(EmailState.EmailFound, PhoneState.PhoneFound))
async def set_users_chat(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()


@router_bd.message(Command('get_emails'), StateFilter(default_state))
async def get_emails(message: types.Message, command: CommandObject):
    values = await get_values(message, 'emails')
    if not values:
        return
    output = ''
    for item in values:
        output += f'id: {item.get("user_id")}\nemails: {item.get("found_emails")}\n\n'
    await answer_users(message, await format_answer_user(output, message.from_user.id), command)


@router_bd.message(Command('get_phone_numbers'), StateFilter(default_state))
async def get_emails(message: types.Message, command: CommandObject):
    values = await get_values(message, 'phones')
    if not values:
        return
    output = ''
    for item in values:
        output += f'id: {item.get("user_id")}\nnumbers: {item.get("found_numbers_phone")}\n\n'
    await answer_users(message, await format_answer_user(output, message.from_user.id), command)

