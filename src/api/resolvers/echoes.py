from typing import List

import strawberry

from src.api.objects import Echo
from src.data_source import DataSource


class EchoResolver:
    def echoes(self, info: strawberry.Info) -> List[str]:
        ds: DataSource = info.context["data_source"]
        return ds.get_echoes()

    def echo(self, name: str, info: strawberry.Info) -> Echo | None:
        ds: DataSource = info.context["data_source"]
        echo = ds.get_echo_by_name(name)

        if echo is None:
            return None

        return Echo(
            name=echo.name,
            attribute=echo.attribute.value,
            enemy_class=echo.enemy_class.value,
            description=echo.description,
        )
