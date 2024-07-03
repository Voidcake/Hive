from datetime import datetime
from typing import Annotated, List, TYPE_CHECKING
from uuid import UUID

from strawberry import type, input, lazy

if TYPE_CHECKING:
    from src.app.user.user_schema import UserType
    from src.app.question.question_schema import QuestionType


@type
class TownsquareType:
    uid: UUID
    created_at: datetime
    name: str
    description: str
    members: List[Annotated["UserType", lazy("src.app.user.user_schema")]]
    questions: List[Annotated["QuestionType", lazy("src.app.question.question_schema")]]


@input
class TownsquareIn:
    name: str
    description: str | None = None


@input
class TownsquareUpdateIn:
    name: str | None = None
    description: str | None = None
