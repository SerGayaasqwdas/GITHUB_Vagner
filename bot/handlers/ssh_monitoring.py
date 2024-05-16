import re
from aiogram import Router, types
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.state import default_state
from data import TEXT_BOT
from utils import SSHConnectionFactory, answer_users
from settings import config
import logging

router_ssh_monitoring = Router()


async def telegram_ssh_linux(message: types.Message, answer: tuple, command: CommandObject):
    if not answer:
        await message.answer(TEXT_BOT.MonitoringMessage['answer_empty'])
        return
    await answer_users(message, answer, command)


@router_ssh_monitoring.message(Command(commands=TEXT_BOT.SSHCommands.keys()), StateFilter(default_state))
async def output_monitoring_easy(message: types.Message, command: CommandObject):
    connect = await SSHConnectionFactory.get_connection(host=config.HOST_IP_SSH, user=config.USERNAME_SSH,
                                                        port=config.PORT_SSH, password=config.PASSWORD_SSH)
    if connect:
        answer = await connect.send_command_to_host(TEXT_BOT.SSHCommands[command.command], message.from_user.id)
        await telegram_ssh_linux(message, answer, command)
    else:
        await message.answer(TEXT_BOT.SSHMessage['failed'])


@router_ssh_monitoring.message(Command('get_apt_list'), StateFilter(default_state))
async def output_monitoring_difficult(message: types.Message, command: CommandObject):
    connect = await SSHConnectionFactory.get_connection(host=config.HOST_IP_SSH, user=config.USERNAME_SSH,
                                                        port=config.PORT_SSH, password=config.PASSWORD_SSH)
    if connect:
        if command.args:
            args = re.sub(r'[^\w -]', '', command.args)
            answer = await connect.send_command_to_host(f'dpkg -s {args}', message.from_user.id)
        else:
            answer = await connect.send_command_to_host('apt list --installed', message.from_user.id)
        await telegram_ssh_linux(message, answer, command)
    else:
        await message.answer(TEXT_BOT.SSHMessage['failed'])