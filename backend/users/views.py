from fastapi import APIRouter, Request
from pydantic import ValidationError
from backend.users.schemas import UserDetailSchema, LoginSchema, UserCreate
from backend.users.model import User
router = APIRouter()

"""
here i will need views for this, but they are just api routes they dont return website: 
- a view to return user details : -> get request 
- a view to login: -> post request, return the api token and use that token to log in   
- a view to create account : -> post request, return a mesange respose of either succeful creation of account 
or if there was an error  
(for now ) 
"""

@router.post("/login")
async def login_(request: Request):
    data = await request.json()
    print(data)
    return {"wow":"its working"}


@router.post("/signup") 
async def signup_(request: Request): 
    data = await request.json()
    cleaned_data =UserCreate(**data)
    print(cleaned_data)
    print(cleaned_data.model_dump_json())
    User.create_user(username=cleaned_data.username, email=cleaned_data.email,password= cleaned_data.password)


    return {"hello":"world"}