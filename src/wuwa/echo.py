from src.wuwa.attribute import Attribute
from src.wuwa.enemy_class import EnemyClass

import dataclasses

@dataclasses.dataclass
class Echo:
    name: str
    attribute: Attribute
    enemy_class: EnemyClass
    description: str