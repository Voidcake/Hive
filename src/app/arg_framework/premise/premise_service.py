from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID

from neomodel import adb, AsyncStructuredNode

from src.app.arg_framework.IAddressable import IAddressable
from src.app.arg_framework.IOwnable import IOwnable
from src.app.arg_framework.claim.claim import Claim
from src.app.arg_framework.claim.claim_repository import ClaimRepository, get_claim_repository
from src.app.arg_framework.premise.premise import Premise
from src.app.arg_framework.premise.premise_repository import PremiseRepository, get_premise_repository
from src.app.user.user import User
from src.app.user.user_repository import UserRepository, get_user_repository


class PremiseService(IOwnable, IAddressable):
    def __init__(self, premise_repository: PremiseRepository, user_repository: UserRepository,
                 claim_repository: ClaimRepository):
        self.premise_repository: PremiseRepository = premise_repository
        self.user_repository: UserRepository = user_repository
        self.claim_repository: ClaimRepository = claim_repository

    async def create_premise(self, content: str, author_id: UUID, claim_ids: List[UUID]) -> Premise:
        async with adb.transaction:
            try:
                new_premise: Premise = Premise(created_at=datetime.now(), content=content)
                author: User = await self.user_repository.get(author_id)

                new_premise: Premise = await self.premise_repository.create(new_premise, author)

                for claim_id in claim_ids:
                    await self.address_node(new_premise, claim_id)

                return new_premise

            except LookupError as e:
                raise ValueError(f"Node not found") from e
            except ValueError as e:
                raise e

    async def get_premise(self, premise_id: UUID) -> Premise:
        return await self.premise_repository.get(premise_id)

    async def get_all_premises(self) -> List[Premise]:
        return await self.premise_repository.get_all()

    async def update_premise(self, premise_id: UUID, **kwargs) -> Premise:
        return await self.premise_repository.update(premise_id, **kwargs)

    async def delete_premise(self, premise_id: UUID) -> str:
        return await self.premise_repository.delete(premise_id)

    async def check_ownership(self, user_id: UUID, premise_id: UUID) -> bool:
        premise: Premise = await self.get_premise(premise_id)
        author: User = await premise.author.single()
        if not author:
            raise ValueError(f"Author of the Premise with ID '{premise_id}' not found")

        if author.uid != user_id.hex:
            raise ValueError("You are not the author of this premise")

        return True

    async def address_node(self, source_node: UUID | AsyncStructuredNode, target_node_id: UUID,
                           relationship_type: Enum | None = None) -> Premise:
        if type(source_node) is not Premise:
            source_node: Premise = await self.get_premise(source_node)

        target_node: Claim = await self.claim_repository.get(target_node_id)

        await source_node.claims.connect(target_node)
        return source_node

    async def disconnect_node(self, source_node: Premise, target_node_id: UUID) -> Premise:
        target_node: Claim = await self.claim_repository.get(target_node_id)

        await source_node.claims.disconnect(target_node)
        return source_node


def get_premise_service() -> PremiseService:
    return PremiseService(get_premise_repository(), get_user_repository(), get_claim_repository())
