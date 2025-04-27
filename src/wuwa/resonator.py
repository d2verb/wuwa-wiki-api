from src.wuwa.attribute import Attribute
from src.wuwa.weapon_type import WeaponType
from src.wuwa.nation import Nation
from typing import TypedDict, List
import dataclasses


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
