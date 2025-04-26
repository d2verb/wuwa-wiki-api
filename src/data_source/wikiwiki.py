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

    def get_resonator_by_name(self, name: str) -> Resonator | None:
        url = f"{self.BASE_URL}::cmd/source"
        r = httpx.get(
            url,
            params={"page": name},
            headers={"User-Agent": self.USER_AGENT},
        )

        if r.status_code == httpx.codes.NOT_FOUND:
            return None

        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        wikitext = soup.select_one("#source > code").text

        weapon_type = None
        attribute = None

        for line in wikitext.splitlines():
            # attribute
            m = re.search(r"\|[^|]*\|属性\|[^;]*;([^|]+)\|?", line)
            if m:
                attribute = Attribute.from_ja(m.group(1).strip())

            # weapon type
            m = re.search(r"\|~\|武器\|[^;]*;([^|]+)\|?", line)
            if m:
                weapon_type = WeaponType.from_ja(m.group(1).strip())

        if weapon_type is None or attribute is None:
            raise DataParsingError(f"Failed to parse resonator data for {name}")

        return Resonator(name=name, weapon_type=weapon_type, attribute=attribute)
