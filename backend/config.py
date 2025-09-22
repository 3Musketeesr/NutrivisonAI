from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    backend_dir: Path = Path(__file__).resolve().parent
    base_dir: Path = Path(__file__).resolve().parent.parent
    AUTH_DB_CONNECTION_STR: str
    SECRET_KEY: str
    GOOGLE_API_KEY:str 
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    class Config:
        env_file = str(Path(__file__).resolve().parent.parent / ".env")

@lru_cache
def get_settings():
    return Settings()
