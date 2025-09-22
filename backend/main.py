from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from backend.users.model import User
from backend.helpers import engine as b_engine
from backend.users.views import router as user_router
from backend.users.backend import JWTCookieBackend
from starlette.middleware.authentication import AuthenticationMiddleware

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = b_engine.get_engine()
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan, redirect_slashes=True)

# Add authentication middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())

app.include_router(user_router, prefix="/user")

@app.get("/")
async def testing():
    return {"hello": "world"}
