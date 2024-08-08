from typing import TYPE_CHECKING, Annotated, List
from uuid import UUID

from strawberry import type, lazy, Private, field, input, enum

from src.app.arg_framework.evidence.evidence import Evidence
from src.app.arg_framework.evidence.evidence import EvidenceTypeEnum
from src.app.base_node import BaseNodeType, MetaType

if TYPE_CHECKING:
    from src.app.user.user_schema import UserType
    from src.app.arg_framework.claim.claim_schema import ClaimType


@type(name="Evidence")
class EvidenceType(BaseNodeType):
    node_instance: Private[Evidence]

    content: str
    source: str

    @field
    async def author(self) -> Annotated["UserType", lazy("src.app.user.user_schema")]:
        from src.app.user.user_schema import UserType

        return UserType.from_node(await self.node_instance.author.single())

    @field
    async def supports(self) -> List[Annotated["ClaimType", lazy("src.app.arg_framework.claim.claim_schema")]]:
        from src.app.arg_framework.premise.premise_schema import PremiseType
        return [PremiseType.from_node(premise_node) for premise_node in await self.node_instance.supports.all()]

    @field
    async def counters(self) -> List[Annotated["ClaimType", lazy("src.app.arg_framework.claim.claim_schema")]]:
        from src.app.arg_framework.premise.premise_schema import PremiseType
        return [PremiseType.from_node(premise_node) for premise_node in await self.node_instance.counters.all()]

    @classmethod
    def from_node(cls, node: Evidence) -> "EvidenceType":
        return EvidenceType(
            node_instance=node,

            meta=MetaType(uid=node.uid, created_at=node.created_at),
            content=node.content,
            source=node.source
        )


@input(name="EvidencePremiseRelationship")
class EvidencePremiseIn:
    premise_id: UUID
    evidence_type: enum(EvidenceTypeEnum)


@input(name="NewEvidence")
class EvidenceIn:
    content: str
    source: str
    premises: List[EvidencePremiseIn]


@input(name="UpdatedEvidence")
class EvidenceUpdateIn:
    evidence_id: UUID
    content: str | None = None
    source: str | None = None


@input(name="AddressPremises")
class AddressPremisesIn:
    evidence_id: UUID
    premises: List[EvidencePremiseIn]
