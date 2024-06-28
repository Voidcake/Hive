from strawberry import type, input, ID, Private

#INFO
# Circular dependencies -> author: Annotated["User", strawberry.lazy(".users")]


@type
class UserType:
    uid: ID
    username: str
    email: str
    password: Private[str]
    first_name: str | None = None


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
