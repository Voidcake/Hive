from datetime import datetime
from typing import List
from uuid import UUID

from neomodel import AsyncStructuredNode, adb

from src.app.arg_framework.IAddressable import IAddressable
from src.app.arg_framework.IOwnable import IOwnable
from src.app.arg_framework.address_relationship import AddressRelationship
from src.app.arg_framework.claim.claim import Claim
from src.app.arg_framework.claim.claim_repository import ClaimRepository, get_claim_repository
from src.app.arg_framework.question.question import Question
from src.app.user.user import User
from src.app.user.user_repository import UserRepository


class ClaimService(IOwnable, IAddressable):
    def __init__(self, claim_repository: ClaimRepository, user_repository: UserRepository):
        self.claim_repository: ClaimRepository = claim_repository
        self.user_repository: UserRepository = user_repository

    async def create_claim(self, content: str, author_id: UUID, relationships: dict) -> Claim:
        async with adb.transaction:
            try:
                new_claim: Claim = Claim(created_at=datetime.now(), content=content)
                author: User = await self.user_repository.get(author_id)
                new_claim: Claim = await self.claim_repository.create(new_claim, author)

                for addressed_node_id, relationship_type in relationships.items():
                    await self.address_node(new_claim, addressed_node_id, relationship_type)

                return new_claim

            except LookupError as e:
                raise ValueError(f"Node not found") from e
            except ValueError as e:
                raise e

    async def get_claim(self, claim_id: UUID) -> Claim:
        return await self.claim_repository.get(claim_id)

    async def get_all_claims(self) -> List[Claim]:
        return await self.claim_repository.get_all()

    async def update_claim(self, claim_id: UUID, **kwargs) -> Claim:
        return await self.claim_repository.update(claim_id, **kwargs)

    async def update_claim_relationship(self, claim: Claim,
                                        target_node_id: UUID, relationship_type: AddressRelationship) -> Claim:
        async with adb.transaction:
            await self.disconnect_node(claim.uid, target_node_id)
            await self.address_node(claim.uid, target_node_id, relationship_type)

        return claim

    async def delete_claim(self, claim_id: UUID) -> str:
        return await self.claim_repository.delete(claim_id)

    async def check_ownership(self, user_id: UUID, claim_id: UUID) -> bool:
        claim: Claim = await self.get_claim(claim_id)
        author: User = await claim.author.single()
        if not author:
            raise ValueError(f"Author of the Claim with ID '{claim_id}' not found")

        if author.uid != user_id.hex:
            raise PermissionError("You are not the author of this claim")
        return True

    # TODO: refactor signature into generic IAdresssable interface
    async def address_node(self, source_node: Claim, target_node_id: UUID,
                           relationship_type: AddressRelationship) -> Claim:
        target_node: AsyncStructuredNode = await self.claim_repository.query_nodes(target_node_id)

        if relationship_type == AddressRelationship.ATTACKS:
            await source_node.counters.connect(target_node)
        elif relationship_type == AddressRelationship.SUPPORTS:
            await source_node.supports.connect(target_node)
        elif relationship_type == AddressRelationship.ANSWERS:
            await source_node.answers.connect(target_node)
        else:
            raise ValueError("Invalid relationship type")

        return source_node

    async def disconnect_node(self, source_node: UUID, target_node_id: UUID) -> Claim:
        claim: Claim = await self.get_claim(source_node)
        target_node: AsyncStructuredNode = await self.claim_repository.query_nodes(target_node_id)

        if target_node.__class__ == Question:
            await claim.answers.disconnect(target_node)

        elif target_node.__class__ == Claim and target_node in await claim.supports.all():
            await claim.supports.disconnect(target_node)

        elif target_node.__class__ == Claim and target_node in await claim.counters.all():
            await claim.counters.disconnect(target_node)

        else:
            raise ValueError("Relationship between the source node and target node not found or invalid")

        return claim


def get_claim_service() -> ClaimService:
    return ClaimService(get_claim_repository(), UserRepository())
