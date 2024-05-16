import asyncio
from aiogram import Bot, Dispatcher
import logging
from settings import config, dp, bot
from handlers import (router_general_commands, router_regex, router_ssh_monitoring,
                      router_set_settings_user, router_bd)
from Middlewares import GeneralOutputMiddleware
from utils import SSHConnectionFactory, start_bot


file_log = logging.FileHandler(filename='bot.log', mode='w', encoding='utf-8')
console_out = logging.StreamHandler()
logging.basicConfig(
    handlers=(file_log, console_out),
    level=logging.DEBUG,
    datefmt='%d.%m.%Y %H:%M:%S',
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s',
)

logger = logging.getLogger(__name__)

dp: Dispatcher
bot: Bot


async def main():
    dp.include_routers(router_general_commands, router_regex, router_ssh_monitoring,
                       router_set_settings_user, router_bd)
    dp.startup.register(start_bot)
    dp.update.outer_middleware(GeneralOutputMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        logger.info('Start Bot')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await SSHConnectionFactory.close_connections()
        logger.info('Stop Bot')

if __name__ == '__main__':
    asyncio.run(main())
