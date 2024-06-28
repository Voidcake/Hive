from passlib.context import CryptContext

from app.user.user import User
from src.app.user.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, username: str, email: str, password: str, first_name: str | None) -> User:
        new_user: User = User(username=username,
                              email=email,
                              password=pwd_context.hash(password),
                              first_name=first_name)
        return await self.user_repository.create(new_user)

    async def get_user_via_id(self, uid: str) -> User:
        return await self.user_repository.get(uid)

    async def get_user_via_username(self, username: str) -> User:
        return await self.user_repository.get_via_username(username)

    async def get_all_users(self) -> list[User]:
        return await self.user_repository.get_all()

    async def update_user(self, uid: str, **kwargs) -> User:
        return await self.user_repository.update(uid, **kwargs)

    async def delete_user(self, uid: str) -> str:
        return await self.user_repository.delete(uid)


def get_user_service() -> UserService:
    return UserService(UserRepository())
