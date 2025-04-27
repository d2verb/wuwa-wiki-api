import strawberry


@strawberry.type
class Resonator:
    name: str
    attribute: str
    weapon_type: str
