from fastapi import APIRouter, Request, Depends, HTTPException, status
from pydantic import ValidationError
import uuid
from backend.supervisor import get_supervisor
from backend.users.schemas import UserDetailSchema, UserCreate, UserLogin, ChatMessagePayload
from backend.users.model import User
from backend.users.auth import create_access_token, get_current_user
from backend.users.decolators import login_required
from langgraph.checkpoint.memory import InMemorySaver
router = APIRouter()

checkpointer = InMemorySaver()
@router.post("/login")
async def login_(request: Request):
    data = await request.json()
    try:
        cleaned_data = UserLogin(**data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        user = User.login_user(username=cleaned_data.username, password=cleaned_data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    if user:
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="user or password is wrong")

@router.post("/signup")
async def signup_(request: Request):
    data = await request.json()
    try:
        cleaned_data = UserCreate(**data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        result = User.create_user(username=cleaned_data.username, email=cleaned_data.email, password=cleaned_data.password)
        return {"details": "user created"}, status.HTTP_201_CREATED
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/details")
@login_required
async def user_details(request: Request):
    user = request.user
    return {"username": getattr(user, "username", None), "is_authenticated": getattr(user, "is_authenticated", False)}

@router.post("/query")
@login_required
async def query_(request:Request,payload:ChatMessagePayload):
    supe = get_supervisor(request, checkpointer=checkpointer)
    thread_id = uuid.uuid4()
    msg_data = {
        "messages": [
            {"role": "user",
            "content": f"{payload.message}" 
          },
        ]
    }
    result = supe.invoke(msg_data, {"configurable": {"thread_id": thread_id}})
    if not result:
        raise HTTPException(status_code=400, detail="Error with supervisor")
    messages = result.get("messages")
    if not messages:
        raise HTTPException(status_code=400, detail="Error with supervisor")
    return messages[-1]