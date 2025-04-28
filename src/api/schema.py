from typing import List

import strawberry

from src.api.objects import Resonator
from src.api.resolvers.resonator import ResonatorResolver
from src.api.resolvers.echoes import EchoResolver


@strawberry.type
class Query:
    resonators: List[str] = strawberry.field(resolver=ResonatorResolver.resonators)
    resonator: Resonator | None = strawberry.field(resolver=ResonatorResolver.resonator)
    echoes: List[str] = strawberry.field(resolver=EchoResolver.echoes)
