from neomodel import StringProperty, AsyncRelationshipFrom

from src.app.BaseNode import BaseNode


class Townsquare(BaseNode):
    name = StringProperty(unique_index=True)
    description = StringProperty()

    members = AsyncRelationshipFrom('src.app.user.user.User', 'MEMBER_OF')
    questions = AsyncRelationshipFrom('src.app.arg_framework.question.question.Question', 'ASKED_IN')
