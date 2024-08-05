from typing import TYPE_CHECKING, Annotated, List
from uuid import UUID

from strawberry import type, lazy, Private, field, input

from src.app.arg_framework.premise.premise import Premise
from src.app.base_node import BaseNodeType, MetaType

if TYPE_CHECKING:
    from src.app.user.user_schema import UserType
    from src.app.arg_framework.claim.claim_schema import ClaimType


@type(name="Premise")
class PremiseType(BaseNodeType):
    node_instance: Private[Premise]

    content: str

    @field
    async def author(self) -> Annotated["UserType", lazy("src.app.user.user_schema")]:
        from src.app.user.user_schema import UserType

        return UserType.from_node(await self.node_instance.author.single())

    @field
    async def claims(self) -> List[Annotated["ClaimType", lazy("src.app.arg_framework.claim.claim_schema")]]:
        from src.app.arg_framework.claim.claim_schema import ClaimType

        return [ClaimType.from_node(claim_node) for claim_node in await self.node_instance.claims.all()]

    @classmethod
    def from_node(cls, node: Premise) -> "PremiseType":
        return PremiseType(
            node_instance=node,

            meta=MetaType(uid=node.uid, created_at=node.created_at),
            content=node.content
        )


@input(name="NewPremise")
class PremiseIn:
    content: str
    claim_ids: List[UUID]


@input(name="UpdatedPremise")
class PremiseUpdateIn:
    premise_id: UUID
    content: str | None = None
