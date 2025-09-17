from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import field_validator
from pydantic import ValidationInfo, ValidationError
from backend.users.model import User
from zxcvbn import zxcvbn
from sqlmodel import select, Session
from backend.helpers import engine as b_engine
from backend.users.validators import _validate_email
class LoginSchema(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: str 
    password: str


    @field_validator("password")
    def validate_password(cls, v: str, info: ValidationInfo) -> str:
        username = (info.data or {}).get("username", "")
        
        # Minimum length rule
        if len(v) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        # Check strength with zxcvbn
        result = zxcvbn(v, user_inputs=[username])
        if result["score"] < 3:  # 0–4 scale
            raise ValidationError("Password is too weak.")
        
        return v
    
    @field_validator("username")
    def validate_username(cls,v:str, info:ValidationInfo) -> str: 
        with Session(b_engine.get_engine()) as session: 
            query = select(User).where(User.username == v)
            obj = session.exec(query).first()
            if obj: 
                raise ValidationError("USER EXISTS!!")
            session.close() 
        return v 
    
    @field_validator("email")
    def validate_password(cls,v:str,info:ValidationError) -> str: 
        valid, msg, email= _validate_email(v)
        if not valid: 
            raise ValidationError(f"EMAIL NOT VALID: {msg}")
        return email



class UserDetailSchema(BaseModel):
    username: str