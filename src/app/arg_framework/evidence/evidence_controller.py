from typing import List
from uuid import UUID

from strawberry import Info, mutation, type, field

from src.app.arg_framework.evidence.evidence import Evidence
from src.app.arg_framework.evidence.evidence_schema import EvidenceIn, EvidenceType, EvidenceUpdateIn, AddressPremisesIn
from src.app.arg_framework.evidence.evidence_service import EvidenceService, get_evidence_service

evidence_service: EvidenceService = get_evidence_service()


@type
class EvidenceQueries:
    @field
    async def all_evidence(self) -> List[EvidenceType]:
        evidence_nodes: List[Evidence] = await evidence_service.get_all_evidence()
        return [EvidenceType.from_node(evidence_node) for evidence_node in evidence_nodes]

    @field
    async def evidence_by_id(self, evidence_id: UUID) -> EvidenceType:
        evidence_node: Evidence = await evidence_service.get_evidence(evidence_id)
        return EvidenceType.from_node(evidence_node)


@type
class EvidenceMutations:
    @mutation
    async def create_evidence(self, info: Info, new_evidence: EvidenceIn) -> EvidenceType:
        uid: UUID = await info.context.uid()

        premises: dict = {}

        for premise in new_evidence.premises:
            premises[premise.premise_id] = premise.evidence_type

        evidence: Evidence = await evidence_service.create_evidence(content=new_evidence.content,
                                                                    source=new_evidence.source,
                                                                    author_id=uid,
                                                                    premises=premises)

        return EvidenceType.from_node(evidence)

    @mutation
    async def update_evidence(self, info: Info, updated_evidence: EvidenceUpdateIn) -> EvidenceType:
        uid: UUID = await info.context.uid()

        if await evidence_service.check_ownership(user_id=uid, evidence_id=updated_evidence.evidence_id):
            evidence: Evidence = await evidence_service.update_evidence(**vars(updated_evidence))

            return EvidenceType.from_node(evidence)

    @mutation
    async def update_evidence_relationships(self, info: Info, updated_evidence: AddressPremisesIn) -> EvidenceType:
        uid: UUID = await info.context.uid()

        if await evidence_service.check_ownership(user_id=uid, evidence_id=updated_evidence.evidence_id):
            evidence: Evidence = await evidence_service.get_evidence(updated_evidence.evidence_id)

            for premise in updated_evidence.premises:
                await evidence_service.update_evidence_relationship(evidence=evidence,
                                                                    target_node_id=premise.premise_id,
                                                                    relationship_type=premise.evidence_type)
            return EvidenceType.from_node(evidence)

    @mutation
    async def delete_evidence(self, info: Info, evidence_id: UUID, confirmation: bool = False) -> str:
        if not confirmation:
            return "Confirmation required before deleting evidence"

        uid: UUID = await info.context.uid()

        if await evidence_service.check_ownership(user_id=uid, evidence_id=evidence_id):
            return await evidence_service.delete_evidence(evidence_id)


@type
class Query:
    @field
    def evidence(self) -> EvidenceQueries:
        return EvidenceQueries()


@type
class Mutation:
    @field
    def evidence(self) -> EvidenceMutations:
        return EvidenceMutations()
