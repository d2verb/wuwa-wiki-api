from typing import List, Protocol

from src.wuwa.archive import Archive
from src.wuwa.echo import Echo
from src.wuwa.resonator import Resonator


class DataParsingError(Exception):
    pass


class DataNotFound(Exception):
    pass


class DataSource(Protocol):
    def get_archives(self) -> List[str]: ...
    def get_archive_by_title(self, title: str) -> Archive | None: ...
    def get_echoes(self) -> List[str]: ...
    def get_echo_by_name(self, name: str) -> Echo | None: ...
    def get_resonators(self) -> List[str]: ...
    def get_resonator_by_name(self, name: str) -> Resonator | None: ...
