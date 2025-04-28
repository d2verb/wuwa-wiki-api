from src.data_source.wikiwiki import WikiWikiDataSource
from src.api.objects import Echo
from typing import List


class EchoResolver:
    def echoes(self) -> List[str]:
        ds = WikiWikiDataSource()
        return ds.get_echoes()

    def echo(self, name: str) -> Echo:
        ds = WikiWikiDataSource()
        echo = ds.get_echo_by_name(name)

        if echo is None:
            return None

        return Echo(
            name=echo.name,
            attribute=echo.attribute.value,
            enemy_class=echo.enemy_class.value,
            description=echo.description,
        )
