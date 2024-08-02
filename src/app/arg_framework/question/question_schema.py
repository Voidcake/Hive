from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from strawberry import type, input, lazy, field, Private

from src.app.arg_framework.question.question import Question
from src.app.base_node import BaseNodeType, MetaType

if TYPE_CHECKING:
    from src.app.user.user_schema import UserType
    from src.app.townsquare.townsquare_schema import TownsquareType


@type
class QuestionType(BaseNodeType):
    node_instance: Private[Question]

    question: str
    description: str | None = None

    @field
    async def author(self) -> Annotated["UserType", lazy("src.app.user.user_schema")]:
        from src.app.user.user_schema import UserType

        author_node: User = await self.node_instance.author.single()
        return UserType.from_node(author_node)

    @field
    async def townsquare(self) -> Annotated["TownsquareType", lazy("src.app.townsquare.townsquare_schema")]:
        from src.app.townsquare.townsquare_schema import TownsquareType

        townsquare_node: Townsquare = await self.node_instance.townsquare.single()
        return TownsquareType.from_node(townsquare_node)

    @classmethod
    def from_node(cls, node: Question) -> "QuestionType":
        return QuestionType(
            node_instance=node,

            meta=MetaType(uid=node.uid, created_at=node.created_at),
            question=node.question,
            description=node.description,
        )


@input(name="NewQuestion")
class QuestionIn:
    question: str
    description: str | None = None
    townsquare_id: UUID
    addressed_node_id: UUID | None = None  # TODO: implement


@input
class QuestionUpdateIn:
    question: str | None = None
    description: str | None = None
