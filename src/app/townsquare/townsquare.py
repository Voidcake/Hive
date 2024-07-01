from neomodel import AsyncStructuredNode, StringProperty, AsyncRelationshipFrom, UniqueIdProperty


class Townsquare(AsyncStructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    description = StringProperty()

    members = AsyncRelationshipFrom('src.app.user.user.User', 'MEMBER_OF')
