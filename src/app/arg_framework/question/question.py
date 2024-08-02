from neomodel import StringProperty, AsyncRelationshipTo, AsyncOne, AsyncRelationshipFrom

from src.app.base_node import BaseNode


class Question(BaseNode):
    question = StringProperty(required=True, unique_index=True)
    description = StringProperty()

    # Relationships
    townsquare = AsyncRelationshipTo('src.app.townsquare.townsquare.Townsquare', 'ASKED_IN', cardinality=AsyncOne)
    author = AsyncRelationshipTo('src.app.user.user.User', 'ASKED_BY', cardinality=AsyncOne)
