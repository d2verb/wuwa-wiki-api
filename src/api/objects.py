import strawberry
from typing import List


@strawberry.type
class ResonatorStory:
    title: str
    content: str


@strawberry.type
class Resonator:
    name: str
    attribute: str
    weapon_type: str
    nation: str
    stories: List[ResonatorStory]
