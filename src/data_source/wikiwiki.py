from src.wuwa.resonator import Resonator
from src.wuwa.attribute import Attribute
from src.wuwa.weapon_type import WeaponType
from src.wuwa.nation import Nation
from src.data_source import DataParsingError
from src.wuwa.resonator import ResonatorStory
from typing import List
from bs4 import BeautifulSoup
import re
import httpx


class WikiWikiDataSource:
    BASE_URL = "https://wikiwiki.jp/w-w/"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def get_resonators(self) -> List[str]:
        wikitext = self._get_page_source("共鳴者一覧")
        if wikitext is None:
            raise DataParsingError("Failed to get resonator list")

        return self._parse_resonators(wikitext)

    def _parse_resonators(self, wikitext: str) -> List[str]:
        resonators = []

        for line in wikitext.splitlines():
            m = re.search(r"\|\[?\[?&ref[^>]*>([^\]]+)\]", line)
            if m:
                resonators.append(m.group(1).strip())

        return resonators

    def get_resonator_by_name(self, name: str) -> Resonator:
        weapon_type: WeaponType | None = None
        attribute: Attribute | None = None
        nation: Nation | None = None
        stories: List[ResonatorStory] | None = None

        # parse character page
        wikitext = self._get_page_source(name)
        if wikitext is None:
            raise DataParsingError(f"Failed to get resonator data for {name}")

        for line in wikitext.splitlines():
            weapon_type = (
                self._parse_weapon_type(line) if weapon_type is None else weapon_type
            )
            attribute = self._parse_attribute(line) if attribute is None else attribute
            nation = self._parse_nation(line) if nation is None else nation

        # parse character profile page
        wikitext = self._get_page_source(f"{name}/プロフィール")
        if wikitext is None:
            raise DataParsingError(f"Failed to get resonator profile for {name}")

        # parse story
        stories = self._parse_stories(wikitext)

        # we can use all() here, but pyright can't narrow down the type if we do so
        if (
            weapon_type is None
            or attribute is None
            or nation is None
            or stories is None
        ):
            raise DataParsingError(f"Failed to parse resonator data for {name}")

        return Resonator(
            name=name,
            weapon_type=weapon_type,
            attribute=attribute,
            nation=nation,
            stories=stories,
        )

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
        el = soup.select_one("#source > code")

        if el is None:
            return None

        return el.text

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

    def _parse_nation(self, line: str) -> Nation | None:
        m = re.search(r"\|~\|出身\|([^|]+)\|?", line)
        if m:
            return Nation(m.group(1).strip())
        return None

    def _parse_stories(self, wikitext: str) -> List[ResonatorStory] | None:
        m = re.search(r"\*\*\*ストーリー \[#Story\](.*?)\*\*\*", wikitext, re.DOTALL)
        if not m:
            return None

        story_text = m.group(1)
        story_sections = re.findall(
            r"&size\(14\)\{&#\d{5}; ''(.*?)''\};\s*(.*?)(?=(?:&size\(14\)\{&#\d{5};|----|\Z))",
            story_text,
            re.DOTALL,
        )

        stories: List[ResonatorStory] = []
        for title, content in story_sections:
            stories.append(ResonatorStory(title=title, content=content))

        return stories
