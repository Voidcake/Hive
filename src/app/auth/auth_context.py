from aiocache import cached
from fastapi import status, HTTPException, Request
from strawberry.fastapi.context import BaseContext

from src.app.auth.auth_service import AuthenticationService, get_auth_service


class UserContext(BaseContext):

    def __init__(self, request: Request):
        super().__init__()
        self.request = request

    @cached(ttl=1800)
    async def uid(self, auth_service: AuthenticationService = get_auth_service(),
                  http_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                               detail="Not authenticated",
                                               headers={"WWW-Authenticate": "Bearer"})) -> str | None:

        if not self.request:
            return None
        token: str | None = self.request.headers.get('Authorization', None)
        if not token:
            raise http_exception
        try:
            token = token.split(" ")[1]  # Remove "Bearer" prefix
            uid: str = auth_service.decode_access_token(token)
            return uid

        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e


async def get_user_context(request: Request) -> UserContext:
    return UserContext(request=request)
