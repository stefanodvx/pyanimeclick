from bs4 import BeautifulSoup
from httpx._models import Response
from typing import Optional

from .types import SearchResult
from .errors import InvalidCode, RequestError
from .parser import Parser

from .utils import SEARCH_PAGE

import logging
import httpx

class AnimeClick:
    def __init__(self):
        self.session = httpx.AsyncClient(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            },
            cookies={
                "AC_SCREEN_RESOLUTION": "1920x1080",
                "AC_VIEWPORT_RESOLUTION": "629x588",
                "ac_campaign": "show",
                "device_view": "full",
                "AC_EU_COOKIE_LAW_CONSENT": "Y"
            }, follow_redirects=True, timeout=10
        )
        self.logger = logging.getLogger("pyanimeclick.main")
        self.parser = Parser()

    async def _make_request(self, **kwargs) -> Optional[Response]:
        response = await self.session.request(**kwargs)
        code = response.status_code

        if code != 200:
            raise RequestError(f"[{code}] Response: {response.text}")
        
        if "AnimeClick.it ....dove sei?!" in response.text:
            raise InvalidCode("You inserted a wrong code. Try again with a different one.")
        
        if "Informazione Pubblicitaria" in response.text:
            raise RequestError("Couldn't bypass ADs. If this error persists, open an issue on GitHub.")
        
        return response

    async def search(self, query: str) -> Optional[list[SearchResult]]:
        response = await self._make_request(
            method="GET", url=SEARCH_PAGE,
            params={"name": query}
        )
        results = []

        soup = BeautifulSoup(response.text, "lxml")
        tab = soup.find("h3", {"id": "type-opera"}).find_next("div")
        divs = tab.find_all("div", {"class": "col-xs-12 col-sm-12 col-md-6 col-lg-4"})

        for div in divs:
            result = self.parser.parse_search_result(div)
            results.append(result)

        return results

    # async def get_anime(self, id: int):
    #     r = await self._make_request(
    #         "GET", ANIME_PAGE.format(id)
    #     )
    #     main = BeautifulSoup(r.text, "lxml")
    #     r = await self._make_request(
    #         "GET", ANIME_PAGE.format(id) + "/staff"
    #     )
    #     staff = BeautifulSoup(r.text, "lxml")
    #     r = await self._make_request(
    #         "GET", ANIME_PAGE.format(id) + "/episodi"
    #     )
    #     episodes = r.text

    #     data = dict()
    #     if title := main.find(text="Titolo inglese"):
    #         data["title"] = title.find_next("span").text.strip()
    #     if original_title := main.find(text="Titolo originale"):
    #         data["original_title"] = original_title.find_next("span").text.strip()
    #     if short_title := main.find(text="Titolo breve"):
    #         data["short_title"] = short_title.find_next("span").text.strip()
    #     if italian_name := main.find("div", {"class": "page-header"}):
    #         data["italian_name"] = italian_name.find("h1").text
    #     if year := main.find(text="Anno"):
    #         data["year"] = int(year.find_next("dd").a.text.strip())
    #     if genres := main.find(text="Genere"):
    #         data["genres"] = [
    #             genre.text.strip()
    #             for genre in genres.find_next("dd").find_all("a")
    #         ]
    #     if overview := main.find("div", {"id": "trama-div"}):
    #         data["overview"] = overview.text.replace("Trama: ", "").strip()
    #     if animations := staff.find(text="Animazioni"):
    #         data["animations"] = [
    #             studio.a.text for studio in
    #             animations.find_next(
    #                 "div", {"class": "well"}
    #             ).div.find_all("h4", {"class": "media-heading"})
    #         ]
    #     durations = [
    #         int(i) for i
    #         in re.findall(r"(\d{1,3})\&\#39", episodes)
    #     ]
    #     if len(durations) != 0:
    #         data["average_duration"] = int(sum(durations) // len(durations))
    #     data["thumb"] = BASE_URL + main.find("img", {"alt": "copertina"})["src"].replace("-thumb-mini", "").replace("-thumb", "")
    #     return Anime(**data)
    
    # async def get_manga(self, id: int):
    #     r = await self._make_request(
    #         "GET", MANGA_PAGE.format(str(id))
    #     )
    #     main = BeautifulSoup(r.text, "lxml")

    #     data = dict()
    #     if title := main.find(text="Titolo inglese"):
    #         data["title"] = title.find_next("span").text.strip()
    #     if original_title := main.find(text="Titolo originale"):
    #         data["original_title"] = original_title.find_next("span").text.strip()
    #     if short_title := main.find(text="Titolo breve"):
    #         data["short_title"] = short_title.find_next("span").text.strip()
    #     if italian_name := main.find("div", {"class": "page-header"}):
    #         data["italian_name"] = italian_name.find("h1").text
    #     if year := main.find(text="Anno"):
    #         data["year"] = int(year.find_next("dd").a.text.strip())
    #     if genres := main.find(text="Genere"):
    #         data["genres"] = [
    #             genre.text.strip()
    #             for genre in genres.find_next("dd").find_all("a")
    #         ]
    #     if nationality := main.find(text="Nazionalità"):
    #         data["nationality"] = nationality.find_next("span", {"itemprop": "name"}).text.strip()
    #     if drawings := main.find(text="Disegni"):
    #         data["drawings"] = [
    #             getattr(artist.find("a"), "text", None) or artist.text.strip()
    #             for artist in drawings.find_next("dd").find_all("span", {"itemprop": "name"})
    #         ]
    #     if history := main.find(text="Storia"):
    #         data["history"] = [
    #             getattr(artist.find("a"), "text", None) or artist.text.strip()
    #             for artist in history.find_next("dd").find_all("span", {"itemprop": "name"})
    #         ]
    #     if category := main.find(text="Categoria"):
    #         data["category"] = [
    #             _category.text.strip()
    #             for _category in category.find_next("dd").find_all("a")
    #         ]
    #     if status := main.find(text="Stato in patria"):
    #         data["status"] = status.find_next("dd").text.strip()
    #     if overview := main.find("div", {"id": "trama-div"}):
    #         data["overview"] = overview.text.replace("Trama: ", "").strip()
    #     data["thumb"] = BASE_URL + main.find("img", {"alt": "copertina"})["src"].replace("-thumb-mini", "").replace("-thumb", "")
    #     return Manga(**data)
