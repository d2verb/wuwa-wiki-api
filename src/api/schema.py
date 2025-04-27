import strawberry
from src.api.objects import Resonator
from src.api.resolvers.resonator import ResonatorResolver


@strawberry.type
class ResonatorQuery:
    resonator: Resonator | None = strawberry.field(resolver=ResonatorResolver.resonator)


@strawberry.type
class Query:
    resonator: ResonatorQuery = strawberry.field(resolver=lambda: ResonatorQuery())
