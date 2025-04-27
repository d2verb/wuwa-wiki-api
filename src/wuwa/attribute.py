from enum import Enum


class Attribute(str, Enum):
    FUSION = "焦熱"
    GLACIO = "凝縮"
    AERO = "気動"
    ELECTRO = "電導"
    SPECTRO = "回折"
    HAVOC = "消滅"
