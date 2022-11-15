import httpx
import re
import time

from bs4 import BeautifulSoup
from bs4.element import Tag
from httpx._models import Response
from typing import Optional

from .errors import InvalidCode, RequestError

class AnimeClick:
    BASE_URL = "https://www.animeclick.it"
    TITLE_PAGE = BASE_URL + "/anime/{}/_"
    SEARCH_PAGE = BASE_URL + "/cerca"

    def __init__(self):
        self.session = httpx.AsyncClient(
            header={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            },
            cookies={
                "AC_SCREEN_RESOLUTION": "1920x1080",
                "AC_VIEWPORT_RESOLUTION": "629x588",
                "ac_campaign": "show",
                "device_view": "full",
                "AC_EU_COOKIE_LAW_CONSENT": "Y"
            }, follow_redirects=True
        )

    async def _make_request(self, **kwargs) -> Optional[Response]:
        response = await self.session.request(**kwargs)
        code = response.status_code
        if code != 200:
            raise RequestError(f"[{code}] {response.text}")
        if "AnimeClick.it ....dove sei?!" in response.text:
            raise InvalidCode(f"Il codice inserito non è valido.")
        if "Informazione Pubblicitaria" in response.text:
            raise RequestError("Non sono riuscito a bypassare le pubblicità.")
        return response

    async def search(self, query: str) -> List[Result]:
        response = await self._make_request(
            method="GET", url=self.SEARCH_PAGE,
            params={"name": query}
        )
        soup = BeautifulSoup(response.text, "lxml")
        tab = soup.find("h3", {"id": "type-opera"}).find_next("div")
        operas: tab.find_all("div", {"class": "col-xs-12 col-sm-12 col-md-6 col-lg-4"})
        results = list()
        for opera in operas:
            left = opera.find("div", {"class": "media-left"})
            body = opera.find("div", {"class": "media-body"})
            data = dict()
            data["title"] = body.find("a").text.strip()
            data["url"] = self.BASE_URL + body.find("a")["href"].strip()
            data["id"] = int(body.find("a")["href"].split("/")[-2].strip())
            data["thumb"] = self.BASE_URL + left.find("img")["src"].replace("-thumb-mini", "")
            data["category"] = "-".join(body.find(text=re.compile(r"categoria: (.+)")).strip().lower().split())
            data["type"] = "manga" if body.find(text="tipo opera: Fumetto") else "anime"
            if year := re.search(r"(\d{4})", body.find(text=re.compile("anno inizio:"))):
                data["year"] = int(year.group(1).strip())
            results.append(data)
        return [Result(**result) for result in results]

    async def get_anime(self, id: int) -> Anime:
        r = await self._make_request(
            "GET", ANIME_PAGE.format(id)
        )
        main = BeautifulSoup(r.text, "lxml")
        r = await self._make_request(
            "GET", ANIME_PAGE.format(id) + "/staff"
        )
        staff = BeautifulSoup(r.text, "lxml")
        r = await self._make_request(
            "GET", ANIME_PAGE.format(id) + "/episodi"
        )
        episodes = r.text

        data = dict()
        if title := main.find(text="Titolo inglese"):
            data["title"] = title.find_next("span").text.strip()
        if original_title := main.find(text="Titolo originale"):
            data["original_title"] = original_title.find_next("span").text.strip()
        if short_title := main.find(text="Titolo breve"):
            data["short_title"] = short_title.find_next("span").text.strip()
        if italian_name := main.find("div", {"class": "page-header"}):
            data["italian_name"] = italian_name.find("h1").text
        if year := main.find(text="Anno"):
            data["year"] = int(year.find_next("dd").a.text.strip())
        if genres := main.find(text="Genere"):
            data["genres"] = [
                genre.text.strip()
                for genre in genres.find_next("dd").find_all("a")
            ]
        if overview := main.find("div", {"id": "trama-div"}):
            data["overview"] = overview.text.replace("Trama: ", "").strip()
        if animations := staff.find(text="Animazioni"):
            data["animations"] = [
                studio.a.text for studio in
                animations.find_next(
                    "div", {"class": "well"}
                ).div.find_all("h4", {"class": "media-heading"})
            ]
        durations = [
            int(i) for i
            in re.findall(r"(\d{1,3})\&\#39", episodes)
        ]
        if len(durations) != 0:
            data["average_duration"] = int(sum(durations) // len(durations))
        data["thumb"] = BASE_URL + main.find("img", {"alt": "copertina"})["src"].replace("-thumb-mini", "").replace("-thumb", "")
        return Anime(**data)
    
    async def get_manga(self, id: int) -> Anime:
        r = await self._make_request(
            "GET", MANGA_PAGE.format(str(id))
        )
        main = BeautifulSoup(r.text, "lxml")

        data = dict()
        if title := main.find(text="Titolo inglese"):
            data["title"] = title.find_next("span").text.strip()
        if original_title := main.find(text="Titolo originale"):
            data["original_title"] = original_title.find_next("span").text.strip()
        if short_title := main.find(text="Titolo breve"):
            data["short_title"] = short_title.find_next("span").text.strip()
        if italian_name := main.find("div", {"class": "page-header"}):
            data["italian_name"] = italian_name.find("h1").text
        if year := main.find(text="Anno"):
            data["year"] = int(year.find_next("dd").a.text.strip())
        if genres := main.find(text="Genere"):
            data["genres"] = [
                genre.text.strip()
                for genre in genres.find_next("dd").find_all("a")
            ]
        if nationality := main.find(text="Nazionalità"):
            data["nationality"] = nationality.find_next("span", {"itemprop": "name"}).text.strip()
        if drawings := main.find(text="Disegni"):
            data["drawings"] = [
                getattr(artist.find("a"), "text", None) or artist.text.strip()
                for artist in drawings.find_next("dd").find_all("span", {"itemprop": "name"})
            ]
        if history := main.find(text="Storia"):
            data["history"] = [
                getattr(artist.find("a"), "text", None) or artist.text.strip()
                for artist in history.find_next("dd").find_all("span", {"itemprop": "name"})
            ]
        if category := main.find(text="Categoria"):
            data["category"] = [
                _category.text.strip()
                for _category in category.find_next("dd").find_all("a")
            ]
        if status := main.find(text="Stato in patria"):
            data["status"] = status.find_next("dd").text.strip()
        if overview := main.find("div", {"id": "trama-div"}):
            data["overview"] = overview.text.replace("Trama: ", "").strip()
        data["thumb"] = BASE_URL + main.find("img", {"alt": "copertina"})["src"].replace("-thumb-mini", "").replace("-thumb", "")
        return Manga(**data)
