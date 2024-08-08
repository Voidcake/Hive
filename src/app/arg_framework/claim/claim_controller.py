from typing import List
from uuid import UUID

from strawberry import type, mutation, field, Info

from src.app.arg_framework.claim.claim import Claim
from src.app.arg_framework.claim.claim_schema import ClaimType, ClaimIn, ClaimUpdateIn, ClaimUpdateRelationshipIn
from src.app.arg_framework.claim.claim_service import ClaimService, get_claim_service

claim_service: ClaimService = get_claim_service()


@type
class ClaimQueries:
    @field
    async def all_claims(self) -> List[ClaimType]:
        claim_nodes: List[Claim] = await claim_service.get_all_claims()
        return [ClaimType.from_node(claim_node) for claim_node in claim_nodes]

    @field
    async def claim_by_id(self, claim_id: UUID) -> ClaimType:
        claim_node: Claim = await claim_service.get_claim(claim_id)
        return ClaimType.from_node(claim_node)


@type
class ClaimMutations:
    @mutation
    async def create_claim(self, info: Info, new_claim: ClaimIn) -> ClaimType:
        uid: UUID = await info.context.uid()

        relationships: dict = {}

        for relationship in new_claim.relationships:
            relationships[relationship.target_node_id] = relationship.relationship_type

        claim: Claim = await claim_service.create_claim(content=new_claim.content, author_id=uid,
                                                        relationships=relationships)

        return ClaimType.from_node(claim)

    @mutation
    async def update_claim(self, info: Info, updated_claim: ClaimUpdateIn) -> ClaimType:
        uid: UUID = await info.context.uid()

        if await claim_service.check_ownership(user_id=uid, claim_id=updated_claim.claim_id):
            claim = await claim_service.update_claim(**vars(updated_claim))
            return ClaimType.from_node(claim)

    @mutation
    async def update_claim_relationships(self, info: Info, updated_claim: ClaimUpdateRelationshipIn) -> ClaimType:
        uid: UUID = await info.context.uid()

        if await claim_service.check_ownership(user_id=uid, claim_id=updated_claim.claim_id):
            claim: Claim = await claim_service.get_claim(updated_claim.claim_id)

            for relationship in updated_claim.relationships:
                await claim_service.update_claim_relationship(claim=claim,
                                                              target_node_id=relationship.target_node_id,
                                                              relationship_type=relationship.relationship_type)
            return ClaimType.from_node(claim)

    @mutation
    async def delete_claim(self, info: Info, claim_id: UUID, confirmation: bool = False) -> str:
        if not confirmation:
            return "Confirmation required before deleting claim"

        uid: UUID = info.context.uid()

        if await claim_service.check_ownership(user_id=uid, claim_id=claim_id):
            return await claim_service.delete_claim(claim_id)


@type
class Query:
    @field
    async def claim(self) -> ClaimQueries:
        return ClaimQueries()


@type
class Mutation:
    @field
    async def claim(self) -> ClaimMutations:
        return ClaimMutations()
