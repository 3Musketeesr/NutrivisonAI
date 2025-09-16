from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "user"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(default=None, description="the username to use, it must be unique", unique=True)
    email: str = Field(default=None, description="user email", unique=True)
    password: str = Field(default=None)

