from neomodel import AsyncStructuredNode, StringProperty, EmailProperty, UniqueIdProperty, AsyncRelationshipFrom, \
    AsyncRelationshipTo, DateTimeProperty


class User(AsyncStructuredNode):
    uid = UniqueIdProperty()
    created_at = DateTimeProperty(default_now=True)
    username = StringProperty(required=True, unique_index=True)
    email = EmailProperty(required=True, unique_index=True)
    password = StringProperty(required=True)
    first_name = StringProperty(required=True)

    townsquare_memberships = AsyncRelationshipTo('src.app.townsquare.townsquare.Townsquare', 'MEMBER_OF')
    questions = AsyncRelationshipFrom('src.app.question.question.Question', 'ASKED_BY')
