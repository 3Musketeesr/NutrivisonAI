from sqlmodel import Field, SQLModel, Session, select
from backend.helpers import engine as b_engine
from backend.users import validators, security
from backend.users.auth import create_access_token, get_current_user

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(default=None, description="the username to use, it must be unique", unique=True)
    email: str = Field(default=None, description="user email", unique=True)
    password: str = Field(default=None)

    @classmethod
    def create_user(cls, username, email, password):
        with Session(b_engine.get_engine()) as session:
            query = select(cls).where(cls.username == username)
            obj = session.exec(query).first()
            if obj:
                raise ValueError("User already exists")
            valid, msg, email = validators._validate_email(email=email)
            if not valid:
                raise ValueError(msg)
            hashed_psw = security.Hasher.get_password_hash(password)
            obj = cls(username=username, password=hashed_psw, email=email)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    @classmethod
    def login_user(cls, username, password):
        with Session(b_engine.get_engine()) as session:
            query = select(cls).where(cls.username == username)
            obj = session.exec(query).first()
            if not obj:
                raise ValueError("User or password is wrong")
            is_valid = security.Hasher.verify_password(password, obj.password)
            if not is_valid:
                raise ValueError("User or password is wrong")
            return obj


