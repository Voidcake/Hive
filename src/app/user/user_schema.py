from typing import Annotated, List, TYPE_CHECKING

from strawberry import type, input, ID, Private, lazy

if TYPE_CHECKING:
    from src.app.townsquare.townsquare_schema import TownsquareType, TownsquareIn


# INFO
# Circular dependencies -> author: Annotated["User", strawberry.lazy(".users")]


@type
class UserType:
    uid: ID
    username: str
    email: str
    password: Private[str]
    first_name: str | None = None
    townsquare_memberships: List[Annotated["TownsquareType", lazy("src.app.townsquare.townsquare_schema")]] | None = None


@input
class UserIn:
    username: str
    email: str
    password: str
    first_name: str | None = None
    townsquare_memberships: List[Annotated["TownsquareIn", lazy("src.app.townsquare.townsquare_schema")]] | None = None


@input
class UserUpdateIn:
    username: str | None = None
    email: str | None = None
    password: str | None = None
    first_name: str | None = None
    townsquare_memberships: List[Annotated["TownsquareIn", lazy("src.app.townsquare.townsquare_schema")]] | None = None
