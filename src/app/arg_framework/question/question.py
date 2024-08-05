from neomodel import StringProperty, AsyncRelationshipTo, AsyncOne, AsyncRelationshipFrom, AsyncZeroOrOne

from src.app.base_node import BaseNode


class Question(BaseNode):
    question = StringProperty(required=True, unique_index=True)
    description = StringProperty()

    author = AsyncRelationshipTo('src.app.user.user.User', 'ASKED_BY', cardinality=AsyncOne)
    townsquare = AsyncRelationshipTo('src.app.townsquare.townsquare.Townsquare', 'ASKED_IN', cardinality=AsyncZeroOrOne)

    # Claims
    questions = AsyncRelationshipTo('src.app.arg_framework.claim.claim.Claim', 'QUESTIONS', cardinality=AsyncZeroOrOne)
    answered_by = AsyncRelationshipFrom('src.app.arg_framework.claim.claim.Claim', 'ANSWERED_BY')
