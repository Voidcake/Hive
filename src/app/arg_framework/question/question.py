from neomodel import StringProperty, AsyncRelationshipTo, AsyncOne

from src.app.BaseNode import BaseNode


class Question(BaseNode):  # , AddressableNode):
    question = StringProperty(required=True)
    description = StringProperty()

    # Relationships
    townsquare = AsyncRelationshipTo('src.app.townsquare.townsquare.Townsquare', 'ASKED_IN', cardinality=AsyncOne)
    author = AsyncRelationshipTo('src.app.user.user.User', 'ASKED_BY', cardinality=AsyncOne)
