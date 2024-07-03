from neomodel import AsyncStructuredNode, StringProperty, AsyncRelationshipFrom, UniqueIdProperty, DateTimeProperty


class Townsquare(AsyncStructuredNode):
    uid = UniqueIdProperty()
    created_at = DateTimeProperty(default_now=True)
    name = StringProperty(unique_index=True)
    description = StringProperty()

    members = AsyncRelationshipFrom('src.app.user.user.User', 'MEMBER_OF')
    questions = AsyncRelationshipFrom('src.app.question.question.Question', 'ASKED_IN')