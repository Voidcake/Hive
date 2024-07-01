from typing import List

from strawberry import type, mutation, field

from src.app.townsquare.townsquare_schema import TownsquareIn, TownsquareType, TownsquareUpdateIn
from src.app.townsquare.townsquare_service import get_townsquare_service, TownsquareService
from src.app.user.user_schema import UserType

townsquare_service: TownsquareService = get_townsquare_service()


@type
class TownsquareQueries:
    all_townsquares: List[TownsquareType] = field(resolver=townsquare_service.get_all_townsquares)
    townsquare_by_id: TownsquareType | None = field(resolver=townsquare_service.get_townsquare_via_id)
    all_members: List[UserType] = field(resolver=townsquare_service.get_all_members)


@type
class TownsquareMutations:
    @mutation
    async def create_townsquare(self, new_townsquare: TownsquareIn) -> TownsquareType:
        return await townsquare_service.create_townsquare(new_townsquare.name, new_townsquare.description)

    @mutation
    async def update_townsquare(self, uid: str, updated_townsquare: TownsquareUpdateIn) -> TownsquareType:
        return await townsquare_service.update_townsquare(uid, **vars(updated_townsquare))

    @mutation
    async def delete_townsquare(self, uid: str) -> str:
        return await townsquare_service.delete_townsquare(uid)


@type
class Query:
    @field
    async def townsquare(self) -> TownsquareQueries:
        return TownsquareQueries()


@type
class Mutation:
    @field
    async def townsquare(self) -> TownsquareMutations:
        return TownsquareMutations()
