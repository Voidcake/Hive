from neomodel import AsyncStructuredNode, StringProperty, AsyncRelationshipTo, UniqueIdProperty, \
    AsyncOne


class Question(AsyncStructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    description = StringProperty()

    townsquare = AsyncRelationshipTo('src.app.townsquare.townsquare.Townsquare', 'ASKED_IN', cardinality=AsyncOne)
    author = AsyncRelationshipTo('src.app.user.user.User', 'ASKED_BY', cardinality=AsyncOne)
