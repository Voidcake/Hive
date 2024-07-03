from typing import TYPE_CHECKING, Annotated, List

from strawberry import type, ID, lazy, input

if TYPE_CHECKING:
    from src.app.user.user_schema import UserType
    from src.app.townsquare.townsquare_schema import TownsquareType


@type
class QuestionType:
    uid: ID
    title: str
    description: str
    author: List[Annotated["UserType", lazy("src.app.user.user_schema")]]
    townsquare: List[Annotated["TownsquareType", lazy("src.app.townsquare.townsquare_schema")]]


@input
class QuestionIn:
    title: str
    description: str
    townsquare_id: ID  # or townsquareIN?


@input
class QuestionUpdateIn:
    title: str | None = None
    description: str | None = None
