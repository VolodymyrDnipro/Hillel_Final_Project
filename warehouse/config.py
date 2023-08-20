from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from envparse import Env

load_dotenv()
env = Env()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    LOG_LEVEL: str = "DEBUG"

    SERVER_PORT: int
    SERVER_HOST: str


settings = Settings()
