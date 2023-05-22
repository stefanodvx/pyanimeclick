from .enums import TitleCategory, TitleType
from .errors import MissingCSRFToken

from bs4 import BeautifulSoup, NavigableString, Tag
from typing import Optional, Union

import re

BASE_URL = "https://www.animeclick.it"

LOGIN_PAGE = BASE_URL + "/aclogin/login"
LOGIN_CHECK_PAGE = BASE_URL + "/login_check"
TITLE_PAGE = BASE_URL + "/anime/{}/_"
SEARCH_PAGE = BASE_URL + "/cerca"

COVER_PATTERN = r"(?P<name>\/.+)(?P<ext>\.\w+)$"
TOKEN_PATTERN = r'name="_csrf_token" value="(?P<token>[^"]+)"'

COOKIES = {
    "AC_SCREEN_RESOLUTION": "1920x1080",
    "AC_VIEWPORT_RESOLUTION": "629x588",
    "ac_campaign": "show",
    "device_view": "full",
    "AC_EU_COOKIE_LAW_CONSENT": "Y"
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"

HEADERS = {
    "user-agent": USER_AGENT
}
LOGIN_HEADERS = {
    "user-agnet": USER_AGENT,
    "authority": "www.animeclick.it",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "it-IT,it;q=0.9,en;q=0.8,en-US;q=0.7,it-AD;q=0.6",
    "origin": "https://www.animeclick.it",
    "referer": "https://www.animeclick.it/",
    "x-requested-with": "XMLHttpRequest",
}

title_type_mapping = {
    "animazione": TitleType.ANIME,
    "fumetto": TitleType.MANGA,
    "novel": TitleType.NOVEL,
    "live action": TitleType.LIVE_ACTION
}

title_category_mapping = {
    "film": TitleCategory.MOVIE,
    "serie tv": TitleCategory.TV,
    "shounen": TitleCategory.SHOUNEN,
    "serie oav": TitleCategory.OAV,
    "light novel": TitleCategory.LIGHT_NOVEL,
    "comics americano": TitleCategory.AMERICAN_COMICS,
    "shoujo": TitleCategory.SHOUJO,
    "romanzo": TitleCategory.ROMANCE,
    "pubblico adulto": TitleCategory.MATURE,
    "boys love": TitleCategory.BOYS_LOVE,
    "hentai": TitleCategory.HENTAI
}

def find_matchin_tag(
    soup: BeautifulSoup,
    name: str,
    pattern: re.Pattern,
    **kwargs
) -> Union[tuple[Union[Tag, NavigableString], Optional[re.Match]], tuple[None, None]]:
    tag = soup.find(name, **kwargs, string=pattern)
    if tag:
        match = pattern.search(tag.string)
        return tag, match
    return None, None

def resolve_path(path: str) -> str:
    return BASE_URL + path

def get_cover(path: str) -> Union[tuple(str, str), tuple(None, None)]:
    def remove_suffix(name: str):
        suffixes = ("-thumb-mini", "-thumb", "-mini")
        for suffix in suffixes:
            if not name.endswith(suffix):
                continue
            return name.rstrip(suffix)
        return name
    match = re.search(COVER_PATTERN, path)
    if not match:
        return None, None
    name, ext = match.groups()
    abs_name = remove_suffix(name)
    hd_cover = resolve_path(abs_name + ext)
    original_cover = resolve_path(path)
    return hd_cover, original_cover

def url_to_id(url: str) -> int:
    # https://www.animeclick.it/live/7430/attack-on-titan-live-action
    splitted_url = url.split("/")
    for part in splitted_url:
        if not part.isdigit():
            continue
        return int(part)

def string_to_title_type(string: str) -> TitleType:
    string = string.lower().strip()
    return title_type_mapping.get(string, TitleType.UNKNOWN)

def string_to_title_category(string: str) -> TitleCategory:
    string = string.lower().strip()
    return title_category_mapping.get(string, TitleCategory.UNKNOWN)

def parse_csrf_token(page: str) -> Optional[str]:
    # name=\"_csrf_token\" value=\"-VMkjKrcNYaR4AHuuEglPVHUsJ1hV8qsC8u3kIoS89I\"
    match = re.search(TOKEN_PATTERN, page.replace("\\", ""))
    if not match:
        raise MissingCSRFToken
    return match.group("token")