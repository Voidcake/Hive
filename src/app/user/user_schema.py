from datetime import datetime
from typing import Annotated, List, TYPE_CHECKING
from uuid import UUID

from strawberry import type, input, Private, lazy

if TYPE_CHECKING:
    from src.app.townsquare.townsquare_schema import TownsquareType
    from src.app.question.question_schema import QuestionType


# INFO
# Circular dependencies -> author: Annotated["User", strawberry.lazy(".users")]


@type
class UserType:
    uid: UUID
    created_at: datetime
    username: str
    email: str
    password: Private[str]
    first_name: str | None = None
    townsquare_memberships: List[
                                Annotated["TownsquareType", lazy("src.app.townsquare.townsquare_schema")]] | None = None
    questions: List[Annotated["QuestionType", lazy("src.app.question.question_schema")]] | None = None


@input
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
