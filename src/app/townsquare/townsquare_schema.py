from typing import Annotated, List, TYPE_CHECKING

from strawberry import type, input, ID, lazy

if TYPE_CHECKING:
    from src.app.user.user_schema import UserType

@type
class TownsquareType:
    uid: ID
    name: str
    description: str
    members: List[Annotated["UserType", lazy("src.app.user.user_schema")]]


@input
class TownsquareIn:
    name: str
    description: str | None = None


@input
class TownsquareUpdateIn:
    name: str | None = None
    description: str | None = None
