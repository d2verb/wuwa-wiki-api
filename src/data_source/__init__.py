from typing import List, Protocol

from src.wuwa.resonator import Resonator
from src.wuwa.echo import Echo


class DataParsingError(Exception):
    pass


class DataSource(Protocol):
    def get_echoes(self) -> List[str]: ...
    def get_echo_by_name(self, name: str) -> Echo | None: ...
    def get_resonators(self) -> List[str]: ...
    def get_resonator_by_name(self, name: str) -> Resonator | None: ...
