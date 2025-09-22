from sqlmodel import Field, SQLModel, Session, select
from datetime import datetime, date
from backend.helpers import engine as b_engine
from backend.users import validators, security

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(default=None, description="the username to use, it must be unique", unique=True)
    email: str = Field(default=None, description="user email", unique=True)
    password: str = Field(default=None)

    @classmethod
    def create_user(cls, username, email, password):
        """This method creates a user object and returns the user object"""
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
        """This method verifies that username and password are correct and returns the user object"""
        with Session(b_engine.get_engine()) as session:
            query = select(cls).where(cls.username == username)
            obj = session.exec(query).first()
            if not obj:
                raise ValueError("User or password is wrong")
            is_valid = security.Hasher.verify_password(password, obj.password)
            if not is_valid:
                raise ValueError("User or password is wrong")
            return obj

class Detail(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", description="Foreign key referencing the User model")
    birth_date: date = Field(description="User's birth date")
    height: float = Field(ge=0.0, description="User's height in centimeters")
    medication: str | None = Field(default=None, max_length=500, description="Description of user's medication, if any")

    def get_age(self) -> int:
        """This method is used to return the age of the user object"""
        today = date.today()
        age = today.year - self.birth_date.year
        if today.month < self.birth_date.month or (today.month == self.birth_date.month and today.day < self.birth_date.day):
            age -= 1
        return age

    @classmethod
    def create_or_update_detail(cls, user_id: int, birth_date: date, height: float, medication: str | None):
        """Creates a user detail object and returns the detail object"""
        with Session(b_engine.get_engine()) as session:
            query = select(cls).where(cls.user_id == user_id)
            detail = session.exec(query).first()
            if detail:
                detail.birth_date = birth_date
                detail.height = height
                detail.medication = medication
            else:
                detail = cls(user_id=user_id, birth_date=birth_date, height=height, medication=medication)
            session.add(detail)
            session.commit()
            session.refresh(detail)
            return detail

    @classmethod
    def get_details(cls, user_id):
        with Session(b_engine.get_engine()) as session:
            query = select(cls).where(cls.user_id == user_id)
            detail = session.exec(query).first()
            if not detail:
                return f"No details found for user {user_id}"
            return {
                "birth_date": detail.birth_date,
                "age": detail.get_age(),
                "height": detail.height,
                "medication": detail.medication
            }

class FoodHist(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", description="Foreign key referencing the User model")
    date_time: datetime = Field(default_factory=datetime.utcnow, description="Date and time of food intake")
    foodname: str = Field(max_length=100, description="Name of the food consumed")
    food_content: str = Field(max_length=500, description="Description of the food content")

    @classmethod
    def add_food_entry(cls, user_id: int, foodname: str, food_content: str):
        """This method is used to create a FoodHist object"""
        with Session(b_engine.get_engine()) as session:
            food_entry = cls(user_id=user_id, foodname=foodname, food_content=food_content)
            session.add(food_entry)
            session.commit()
            session.refresh(food_entry)
            return food_entry

    @classmethod
    def get_food_history(cls, user_id):
        with Session(b_engine.get_engine()) as session:
            q = select(cls).where(cls.user_id == user_id)
            objs = session.exec(q).all()
        return objs
