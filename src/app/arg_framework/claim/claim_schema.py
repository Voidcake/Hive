from typing import TYPE_CHECKING, Annotated, List
from uuid import UUID

from strawberry import type, input, lazy, Private, field

from src.app.arg_framework.address_relationship import AddressRelationshipSchema
from src.app.arg_framework.claim.claim import Claim
from src.app.base_node import BaseNodeType, MetaType

if TYPE_CHECKING:
    from src.app.user.user_schema import UserType
    from src.app.arg_framework.question.question_schema import QuestionType
    from src.app.arg_framework.premise.premise_schema import PremiseType


@type(name="ClaimRelationships")
class RelationshipsType:
    node_instance: Private[Claim]

    @field
    async def counters(self) -> List[Annotated["ClaimType", lazy("src.app.arg_framework.claim.claim_schema")]]:
        return [ClaimType.from_node(claim_node) for claim_node in await self.node_instance.counters.all()]

    @field
    async def supports(self) -> List[Annotated["ClaimType", lazy("src.app.arg_framework.claim.claim_schema")]]:
        return [ClaimType.from_node(claim_node) for claim_node in await self.node_instance.supports.all()]

    @field
    async def answers(self) -> List[Annotated["QuestionType", lazy("src.app.arg_framework.question.question_schema")]]:
        from src.app.arg_framework.question.question_schema import QuestionType

        return [QuestionType.from_node(question_node) for question_node in await self.node_instance.answers.all()]

    @field
    async def countered_by(self) -> List[Annotated["ClaimType", lazy("src.app.arg_framework.claim.claim_schema")]]:
        return [ClaimType.from_node(claim_node) for claim_node in await self.node_instance.countered_by.all()]

    @field
    async def supported_by(self) -> List[Annotated["ClaimType", lazy("src.app.arg_framework.claim.claim_schema")]]:
        return [ClaimType.from_node(claim_node) for claim_node in await self.node_instance.supported_by.all()]

    @field
    async def questioned_by(self) -> List[
        Annotated["QuestionType", lazy("src.app.arg_framework.question.question_schema")]]:
        from src.app.arg_framework.question.question_schema import QuestionType

        return [QuestionType.from_node(question_node) for question_node in await self.node_instance.questioned_by.all()]


@type(name="Claim")
class ClaimType(BaseNodeType):
    node_instance: Private[Claim]

    content: str

    @field
    async def author(self) -> Annotated["UserType", lazy("src.app.user.user_schema")]:
        from src.app.user.user_schema import UserType

        return UserType.from_node(await self.node_instance.author.single())

    @field
    async def premises(self) -> List[Annotated["PremiseType", lazy("src.app.arg_framework.premise.premise_schema")]]:
        from src.app.arg_framework.premise.premise_schema import PremiseType

        return [PremiseType.from_node(premise_node) for premise_node in await self.node_instance.premises.all()]

    @field
    async def relationships(self) -> RelationshipsType:
        return RelationshipsType(node_instance=self.node_instance)

    @classmethod
    def from_node(cls, node: Claim) -> "ClaimType":
        return ClaimType(
            node_instance=node,

            meta=MetaType(uid=node.uid, created_at=node.created_at),
            content=node.content,
        )


@input(name="ClaimRelationship")
class ClaimRelationshipIn:
    target_node_id: UUID
    relationship_type: AddressRelationshipSchema


@input(name="NewClaim")
class ClaimIn:
    content: str
    relationships: List[ClaimRelationshipIn]


@input(name="UpdatedClaim")
class ClaimUpdateIn:
    claim_id: UUID
    content: str | None = None


@input(name="UpdatedClaimRelationships")
class ClaimUpdateRelationshipIn:
    claim_id: UUID
    relationships: List[ClaimRelationshipIn]
