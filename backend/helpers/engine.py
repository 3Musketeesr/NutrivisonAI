from sqlmodel import create_engine
from backend import config as b_config


settings = b_config.get_settings()
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(settings.AUTH_DB_CONNECTION_STR)
    return _engine