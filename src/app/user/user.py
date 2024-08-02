from neomodel import StringProperty, EmailProperty, AsyncRelationshipFrom, \
    AsyncRelationshipTo

from src.app.base_node import BaseNode


class User(BaseNode):
    username = StringProperty(required=True, unique_index=True)
    email = EmailProperty(required=True)
    password = StringProperty(required=True)
    first_name = StringProperty(required=True)

    townsquare_memberships = AsyncRelationshipTo('src.app.townsquare.townsquare.Townsquare', 'MEMBER_OF')
    questions = AsyncRelationshipFrom('src.app.arg_framework.question.question.Question', 'ASKED_BY')
    claims = AsyncRelationshipFrom('src.app.arg_framework.claim.claim.Claim', 'AUTHORED_BY')
