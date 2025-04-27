from src.api.objects import Resonator
from src.data_source.wikiwiki import WikiWikiDataSource


class ResonatorResolver:
    def resonator(self, name: str) -> Resonator | None:
        ds = WikiWikiDataSource()
        resonator = ds.get_resonator_by_name(name)

        if resonator is None:
            return None

        return Resonator(
            name=resonator.name,
            attribute=resonator.attribute.to_ja(),
            weapon_type=resonator.weapon_type.to_ja(),
        )
