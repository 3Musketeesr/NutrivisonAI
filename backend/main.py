from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from backend.users.model import User
from backend.helpers import engine as b_engine

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = b_engine.get_engine()
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def testing():
    return {"hello": "world"}