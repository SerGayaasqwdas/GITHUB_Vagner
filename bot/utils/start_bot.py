from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from data import TEXT_BOT
from settings import bot, config


async def set_commands(bot: Bot):
    commands = []
    for i in TEXT_BOT.MenuCommands:
        commands.append(BotCommand(command=i, description=TEXT_BOT.MenuCommands[i]))
    await bot.set_my_commands(commands=commands)


async def start_bot(bot: Bot):
    await set_commands(bot)
