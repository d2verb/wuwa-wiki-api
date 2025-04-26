from enum import Enum


class WeaponType(str, Enum):
    SWORD = "sword"
    BROADBLADE = "broadblade"
    PISTOL = "pistol"
    GAUNTLET = "gauntlet"
    RECTIFIER = "rectifier"

    @classmethod
    def from_ja(cls, ja: str) -> "WeaponType":
        match ja:
            case "迅刀":
                return cls.SWORD
            case "長刃":
                return cls.BROADBLADE
            case "拳銃":
                return cls.PISTOL
            case "手甲":
                return cls.GAUNTLET
            case "増幅器":
                return cls.RECTIFIER
            case _:
                raise ValueError(f"Invalid weapon type: {ja}")

    def to_ja(self) -> str:
        match self:
            case WeaponType.SWORD:
                return "迅刀"
            case WeaponType.BROADBLADE:
                return "長刃"
            case WeaponType.PISTOL:
                return "拳銃"
            case WeaponType.GAUNTLET:
                return "手甲"
            case WeaponType.RECTIFIER:
                return "増幅器"
