from enum import Enum, auto

from neomodel import StringProperty, AsyncRelationshipTo, AsyncOne

from src.app.base_node import BaseNode


class Evidence(BaseNode):
    content = StringProperty(required=True)
    source = StringProperty(required=True)  # TODO: string -> Source Node
    author = AsyncRelationshipTo('src.app.user.user.User', 'AUTHORED_BY', cardinality=AsyncOne)

    supports = AsyncRelationshipTo('src.app.arg_framework.premise.premise.Premise', 'SUPPORTS')
    counters = AsyncRelationshipTo('src.app.arg_framework.premise.premise.Premise', 'COUNTERS')


class EvidenceTypeEnum(Enum):
    SUPPORTS = auto()
    COUNTERS = auto()
