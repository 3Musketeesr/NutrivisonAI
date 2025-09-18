from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    UnauthenticatedUser,
    AuthCredentials
)

from .auth import get_current_user

class JWTCookieBackend(AuthenticationBackend):
    async def authenticate(self, request):
        # Check Authorization header first
        auth_header = request.headers.get("authorization")
        token = None
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ", 1)[1]
        else:
            # Fallback to cookie
            token = request.cookies.get("session_id")
        if not token:
            return AuthCredentials(["anon"]), UnauthenticatedUser()
        try:
            user = await get_current_user(token)
            if not user:
                return AuthCredentials(["anon"]), UnauthenticatedUser()
            return AuthCredentials(["authenticated"]), SimpleUser(user.username)
        except Exception:
            return AuthCredentials(["anon"]), UnauthenticatedUser()