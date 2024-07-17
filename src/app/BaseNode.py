from datetime import datetime
from uuid import UUID

from neomodel import AsyncStructuredNode, UniqueIdProperty, DateTimeProperty
from strawberry import interface


class BaseNode(AsyncStructuredNode):
    __abstract_node__ = True

    uid = UniqueIdProperty()
    created_at = DateTimeProperty()


@interface
class BaseNodeType:
    uid: UUID
    created_at: datetime
