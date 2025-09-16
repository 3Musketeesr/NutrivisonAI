
from sqlmodel import create_engine, Session 
from backend.helpers import engine as b_engine

engine = b_engine.get_engine()

def get_session():
    with Session(engine) as session: 
        yield session