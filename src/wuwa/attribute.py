from enum import Enum


class Attribute(str, Enum):
    FUSION = "fusion"
    GLACIO = "glacio"
    AERO = "aero"
    ELECTRO = "electro"
    SPECTRO = "spectro"
    HAVOC = "havoc"

    @classmethod
    def from_ja(cls, ja: str) -> "Attribute":
        match ja:
            case "焦熱":
                return cls.FUSION
            case "凝縮":
                return cls.GLACIO
            case "気動":
                return cls.AERO
            case "電導":
                return cls.ELECTRO
            case "回折":
                return cls.SPECTRO
            case "消滅":
                return cls.HAVOC
            case _:
                raise ValueError(f"Invalid attribute: {ja}")

    def to_ja(self) -> str:
        match self:
            case Attribute.FUSION:
                return "焦熱"
            case Attribute.GLACIO:
                return "凝縮"
            case Attribute.AERO:
                return "気動"
            case Attribute.ELECTRO:
                return "電導"
            case Attribute.SPECTRO:
                return "回折"
            case Attribute.HAVOC:
                return "消滅"
