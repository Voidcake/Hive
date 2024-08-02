from datetime import datetime
from uuid import UUID

from neomodel import AsyncStructuredNode, UniqueIdProperty, DateTimeProperty
from strawberry import interface, type


class BaseNode(AsyncStructuredNode):
    __abstract_node__ = True

    uid = UniqueIdProperty()
    created_at = DateTimeProperty()


@type(name="Metadata")
class MetaType:
    uid: UUID
    created_at: datetime


@interface(name="BaseNode")
class BaseNodeType:
    meta: MetaType
