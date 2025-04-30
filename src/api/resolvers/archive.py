from typing import List

import strawberry

from src.api.objects import Archive
from src.data_source import DataSource


class ArchiveResolver:
    def archives(self, info: strawberry.Info) -> List[str]:
        ds: DataSource = info.context["data_source"]
        return ds.get_archives()

    def archive(self, title: str, info: strawberry.Info) -> Archive | None:
        ds: DataSource = info.context["data_source"]
        archive = ds.get_archive_by_title(title)

        if archive is None:
            return None

        return Archive(title=archive.title, content=archive.content)
