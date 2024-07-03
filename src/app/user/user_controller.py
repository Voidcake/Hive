from typing import List

from strawberry import type, mutation, Info, field

from src.app.townsquare.townsquare_schema import TownsquareType
from src.app.user.user_schema import UserIn, UserType, UserUpdateIn
from src.app.user.user_service import get_user_service, UserService

user_service: UserService = get_user_service()


@type
class UserQueries:
    all_users: List[UserType] = field(resolver=user_service.get_all_users)
    user_by_id: UserType | None = field(resolver=user_service.get_user_via_id)
    user_by_username: UserType | None = field(resolver=user_service.get_user_via_username)
    all_townsquare_memberships: List[TownsquareType] = field(resolver=user_service.get_all_townsquare_memberships)


@type
class UserMutations:
    @mutation
    async def create_user(self, new_user: UserIn) -> UserType:
        return await user_service.create_user(new_user.username, new_user.email, new_user.password,
                                              new_user.first_name)

    @mutation
    async def update_current_user(self, info: Info, updated_user: UserUpdateIn) -> UserType:
        uid: str = await info.context.uid()
        return await user_service.update_user(user_id=uid, **vars(updated_user))

    @mutation
    async def delete_current_user(self, info: Info, confirmation: bool = False) -> str:
        if not confirmation:
            return "Deletion not confirmed"
        uid: str = await info.context.uid()
        return await user_service.delete_user(user_id=uid)

    @mutation
    async def join_townsquare(self, info: Info, townsquare_id: str) -> UserType:
        uid: str = await info.context.uid()
        return await user_service.join_townsquare(user_id=uid, townsquare_id=townsquare_id)

    @mutation
    async def leave_townsquare(self, info: Info, townsquare_id: str) -> UserType:
        uid: str = await info.context.uid()
        return await user_service.leave_townsquare(user_id=uid, townsquare_id=townsquare_id)


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
