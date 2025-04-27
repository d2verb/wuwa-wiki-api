from src.wuwa.resonator import Resonator
from src.wuwa.attribute import Attribute
from src.wuwa.weapon_type import WeaponType
from src.data_source import DataParsingError
from bs4 import BeautifulSoup
import re
import httpx


class WikiWikiDataSource:
    BASE_URL = "https://wikiwiki.jp/w-w/"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def get_resonator_by_name(self, name: str) -> Resonator:
        weapon_type = None
        attribute = None

        # parse character page
        wikitext = self._get_page_source(name)
        if wikitext is None:
            raise DataParsingError(f"Failed to get resonator data for {name}")

        for line in wikitext.splitlines():
            weapon_type = (
                self._parse_weapon_type(line) if weapon_type is None else weapon_type
            )
            attribute = self._parse_attribute(line) if attribute is None else attribute

        if not all([weapon_type, attribute]):
            raise DataParsingError(f"Failed to parse resonator data for {name}")

        return Resonator(name=name, weapon_type=weapon_type, attribute=attribute)

    def _get_page_source(self, page: str) -> str | None:
        url = f"{self.BASE_URL}::cmd/source"
        r = httpx.get(
            url,
            params={"page": page},
            headers={"User-Agent": self.USER_AGENT},
        )

        if r.status_code == httpx.codes.NOT_FOUND:
            return None

        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        wikitext = soup.select_one("#source > code").text

        return wikitext

    def _parse_attribute(self, line: str) -> Attribute | None:
        m = re.search(r"\|[^|]*\|属性\|[^;]*;([^|]+)\|?", line)
        if m:
            return Attribute(m.group(1).strip())
        return None

    def _parse_weapon_type(self, line: str) -> WeaponType | None:
        m = re.search(r"\|~\|武器\|[^;]*;([^|]+)\|?", line)
        if m:
            return WeaponType(m.group(1).strip())
        return None
