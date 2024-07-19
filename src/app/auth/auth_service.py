import os
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.app.user.user import User
from src.app.user.user_service import get_user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationService:

    def __init__(self):
        self.__secret_key: str = os.getenv("SECRET_KEY")
        self.__algorithm: str = os.getenv("ALGORITHM", "HS256")
        self.__access_token_expire_minutes: timedelta = timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()

        # Add expiration date to the token
        expires_delta: timedelta = expires_delta or self.__access_token_expire_minutes
        expire: datetime = datetime.now() + expires_delta
        to_encode.update({"exp": expire})

        # Encode the token
        try:
            return jwt.encode(to_encode, self.__secret_key, algorithm=self.__algorithm)
        except JWTError as e:
            raise PermissionError("Failed to create access Token") from e

    def decode_access_token(self, token: str) -> UUID:
        """Decode the access token and return the user UUID from (sub)"""
        try:
            payload = jwt.decode(token=token, key=self.__secret_key, algorithms=[self.__algorithm])
            uid: str = payload.get("sub")
            if uid is None:
                raise PermissionError("Invalid token data")
            return UUID(uid)

        except JWTError as e:
            raise PermissionError("Could not validate credentials") from e

    @staticmethod
    async def authenticate_user(username: str, password: str) -> User:
        try:
            user: User = await get_user_service().get_user_via_username(username)
            if not pwd_context.verify(password, user.password):
                raise PermissionError("Wrong Password")
            return user
        except LookupError as e:
            raise e

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        try:
            uid: UUID = self.decode_access_token(token)
            return await get_user_service().get_user_via_id(uid)
        except Exception as e:
            raise e


def get_auth_service() -> AuthenticationService:
    return AuthenticationService()
