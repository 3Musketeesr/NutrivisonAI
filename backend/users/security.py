from passlib.context import CryptContext
from pydantic import ValidationError
import zxcvbn
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
    

class PASSWORD_VALIDATOR():
    @staticmethod
    def verify_password(plain_password,user_name): 
        if len(plain_password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        
        # Check strength with zxcvbn
        result = zxcvbn.zxcvbn(plain_password, user_inputs=[user_name])
        if result["score"] < 3:  # 0–4 scale
            raise ValueError("Password is too weak.")
        
        return plain_password
    