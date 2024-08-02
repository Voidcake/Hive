from typing import List, TYPE_CHECKING, Annotated

from strawberry import type, input, Private, field, lazy

from src.app.arg_framework.claim.claim import Claim
from src.app.arg_framework.question.question import Question
from src.app.base_node import BaseNodeType, MetaType
from src.app.townsquare.townsquare import Townsquare
from src.app.user.user import User

if TYPE_CHECKING:
    from src.app.townsquare.townsquare_schema import TownsquareType
    from src.app.question.question_schema import QuestionType
    from src.app.arg_framework.claim.claim_schema import ClaimType


@type(name="User")
class UserType(BaseNodeType):
    node_instance: Private[User]

    username: str
    email: str
    password: Private[str]
    first_name: str | None = None

    @field
    async def townsquare_memberships(self) -> List[Annotated[
        "TownsquareType", lazy("src.app.townsquare.townsquare_schema")]] | None:
        from src.app.townsquare.townsquare_schema import TownsquareType

        townsquare_nodes: List[Townsquare] = await self.node_instance.townsquare_memberships.all()
        return [TownsquareType.from_node(townsquare_node) for townsquare_node in townsquare_nodes]

    @field
    async def questions(self) -> List[Annotated[
        "QuestionType", lazy("src.app.arg_framework.question.question_schema")]] | None:
        from src.app.arg_framework.question.question_schema import QuestionType

        question_nodes: List[Question] = await self.node_instance.questions.all()
        return [QuestionType.from_node(question_node) for question_node in question_nodes]

    @field
    async def claims(self) -> List[Annotated["ClaimType", lazy("src.app.arg_framework.claim.claim_schema")]] | None:
        from src.app.arg_framework.claim.claim_schema import ClaimType

        claim_nodes: List[Claim] = await self.node_instance.claims.all()
        return [ClaimType.from_node(claim_node) for claim_node in claim_nodes]

    @classmethod
    def from_node(cls, node: User) -> "UserType":
        return UserType(
            node_instance=node,

            meta=MetaType(uid=node.uid, created_at=node.created_at),
            username=node.username,
            email=node.email,
            password=node.password,
            first_name=node.first_name,
        )


@input(name="NewUser")
class UserIn:
    username: str
    email: str
    password: str
    first_name: str | None = None


@input
class UserUpdateIn:
    username: str | None = None
    email: str | None = None
    password: str | None = None
    first_name: str | None = None
