from datetime import datetime
from typing import List

from passlib.context import CryptContext

from src.app.user.user import User
from src.app.user.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, username: str, email: str, password: str, first_name: str | None) -> User:
        new_user: User = User(created_at=datetime.now(),
                              username=username,
                              email=email,
                              password=pwd_context.hash(password))
        if first_name:
            new_user.first_name = first_name.capitalize()
        return await self.user_repository.create(new_user)

    async def get_user_via_id(self, user_id: str) -> User:
        return await self.user_repository.get(user_id)

    async def get_user_via_username(self, username: str) -> User:
        return await self.user_repository.get_via_username(username)

    async def get_all_users(self) -> List[User]:
        return await self.user_repository.get_all()

    async def update_user(self, user_id: str, **kwargs) -> User:
        return await self.user_repository.update(user_id, **kwargs)

    async def delete_user(self, user_id: str) -> str:
        return await self.user_repository.delete(user_id)

    async def join_townsquare(self, user_id: str, townsquare_id: str) -> User:
        return await self.user_repository.join_townsquare(user_id, townsquare_id)

    async def leave_townsquare(self, user_id: str, townsquare_id: str) -> User:
        return await self.user_repository.leave_townsquare(user_id, townsquare_id)


def get_user_service() -> UserService:
    return UserService(UserRepository())
