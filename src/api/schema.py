from typing import List

import strawberry

from src.api.objects import Echo, Resonator, Archive
from src.api.resolvers.echoes import EchoResolver
from src.api.resolvers.resonator import ResonatorResolver
from src.api.resolvers.archive import ArchiveResolver

@strawberry.type
class Query:
    resonators: List[str] = strawberry.field(resolver=ResonatorResolver.resonators)
    resonator: Resonator | None = strawberry.field(resolver=ResonatorResolver.resonator)
    echoes: List[str] = strawberry.field(resolver=EchoResolver.echoes)
    echo: Echo | None = strawberry.field(resolver=EchoResolver.echo)
    archives: List[str] = strawberry.field(resolver=ArchiveResolver.archives)
    archive: Archive | None = strawberry.field(resolver=ArchiveResolver.archive)

schema = strawberry.Schema(query=Query)
