from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
    DATABASE_URL: str

settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)