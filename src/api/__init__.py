import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.api.di import DIContainer, get_context
from src.api.schema import Query


def create_app() -> FastAPI:
    app = FastAPI()

    container = DIContainer()
    container.wire(modules=[__name__])
    app.container = container  # type: ignore

    schema = strawberry.Schema(query=Query)
    graphql_app = GraphQLRouter(schema, context_getter=get_context)
    app.include_router(graphql_app, prefix="/graphql")

    return app
