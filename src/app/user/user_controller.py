from typing import List
from uuid import UUID

from strawberry import type, mutation, Info, field

from src.app.user.user import User
from src.app.user.user_schema import UserIn, UserType, UserUpdateIn
from src.app.user.user_service import get_user_service, UserService

user_service: UserService = get_user_service()


@type
class UserQueries:
    @field
    async def all_users(self) -> List[UserType]:
        user_nodes: List[User] = await user_service.get_all_users()
        return [UserType.from_node(user_node) for user_node in user_nodes]

    @field
    async def user_by_id(self, user_id: UUID) -> UserType:
        user_node: User = await user_service.get_user_via_id(user_id)
        return UserType.from_node(user_node)

    @field
    async def user_by_username(self, username: str) -> UserType:
        user_node: User = await user_service.get_user_via_username(username)
        return UserType.from_node(user_node)


@type
class UserMutations:
    @mutation
    async def create_user(self, new_user: UserIn) -> UserType:
        user = await user_service.create_user(new_user.username, new_user.email, new_user.password,
                                              new_user.first_name)
        return UserType.from_node(user)

    @mutation
    async def update_current_user(self, info: Info, updated_user: UserUpdateIn) -> UserType:
        uid: UUID = await info.context.uid()
        user = await user_service.update_user(user_id=uid, **vars(updated_user))
        return UserType.from_node(user)

    @mutation
    async def delete_current_user(self, info: Info, confirmation: bool = False) -> str:
        if not confirmation:
            return "Deletion not confirmed"
        uid: UUID = await info.context.uid()
        return await user_service.delete_user(user_id=uid)

    @mutation
    async def join_townsquare(self, info: Info, townsquare_id: UUID) -> UserType:
        uid: UUID = await info.context.uid()
        user = await user_service.join_townsquare(user_id=uid, townsquare_id=townsquare_id)
        return UserType.from_node(user)

    @mutation
    async def leave_townsquare(self, info: Info, townsquare_id: UUID) -> UserType:
        uid: UUID = await info.context.uid()
        user = await user_service.leave_townsquare(user_id=uid, townsquare_id=townsquare_id)
        return UserType.from_node(user)


@type
class Query:
    @field
    async def user(self) -> UserQueries:
        return UserQueries()


@type
class Mutation:
    @field
    async def user(self) -> UserMutations:
        return UserMutations()
