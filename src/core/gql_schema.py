from strawberry import type, Schema
from strawberry.extensions import QueryDepthLimiter
from strawberry.fastapi import GraphQLRouter

from src.app.auth.auth_context import get_user_context
from src.app.auth.auth_controller import Mutation as AuthMutations
from src.app.townsquare.townsquare_controller import Mutation as TownsquareMutations
from src.app.townsquare.townsquare_controller import Query as TownsquareQueries
from src.app.user.user_controller import Mutation as UserMutations
from src.app.user.user_controller import Query as UserQueries


@type
class Query(UserQueries, TownsquareQueries):
    pass


@type
class Mutation(UserMutations, AuthMutations, TownsquareMutations):
    pass


schema: Schema = Schema(query=Query, mutation=Mutation, extensions=[QueryDepthLimiter(15)])

graphql_app: GraphQLRouter = GraphQLRouter(schema=schema, context_getter=get_user_context)
