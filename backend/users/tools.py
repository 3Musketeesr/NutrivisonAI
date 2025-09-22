from langchain_core.tools import tool
from datetime import date, datetime
from typing import List
from sqlmodel import Session, select
from backend.users.model import User, Detail, FoodHist
from backend.helpers import engine as b_engine
import re


def get_user_tools(request) -> List:
    """Create user tools bound to the current request via closures.

    This avoids exposing non-serializable types (like Request) in tool schemas.
    """
    req = request

    @tool
    def get_user_details() -> dict | str:
        """Get the authenticated user's details from the database."""
        if not getattr(req.user, "is_authenticated", False):
            raise ValueError("User is not authenticated")
        username = req.user.username
        with Session(b_engine.get_engine()) as session:
            q = select(User).where(User.username == username)
            obj = session.exec(q).first()
            if not obj:
                raise ValueError("User object not found")
            details = Detail.get_details(user_id=obj.id)
            return details

    @tool
    def create_or_update_user_details(birth_date: date, height: float, medication: str | None = None) -> str:
        """Create or update the authenticated user's details in the database."""
        if not getattr(req.user, "is_authenticated", False):
            raise ValueError("User is not authenticated")
        username = req.user.username
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
    def add_food_history(foodname: str, food_content: str) -> str:
        """Add a food history entry for the authenticated user."""
        if not getattr(req.user, "is_authenticated", False):
            raise ValueError("User is not authenticated")
        username = req.user.username
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
    def get_food_history() -> list[dict]:
        """Get the full food history for the authenticated user as a list of dictionaries."""
        if not getattr(req.user, "is_authenticated", False):
            raise ValueError("User is not authenticated")
        username = req.user.username
        with Session(b_engine.get_engine()) as session:
            q = select(User).where(User.username == username)
            obj = session.exec(q).first()
            if not obj:
                raise ValueError("User object not found")
        objs = FoodHist.get_food_history(user_id=obj.id)
        return [obj.model_dump() for obj in objs]

    @tool
    def get_food_history_by_date_range(start_date: datetime | None = None, end_date: datetime | None = None) -> list[dict]:
        """Get the food history for the authenticated user within a specified date range as a list of dictionaries.
        
        Args:
            start_date: Optional start date for the range (inclusive).
            end_date: Optional end date for the range (inclusive).
        """
        if not getattr(req.user, "is_authenticated", False):
            raise ValueError("User is not authenticated")
        username = req.user.username
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

    @tool
    def parse_birth_date(text: str) -> date:
        """Parse a natural-language birth date (e.g., '2003 June 30th') into a date object."""
        months = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
            'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9,
            'sept': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        }
        s = text.strip().lower()
        s = re.sub(r"[,]+", " ", s)
        # Remove ordinal suffixes
        s = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", s)

        # Common pattern: YYYY month DD
        m = re.search(r"(\d{4})\s+([a-zA-Z]+)\s+(\d{1,2})", s)
        if m:
            year = int(m.group(1))
            month_name = m.group(2)
            day = int(m.group(3))
            month = months.get(month_name.lower())
            if month:
                return date(year, month, day)

        # Pattern: DD month YYYY
        m = re.search(r"(\d{1,2})\s+([a-zA-Z]+)\s+(\d{4})", s)
        if m:
            day = int(m.group(1))
            month_name = m.group(2)
            year = int(m.group(3))
            month = months.get(month_name.lower())
            if month:
                return date(year, month, day)

        # Pattern: YYYY-MM-DD or DD-MM-YYYY
        m = re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", s)
        if m:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = re.search(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", s)
        if m:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))

        raise ValueError("Could not parse birth date from text")

    @tool
    def parse_height_to_cm(text: str) -> float:
        """Parse natural-language height into centimeters (e.g., '5 meters' -> 500.0)."""
        s = text.strip().lower()
        # meters
        m = re.search(r"(\d+(?:\.\d+)?)\s*m(eters)?\b", s)
        if m:
            return float(m.group(1)) * 100.0
        # centimeters
        m = re.search(r"(\d+(?:\.\d+)?)\s*cm\b|centimeters?\b", s)
        if m:
            # If 'centimeters' matched without number, fall through
            try:
                return float(m.group(1))
            except Exception:
                pass
        # plain number assume centimeters
        m = re.search(r"\b(\d{2,3})(?:\.\d+)?\b", s)
        if m:
            return float(m.group(1))
        raise ValueError("Could not parse height from text")

    return [
        get_user_details,
        create_or_update_user_details,
        add_food_history,
        get_food_history,
        get_food_history_by_date_range,
        parse_birth_date,
        parse_height_to_cm,
    ]
