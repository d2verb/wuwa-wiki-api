import dataclasses
from typing import List, TypedDict

from src.wuwa.attribute import Attribute
from src.wuwa.nation import Nation
from src.wuwa.weapon_type import WeaponType


class ResonatorStory(TypedDict):
    title: str
    content: str


@dataclasses.dataclass
class Resonator:
    name: str
    attribute: Attribute
    weapon_type: WeaponType
    nation: Nation
    stories: List[ResonatorStory]
