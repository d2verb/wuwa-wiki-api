from typing import List

import strawberry


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


@strawberry.type
class Echo:
    name: str
    attribute: str
    enemy_class: str
    description: str