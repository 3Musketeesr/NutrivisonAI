from functools import wraps
from fastapi import Request
from .exceptions import LoginRequiredException

def login_required(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if not getattr(request.user, "is_authenticated", False):
            raise LoginRequiredException(status_code=401)
        return await func(request, *args, **kwargs)
    return wrapper