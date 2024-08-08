from neomodel import StringProperty, AsyncRelationshipFrom, AsyncRelationshipTo, AsyncOne

from src.app.base_node import BaseNode


class Premise(BaseNode):
    content = StringProperty(required=True)
    author = AsyncRelationshipTo('src.app.user.user.User', 'AUTHORED_BY', cardinality=AsyncOne)

    claims = AsyncRelationshipFrom('src.app.arg_framework.claim.claim.Claim', 'HAS_PREMISE')
    evidence = AsyncRelationshipFrom('src.app.arg_framework.evidence.evidence.Evidence', 'SUPPORTS')
