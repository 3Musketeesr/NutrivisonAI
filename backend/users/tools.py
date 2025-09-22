from langchain_core.tools import tool
from fastapi import Request
from datetime import date, datetime
from typing import List
from sqlmodel import Session, select
from backend.users.model import User, Detail, FoodHist
from backend.helpers import engine as b_engine

@tool
def get_user_details(request: Request) -> dict | str:
    """Get the authenticated user's details from the database."""
    if not request.user.is_authenticated:
        raise ValueError("User is not authenticated")
    username = request.user.username
    with Session(b_engine.get_engine()) as session:
        q = select(User).where(User.username == username)
        obj = session.exec(q).first()
        if not obj:
            raise ValueError("User object not found")
        details = Detail.get_details(user_id=obj.id)
        return details

@tool
def create_or_update_user_details(request: Request, birth_date: date, height: float, medication: str | None = None) -> str:
    """Create or update the authenticated user's details in the database."""
    if not request.user.is_authenticated:
        raise ValueError("User is not authenticated")
    username = request.user.username
    with Session(b_engine.get_engine()) as session:
        q = select(User).where(User.username == username)
        obj = session.exec(q).first()
        if not obj:
            raise ValueError("User object not found")
    details = Detail.create_or_update_detail(user_id=obj.id, birth_date=birth_date, height=height, medication=medication)
    if details:
        return "success"
    else:
        return "error"

@tool
def add_food_history(request: Request, foodname: str, food_content: str) -> str:
    """Add a food history entry for the authenticated user."""
    if not request.user.is_authenticated:
        raise ValueError("User is not authenticated")
    username = request.user.username
    with Session(b_engine.get_engine()) as session:
        q = select(User).where(User.username == username)
        obj = session.exec(q).first()
        if not obj:
            raise ValueError("User object not found")
    try:
        FoodHist.add_food_entry(user_id=obj.id, foodname=foodname, food_content=food_content)
        return "success"
    except Exception as e:
        return f"error: {str(e)}"

@tool
def get_food_history(request: Request) -> list[dict]:
    """Get the full food history for the authenticated user as a list of dictionaries."""
    if not request.user.is_authenticated:
        raise ValueError("User is not authenticated")
    username = request.user.username
    with Session(b_engine.get_engine()) as session:
        q = select(User).where(User.username == username)
        obj = session.exec(q).first()
        if not obj:
            raise ValueError("User object not found")
    objs = FoodHist.get_food_history(user_id=obj.id)
    return [obj.model_dump() for obj in objs]

@tool
def get_food_history_by_date_range(request: Request, start_date: datetime | None = None, end_date: datetime | None = None) -> list[dict]:
    """Get the food history for the authenticated user within a specified date range as a list of dictionaries.
    
    Args:
        start_date: Optional start date for the range (inclusive).
        end_date: Optional end date for the range (inclusive).
    """
    if not request.user.is_authenticated:
        raise ValueError("User is not authenticated")
    username = request.user.username
    with Session(b_engine.get_engine()) as session:
        q = select(User).where(User.username == username)
        user_obj = session.exec(q).first()
        if not user_obj:
            raise ValueError("User object not found")
        
        query = select(FoodHist).where(FoodHist.user_id == user_obj.id)
        if start_date:
            query = query.where(FoodHist.date_time >= start_date)
        if end_date:
            query = query.where(FoodHist.date_time <= end_date)
        objs = session.exec(query).all()
    return [obj.model_dump() for obj in objs]


def get_user_tools()->List:
    return [get_user_details,
            create_or_update_user_details,
            add_food_history,
            get_food_history,
            get_food_history_by_date_range
            ]
