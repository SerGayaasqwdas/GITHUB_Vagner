from data import ANSWER_MESSAGE_AND_FILE, ANSWER_FILE, ANSWER_MESSAGE
from aiogram import types
from aiogram.filters import CommandObject
from Middlewares import UserSettings
import logging
from utils import BDConnect
from settings import config
import io

loger = logging.getLogger(__name__)


async def format_answer_user(output: str, user_id: int):
    if len(output) > 4095:
        return (io.BytesIO(output.encode('utf-8')),)
    if UserSettings.get(user_id) == ANSWER_MESSAGE_AND_FILE:
        return output, io.BytesIO(output.encode('utf-8'))
    elif UserSettings.get(user_id) == ANSWER_FILE:
        return (io.BytesIO(output.encode('utf-8')),)
    elif UserSettings.get(user_id) == ANSWER_MESSAGE:
        return (output,)
    else:
        loger.critical('Type message not valid')
        raise ValueError()


async def answer_users(message: types.Message, answer: tuple, command: CommandObject):
    for i in answer:
        if type(i) == str:
            await message.answer(i, disable_web_page_preview=True, parse_mode=None)
        elif isinstance(i, io.BytesIO):
            file = types.BufferedInputFile(file=i.getvalue(), filename=f'{command.command}.txt')
            await message.bot.send_document(chat_id=message.chat.id, document=file)
