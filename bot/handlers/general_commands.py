import re

from aiogram import Router, types
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.state import default_state
from data import TEXT_BOT
from keyboards import kb_inline_settings_user
from settings import config
from utils import format_answer_user, answer_users
import subprocess

router_general_commands = Router()


@router_general_commands.message(Command('start'), StateFilter(default_state))
async def command_start(message: types.Message):
    await message.answer(TEXT_BOT.GeneralCommands['start_message'].format(message.from_user.full_name))


@router_general_commands.message(Command('help'), StateFilter(default_state))
async def command_help(message: types.Message):
    for mess in TEXT_BOT.GeneralCommands['help_message']:
        await message.answer(mess)


@router_general_commands.message(Command('settings_user'), StateFilter(default_state))
async def command_settings(message: types.Message):
    await message.answer(TEXT_BOT.GeneralCommands['settings_user_message'], reply_markup=kb_inline_settings_user)


@router_general_commands.message(Command('get_repl_logs'), StateFilter(default_state))
async def command_logs(message: types.Message, command: CommandObject):
    if message.from_user.id in config.ADMINS:
        path = "/var/log/postgresql/postgresql-15-main.log"
        if command.args:
            number = int(re.sub(r'[^\d]', '', command.args))
            output = subprocess.run(["tail", f"-{number}", path],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            output = subprocess.run(["cat", path],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = output.stdout + output.stderr
        await answer_users(message, await format_answer_user(output, message.from_user.id), command)
    else:
        await message.answer(TEXT_BOT.GeneralCommands['permission_denied'])