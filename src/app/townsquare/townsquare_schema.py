from typing import List, TYPE_CHECKING, Annotated

from strawberry import type, input, field, Private, lazy

from src.app.BaseNode import BaseNodeType
from src.app.townsquare.townsquare import Townsquare
from src.app.user.user import User

if TYPE_CHECKING:
    from src.app.user.user_schema import UserType
    from src.app.arg_framework.question.question_schema import QuestionType


@type
class TownsquareType(BaseNodeType):
    name: str
    description: str

    node_instance: Private[Townsquare]

    @field
    async def members(self) -> List[Annotated["UserType", lazy("src.app.user.user_schema")]]:
        from src.app.user.user_schema import UserType

        member_nodes: List[User] = await self.node_instance.members.all()
        return [UserType.from_node(member_node) for member_node in member_nodes]

    @field
    async def questions(self) -> List[
        Annotated["QuestionType", lazy("src.app.arg_framework.question.question_schema")]]:
        from src.app.arg_framework.question.question_schema import QuestionType

        question_nodes: List[Question] = await self.node_instance.questions.all()
        return [QuestionType.from_node(question_node) for question_node in question_nodes]

    @classmethod
    def from_node(cls, node: Townsquare) -> "TownsquareType":
        return cls(
            uid=node.uid,
            created_at=node.created_at,
            name=node.name,
            description=node.description,
            node_instance=node
        )


@input
class TownsquareIn:
    name: str
    description: str | None = None


@input
class TownsquareUpdateIn:
    name: str | None = None
    description: str | None = None
