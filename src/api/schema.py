from typing import List

import strawberry

from src.api.objects import Resonator
from src.api.resolvers.resonator import ResonatorResolver


@strawberry.type
class Query:
    resonators: List[str] = strawberry.field(resolver=ResonatorResolver.resonators)
    resonator: Resonator | None = strawberry.field(resolver=ResonatorResolver.resonator)
