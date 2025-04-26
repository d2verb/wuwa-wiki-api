from src.wuwa.attribute import Attribute
from src.wuwa.weapon_type import WeaponType
import dataclasses


@dataclasses.dataclass
class Resonator:
    name: str
    attribute: Attribute
    weapon_type: WeaponType
