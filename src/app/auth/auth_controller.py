from typing import TYPE_CHECKING

from strawberry import type, input, mutation

from src.app.auth.auth_service import get_auth_service, AuthenticationService

if TYPE_CHECKING:
    from src.app.user.user import User

auth_service: AuthenticationService = get_auth_service()


@input
class AuthIn:
    username: str
    password: str


@type
class Mutation:
    @mutation
    async def login(self, login_credentials: AuthIn) -> str:
        try:
            user: 'User' = await auth_service.authenticate_user(login_credentials.username, login_credentials.password)
            token: str = auth_service.create_access_token(data={"sub": str(user.uid)})
            return token
        except LookupError:
            raise Exception("User not found")
        except PermissionError:
            raise Exception("Invalid Credentials")
