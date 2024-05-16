from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    HOST_IP_SSH: str
    USERNAME_SSH: str
    PASSWORD_SSH: SecretStr
    PORT_SSH: int
    HOST_IP_BD: str
    USERNAME_BD: str
    PASSWORD_BD: SecretStr
    PORT_BD: str
    DATABASES: str
    ADMINS: list[int]

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf8')


config = Settings()
