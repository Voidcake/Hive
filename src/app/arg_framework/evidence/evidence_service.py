from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID

from neomodel import adb

from src.app.arg_framework.IAddressable import IAddressable
from src.app.arg_framework.IOwnable import IOwnable
from src.app.arg_framework.evidence.evidence import Evidence, EvidenceTypeEnum
from src.app.arg_framework.evidence.evidence_repository import EvidenceRepository, get_evidence_repository
from src.app.arg_framework.premise.premise import Premise
from src.app.arg_framework.premise.premise_repository import PremiseRepository, get_premise_repository
from src.app.user.user import User
from src.app.user.user_repository import UserRepository, get_user_repository


class EvidenceService(IAddressable, IOwnable):
    def __init__(self, evidence_repository: EvidenceRepository, user_repository: UserRepository,
                 premise_repository: PremiseRepository):
        self.evidence_repository: EvidenceRepository = evidence_repository
        self.user_repository: UserRepository = user_repository
        self.premise_repository: PremiseRepository = premise_repository

    async def create_evidence(self, content: str, source: str, author_id: UUID, premises: dict) -> Evidence:
        async with adb.transaction:
            try:
                new_evidence: Evidence = Evidence(created_at=datetime.now(), content=content, source=source)
                author: User = await self.user_repository.get(author_id)
                new_evidence: Evidence = await self.evidence_repository.create(new_evidence, author)

                for premise_id, relationship_type in premises.items():
                    await self.address_node(new_evidence, premise_id, relationship_type)

                return new_evidence
            except LookupError as e:
                raise ValueError(f"Node not found") from e
            except ValueError as e:
                raise e

    async def get_evidence(self, evidence_id: UUID) -> Evidence:
        return await self.evidence_repository.get(evidence_id)

    async def get_all_evidence(self) -> List[Evidence]:
        return await self.evidence_repository.get_all()

    async def update_evidence(self, evidence_id: UUID, **kwargs) -> Evidence:
        return await self.evidence_repository.update(evidence_id, **kwargs)

    async def update_evidence_relationship(self, evidence: Evidence, target_node_id: UUID,
                                           relationship_type: EvidenceTypeEnum) -> Evidence:
        async with adb.transaction:
            try:
                await self.disconnect_node(evidence.uid, target_node_id)
                await self.address_node(evidence.uid, target_node_id, relationship_type)

                return evidence
            except ValueError as e:
                raise e

    async def delete_evidence(self, claim_id: UUID) -> str:
        return await self.evidence_repository.delete(claim_id)

    async def address_node(self, source_node: UUID | Evidence, target_node_id: UUID,
                           relationship_type: Enum | None = None) -> Evidence:
        if type(source_node) is not Evidence:
            source_node: Evidence = await self.evidence_repository.get(source_node)

        target_premise: Premise = await self.premise_repository.get(target_node_id)

        if relationship_type == EvidenceTypeEnum.SUPPORTS:
            await source_node.supports.connect(target_premise)
        elif relationship_type == EvidenceTypeEnum.COUNTERS:
            await source_node.counters.connect(target_premise)
        else:
            raise ValueError(f"Invalid relationship type: {relationship_type}")

        return source_node

    async def disconnect_node(self, source_node: UUID | Evidence, target_node_id: UUID) -> Evidence:
        if source_node is not Evidence:
            source_node: Evidence = await self.evidence_repository.get(source_node)

        target_premise: Premise = await self.premise_repository.get(target_node_id)

        if target_premise in await source_node.supports.all():
            await source_node.supports.disconnect(target_premise)
        elif target_premise in await source_node.counters.all():
            await source_node.counters.disconnect(target_premise)
        else:
            raise ValueError("Relationship between the source node and target node not found or invalid")

        return source_node

    async def check_ownership(self, user_id: UUID, evidence_id: UUID) -> bool:
        evidence: Evidence = await self.evidence_repository.get(evidence_id)
        author: User = await evidence.author.single()

        if author.uid != user_id.hex:
            raise PermissionError("You are not the author of this evidence")
        return True


def get_evidence_service() -> EvidenceService:
    return EvidenceService(get_evidence_repository(), get_user_repository(), get_premise_repository())
