import logging
import asyncio
import asyncpg
from pydantic import SecretStr

loger = logging.getLogger(__name__)


class BDWorker:
    def __init__(self):
        self.__connect = None

    async def bd_connect(self, user: str, host: str, db: str = None, port: int = None, password: SecretStr = None):
        try:
            self.__connect = await asyncpg.connect(user=user, password=password.get_secret_value(), host=host,
                                                   port=port, database=db)
            return self
        except Exception as e:
            loger.exception('bd_connect failed', exc_info=e)
            return e

    async def read(self, command):
        try:
            data = await self.__connect.fetch(command)
            return data
        except Exception as e:
            loger.warning('bd read failed', exc_info=e)
            return e

    async def write(self, command):
        try:
            await self.__connect.execute(command)
        except Exception as e:
            loger.warning('bd write failed', exc_info=e)
            return e


class BDConnect:
    _connection = {}

    @classmethod
    async def get_connect(cls, user: str, host: str, db: str = None, port: int = None, password: SecretStr = None):
        if not cls._connection.get((user, host, db)):
            tmp = BDWorker()
            tmp = await tmp.bd_connect(user, host, db, port, password)
            if isinstance(tmp, Exception):
                return tmp
            cls._connection[(user, host, db)] = tmp
        return cls._connection[(user, host, db)]

    @classmethod
    async def interface_bd(cls, command: str, f: str, params_connect):
        connect = await cls.get_connect(params_connect.get('user'), params_connect.get('host'),
                                        params_connect.get('db'), params_connect.get('port'),
                                        params_connect.get('password'))
        if isinstance(connect, Exception):
            return connect
        if f == 'read':
            return await connect.read(command)
        elif f == 'write':
            return await connect.write(command)
