import asyncssh
import logging
from pydantic import SecretStr
import asyncio
from utils import format_answer_user

loger = logging.getLogger(__name__)


class SSHConnection:
    def __init__(self):
        self.conn = None
        self.writer = None
        self.reader = None
        self.stderr = None

    async def connect_ssh(self, host: str, port: int, username: str, password: SecretStr):
        try:
            self.conn = await asyncssh.connect(host=host, port=port,
                                               username=username, password=password.get_secret_value(),
                                               encoding='utf-8', known_hosts=None)
            self.writer, self.reader, self.stderr = await self.conn.open_session()
            await self.writer.drain()
            await self.create_outputs()
            return self
        except Exception as e:
            loger.error(f'Not connect to host {host}', exc_info=e)
            return None

    async def close_conn(self):
        self.conn.close()

    @staticmethod
    async def create_task_read(stream: asyncssh.stream.SSHReader):
        while True:
            yield stream.readexactly(1)

    async def stream_read(self, stream, t):
        out = ''
        async for task in self.create_task_read(stream):
            try:
                out += await asyncio.wait_for(task, timeout=t)
            except TimeoutError:
                return out

    async def create_outputs(self, user_id: int = None):
        out = await asyncio.gather(self.stream_read(self.reader, 0.4), self.stream_read(self.stderr, 0.2))
        if out == ['', ''] or not user_id:
            return
        if out[-1]:
            stdout = '\nError:\n'.join(out)
        else:
            stdout = out[0]
        return await format_answer_user(stdout, user_id)

    async def send_command_to_host(self, command: str, user_id: int):
        self.writer.write(command + '\n')
        return await self.create_outputs(user_id)


class SSHConnectionFactory:
    _connections = {}

    @classmethod
    async def get_connection(cls, host: str, user: str, **kwargs):
        if (host, user) not in cls._connections:
            connection = await SSHConnection().connect_ssh(host=host, port=kwargs.get('port'),
                                                           username=user, password=kwargs.get('password'))
            if connection:
                cls._connections[(host, user)] = connection
            else:
                return None
        return cls._connections[(host, user)]

    @classmethod
    async def close_connections(cls):
        for key in cls._connections:
            await cls._connections[key].close_conn()
        cls._connections = {}
