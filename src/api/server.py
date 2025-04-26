import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from src.data_source.wikiwiki import WikiWikiDataSource


@strawberry.type
class Resonator:
    name: str
    attribute: str
    weapon_type: str


@strawberry.type
class Query:
    @strawberry.field
    def resonator(self, name: str) -> Resonator | None:
        ds = WikiWikiDataSource()
        resonator = ds.get_resonator_by_name(name)

        if resonator is None:
            return None

        return Resonator(
            name=resonator.name,
            attribute=resonator.attribute.to_ja(),
            weapon_type=resonator.weapon_type.to_ja(),
        )


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
