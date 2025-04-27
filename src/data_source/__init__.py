from typing import List, Protocol

from src.wuwa.resonator import Resonator


class DataParsingError(Exception):
    pass


class DataSource(Protocol):
    def get_resonators(self) -> List[str]: ...
    def get_resonator_by_name(self, name: str) -> Resonator | None: ...
