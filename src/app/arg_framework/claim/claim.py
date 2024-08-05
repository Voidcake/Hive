from neomodel import StringProperty, AsyncRelationshipTo, AsyncOne, AsyncRelationshipFrom

from src.app.base_node import BaseNode


class Claim(BaseNode):
    content = StringProperty(required=True)
    author = AsyncRelationshipTo('src.app.user.user.User', 'AUTHORED_BY', cardinality=AsyncOne)

    attacks = AsyncRelationshipTo('src.app.arg_framework.claim.claim.Claim', 'ATTACKS')
    supports = AsyncRelationshipTo('src.app.arg_framework.claim.claim.Claim', 'SUPPORTS')
    answers = AsyncRelationshipTo('src.app.arg_framework.question.question.Question', 'ANSWERS')

    attacked_by = AsyncRelationshipFrom('src.app.arg_framework.claim.claim.Claim', 'ATTACKED_BY')
    supported_by = AsyncRelationshipFrom('src.app.arg_framework.claim.claim.Claim', 'SUPPORTED_BY')
    questioned_by = AsyncRelationshipFrom('src.app.arg_framework.question.question.Question', 'QUESTIONS')

    # TODO: premises
    # TODO: evidence = AsyncRelationshipFrom('app.evidence.evidence.Evidence', 'SUPPORTS', model='evidence')
