import re
import html
from typing import List

from src.data_source import DataParsingError, DataNotFound
from src.wuwa.archive import Archive
from src.wuwa.attribute import Attribute
from src.wuwa.echo import Echo
from src.wuwa.enemy_class import EnemyClass
from src.wuwa.nation import Nation
from src.wuwa.resonator import Resonator, ResonatorStory
from src.wuwa.weapon_type import WeaponType

from src.data_source.wikiwiki.http_client import HttpClient, WikiWikiHttpClient


class WikiWikiDataSource:
    client: HttpClient

    def __init__(self, client: HttpClient = WikiWikiHttpClient()) -> None:
        self.client = client

    def get_archives(self) -> List[str]:
        wikitext = self.client.get_page_source("ソラリス辞典")
        if wikitext is None:
            raise DataNotFound("Failed to get archive list")
        return self._parse_archives(wikitext)

    def _parse_archives(self, wikitext: str) -> List[str]:
        archives = []
        for line in wikitext.splitlines():
            m = re.search(r"\*\*([^\[]+)\[", line)
            if m:
                archives.append(m.group(1).strip())
        return archives

    def get_archive_by_title(self, title: str) -> Archive | None:
        wikitext = self.client.get_page_source("ソラリス辞典")
        if wikitext is None:
            raise DataNotFound(f"Failed to get archive data for {title}")

        archive = self._parse_archive(wikitext, title)
        if archive is None:
            raise DataParsingError(f"Failed to parse archive data for {title}")

        return archive

    def _parse_archive(self, wikitext: str, title: str) -> Archive | None:
        is_parsing = False
        lines = []

        for line in wikitext.splitlines():
            if not is_parsing and line.startswith(f"**{title}"):
                is_parsing = True
                continue

            if is_parsing and line.startswith("**"):
                is_parsing = False
                break

            if is_parsing:
                lines.append(line)

        if len(lines) == 0:
            return None

        return Archive(title=title, content="\n".join(lines))

    def get_echoes(self) -> List[str]:
        wikitext = self.client.get_page_source("音骸一覧")
        if wikitext is None:
            raise DataNotFound("Failed to get echo list")

        return self._parse_echoes(wikitext)

    def _parse_echoes(self, wikitext: str) -> List[str]:
        echoes = []
        for line in wikitext.splitlines():
            m = re.search(r";\|\[\[([^\]]+)\]\]\|\d", line)
            if m:
                echoes.append(m.group(1).strip())
        return echoes

    def get_echo_by_name(self, name: str) -> Echo | None:
        attribute: Attribute | None = None
        enemy_class: EnemyClass | None = None
        description: str | None = None

        wikitext = self.client.get_page_source(name)
        if wikitext is None:
            raise DataNotFound(f"Failed to get echo data for {name}")

        for line in wikitext.splitlines():
            attribute = self._parse_attribute(line) if attribute is None else attribute
            enemy_class = (
                self._parse_enemy_class(line) if enemy_class is None else enemy_class
            )

        description = self._parse_echo_description(wikitext)

        if attribute is None or enemy_class is None or description is None:
            raise DataParsingError(f"Failed to parse echo data for {name}")

        return Echo(
            name=name,
            attribute=attribute,
            enemy_class=enemy_class,
            description=description,
        )

    def _parse_enemy_class(self, line: str) -> EnemyClass | None:
        m = re.search(r"\|~\|クラス\|([^|]+)\|?", line)
        if m:
            return EnemyClass(m.group(1).strip())
        return None

    def _parse_echo_description(self, wikitext: str) -> str | None:
        m = re.search(
            r"ソラガイド発見済テキスト\s*\n([\s\S]*?)\n\}\}", wikitext, re.DOTALL
        )
        if m:
            return m.group(1).strip()
        return None

    def get_resonators(self) -> List[str]:
        wikitext = self.client.get_page_source("共鳴者一覧")
        if wikitext is None:
            raise DataNotFound("Failed to get resonator list")

        return self._parse_resonators(wikitext)

    def _parse_resonators(self, wikitext: str) -> List[str]:
        resonators = []

        is_parsing = False

        for line in wikitext.splitlines():
            if line.startswith("*共鳴者一覧"):
                is_parsing = True
                continue

            if is_parsing and line.startswith("}}"):
                is_parsing = False
                break

            if not is_parsing:
                continue

            m = re.search(
                r"^\|\[?\[?&ref[^\|]*?\|\[?\[?([^>]*?>)?([^\]]*?)\]?\]?\|", line
            )
            if not m:
                continue

            candidate = m.group(2).strip()
            resonators.append(candidate)

        return resonators

    def get_resonator_by_name(self, name: str) -> Resonator:
        weapon_type: WeaponType | None = None
        attribute: Attribute | None = None
        nation: Nation | None = None
        stories: List[ResonatorStory] | None = None

        # parse character page
        wikitext = self.client.get_page_source(name)
        if wikitext is None:
            raise DataNotFound(f"Failed to get resonator data for {name}")

        for line in wikitext.splitlines():
            weapon_type = (
                self._parse_weapon_type(line) if weapon_type is None else weapon_type
            )
            attribute = self._parse_attribute(line) if attribute is None else attribute
            nation = self._parse_nation(line) if nation is None else nation

        # parse character profile page
        wikitext = self.client.get_page_source(f"{name}/プロフィール")
        if wikitext is None:
            raise DataNotFound(f"Failed to get resonator profile for {name}")

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
            nation = html.unescape(m.group(1).strip())
            nation = (
                "瑝瓏" if nation == "瑝龍" else nation
            )  # "瑝龍" is a wrong word. wuwa uses "瑝瓏" in the game.
            return Nation(nation)
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
