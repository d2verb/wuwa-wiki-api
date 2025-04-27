from src.api.objects import Resonator, ResonatorStory
from src.data_source.wikiwiki import WikiWikiDataSource
from typing import List


class ResonatorResolver:
    def resonators(self) -> List[str]:
        ds = WikiWikiDataSource()
        return ds.get_resonators()

    def resonator(self, name: str) -> Resonator | None:
        ds = WikiWikiDataSource()
        resonator = ds.get_resonator_by_name(name)

        if resonator is None:
            return None

        return Resonator(
            name=resonator.name,
            attribute=resonator.attribute.value,
            weapon_type=resonator.weapon_type.value,
            nation=resonator.nation.value,
            stories=[
                ResonatorStory(title=s["title"], content=s["content"])
                for s in resonator.stories
            ],
        )
