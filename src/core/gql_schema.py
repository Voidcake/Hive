from functools import lru_cache
from importlib import import_module
from pathlib import Path

from strawberry import type, Schema
from strawberry.extensions import QueryDepthLimiter, MaxAliasesLimiter, MaxTokensLimiter
from strawberry.fastapi import GraphQLRouter

from src.app.auth.auth_context import get_user_context


# Dynamically locate controller modules and import classes based on class name
@lru_cache(maxsize=None)
def dynamic_import_classes(class_name) -> list:
    return [
        getattr(import_module(module_path), class_name)
        for module_path in
        (str(file).replace('/', '.').replace('\\', '.')[:-3] for file in Path('src/app').glob('**/*_controller.py'))
        if hasattr(import_module(module_path), class_name)
    ]


# Define GraphQL schema using aggregated classes
@type
class Query(*(dynamic_import_classes('Query'))):
    pass


@type
class Mutation(*(dynamic_import_classes('Mutation'))):
    pass


security_extensions = [QueryDepthLimiter(10), MaxAliasesLimiter(10), MaxTokensLimiter(1000)]
schema: Schema = Schema(query=Query, mutation=Mutation, extensions=security_extensions)

graphql_app: GraphQLRouter = GraphQLRouter(schema=schema, context_getter=get_user_context, graphql_ide="graphiql")
