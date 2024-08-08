from typing import List
from uuid import UUID

from strawberry import type, field, mutation, Info

from src.app.arg_framework.premise.premise import Premise
from src.app.arg_framework.premise.premise_schema import PremiseType, PremiseIn, PremiseUpdateIn
from src.app.arg_framework.premise.premise_service import PremiseService, get_premise_service

premise_service: PremiseService = get_premise_service()


@type
class PremiseQueries:
    @field
    async def all_premises(self) -> List[PremiseType]:
        premise_nodes: List[Premise] = await premise_service.get_all_premises()
        return [PremiseType.from_node(premise_node) for premise_node in premise_nodes]

    @field
    async def premise_by_id(self, premise_id: UUID) -> PremiseType:
        premise_node: Premise = await premise_service.get_premise(premise_id)
        return PremiseType.from_node(premise_node)


@type
class PremiseMutations:
    @mutation
    async def create_premise(self, info: Info, new_premise: PremiseIn) -> PremiseType:
        uid: UUID = await info.context.uid()

        premise: Premise = await premise_service.create_premise(content=new_premise.content, author_id=uid,
                                                                claim_ids=new_premise.claim_ids)

        return PremiseType.from_node(premise)

    @mutation
    async def update_premise(self, info: Info, updated_premise: PremiseUpdateIn) -> PremiseType:
        uid: UUID = await info.context.uid()

        if await premise_service.check_ownership(user_id=uid, premise_id=updated_premise.premise_id):
            premise = await premise_service.update_premise(**vars(updated_premise))
            return PremiseType.from_node(premise)

    @mutation
    async def address_claims(self, info: Info, premise_id: UUID, claim_ids: List[UUID]) -> PremiseType:
        uid: UUID = await info.context.uid()

        if await premise_service.check_ownership(user_id=uid, premise_id=premise_id):
            premise: Premise = await premise_service.get_premise(premise_id)

            for claim_id in claim_ids:
                await premise_service.address_node(premise, claim_id)

            return PremiseType.from_node(premise)

    @mutation
    async def disconnect_node(self, info: Info, premise_id: UUID, claim_ids: List[UUID]) -> PremiseType:
        uid: UUID = await info.context.uid()

        if await premise_service.check_ownership(user_id=uid, premise_id=premise_id):
            premise: Premise = await premise_service.get_premise(premise_id)

            for claim_id in claim_ids:
                await premise_service.disconnect_node(premise, claim_id)

            return PremiseType.from_node(premise)

    @mutation
    async def delete_premise(self, info: Info, confirmation: bool = False) -> str:
        if not confirmation:
            return "Confirmation required to delete premise"

        if await premise_service.check_ownership(user_id=uid, premise_id=premise_id):
            return await premise_service.delete_premise(premise_id)


@type
class Query:
    @field
    async def premise(self) -> PremiseQueries:
        return PremiseQueries()


@type
class Mutation:
    @field
    async def premise(self) -> PremiseMutations:
        return PremiseMutations()
