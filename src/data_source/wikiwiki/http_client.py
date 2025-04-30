import httpx
from bs4 import BeautifulSoup
from typing import Protocol


class HttpClient(Protocol):
    def get_page_source(self, page_title: str) -> str | None: ...


class WikiWikiHttpClient:
    BASE_URL = "https://wikiwiki.jp/w-w/"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def get_page_source(self, page_title: str) -> str | None:
        url = f"{self.BASE_URL}::cmd/source"
        r = httpx.get(
            url,
            params={"page": page_title},
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
