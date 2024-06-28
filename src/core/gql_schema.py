from strawberry import type, Schema
from strawberry.extensions import QueryDepthLimiter
from strawberry.fastapi import GraphQLRouter

from src.app.auth.auth_context import get_user_context
from src.app.user.user_controller import Mutation as UserMutations
from src.app.user.user_controller import Query as UserQueries
from src.app.auth.auth_controller import Mutation as AuthMutations


@type
class Query(UserQueries):
    pass


@type
class Mutation(UserMutations, AuthMutations):
    pass


schema: Schema = Schema(query=Query, mutation=Mutation, extensions=[QueryDepthLimiter(15)])

graphql_app: GraphQLRouter = GraphQLRouter(schema=schema, context_getter=get_user_context)
