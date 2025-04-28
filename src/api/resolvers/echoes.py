from src.data_source.wikiwiki import WikiWikiDataSource
from typing import List


class EchoResolver:
    def echoes(self) -> List[str]:
        ds = WikiWikiDataSource()
        return ds.get_echoes()
