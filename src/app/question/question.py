from neomodel import AsyncStructuredNode, StringProperty, AsyncRelationshipTo, UniqueIdProperty, \
    AsyncOne, DateTimeProperty


class Question(AsyncStructuredNode):
    uid = UniqueIdProperty()
    created_at = DateTimeProperty(default_now=True)
    title = StringProperty(required=True)
    description = StringProperty()

    # Relationships
    townsquare = AsyncRelationshipTo('src.app.townsquare.townsquare.Townsquare', 'ASKED_IN', cardinality=AsyncOne)
    author = AsyncRelationshipTo('src.app.user.user.User', 'ASKED_BY', cardinality=AsyncOne)
