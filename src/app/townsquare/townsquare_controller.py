from typing import List

from strawberry import type, mutation, field, Info

from src.app.townsquare.townsquare import Townsquare
from src.app.townsquare.townsquare_schema import TownsquareIn, TownsquareType, TownsquareUpdateIn
from src.app.townsquare.townsquare_service import get_townsquare_service, TownsquareService

townsquare_service: TownsquareService = get_townsquare_service()


@type
class TownsquareQueries:
    @field
    async def all_townsquares(self) -> List[TownsquareType]:
        townsquare_nodes: List[Townsquare] = await townsquare_service.get_all_townsquares()
        return [TownsquareType.from_node(townsquare_node) for townsquare_node in townsquare_nodes]

    @field
    async def townsquare_by_id(self, townsquare_id: str) -> TownsquareType:
        townsquare_node: Townsquare = await townsquare_service.get_townsquare(townsquare_id)
        return TownsquareType.from_node(townsquare_node)


@type
class TownsquareMutations:
    @mutation
    async def create_townsquare(self, info: Info, new_townsquare: TownsquareIn) -> TownsquareType:
        uid: str = await info.context.uid()
        townsquare = await townsquare_service.create_townsquare(creator_id=uid, name=new_townsquare.name,
                                                                description=new_townsquare.description)
        return TownsquareType.from_node(townsquare)

    @mutation
    async def update_townsquare(self, townsquare_id: str, updated_townsquare: TownsquareUpdateIn) -> TownsquareType:
        townsquare = await townsquare_service.update_townsquare(townsquare_id, **vars(updated_townsquare))
        return TownsquareType.from_node(townsquare)

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
