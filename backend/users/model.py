from sqlmodel import Field, SQLModel, Session, select
from backend.helpers import engine as b_engine
from backend.users import validators, security
from pydantic import ValidationError
class User(SQLModel, table=True):
    __tablename__ = "user"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(default=None, description="the username to use, it must be unique", unique=True)
    email: str = Field(default=None, description="user email", unique=True)
    password: str = Field(default=None)

    @classmethod
    def create_user(cls,username,email,password):
       with Session(b_engine.get_engine()) as session: 
            query = select(cls).where(cls.username == username)
            obj = session.exec(query).first()
            if not obj:
                valid, msg, email = validators._validate_email(email=email)
                if not valid: 
                    raise ValidationError(msg)
                valid_psw = security.PASSWORD_VALIDATOR.verify_password(password,username)
                hashed_psw = security.Hasher.get_password_hash(password=valid_psw)
                obj = cls(username=username, password=hashed_psw, email=email)
                session.add(obj)
                session.commit()
                session.refresh(obj)
                return obj
            return None

