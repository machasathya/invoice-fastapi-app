from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str  # Note: Port is generally not part of the host in this URL format, but handled by the driver
    MYSQL_DB_NAME: str
    SECRERT_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config():
        env_file = ".env"


settings = Settings()
