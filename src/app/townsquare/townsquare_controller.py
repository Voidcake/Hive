from typing import List

from strawberry import type, mutation, field, Info

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
    async def create_townsquare(self, info: Info, new_townsquare: TownsquareIn) -> TownsquareType:
        uid: str = await info.context.uid()
        return await townsquare_service.create_townsquare(creator_id=uid, name=new_townsquare.name,
                                                          description=new_townsquare.description)

    @mutation
    async def update_townsquare(self, townsquare_id: str, updated_townsquare: TownsquareUpdateIn) -> TownsquareType:
        return await townsquare_service.update_townsquare(townsquare_id, **vars(updated_townsquare))

    @mutation
    async def delete_townsquare(self, townsquare_id: str, confirmation: bool = False) -> str:
        if not confirmation:
            return "Deletion not confirmed"
        return await townsquare_service.delete_townsquare(townsquare_id)


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
