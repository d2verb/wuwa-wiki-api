from typing import List

import strawberry

from src.api.objects import Resonator, ResonatorStory
from src.data_source import DataSource


class ResonatorResolver:
    def resonators(self, info: strawberry.Info) -> List[str]:
        ds: DataSource = info.context["data_source"]
        return ds.get_resonators()

    def resonator(self, name: str, info: strawberry.Info) -> Resonator | None:
        ds: DataSource = info.context["data_source"]
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
