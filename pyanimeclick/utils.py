from bs4 import BeautifulSoup
from .enums import TitleCategory, TitleType

import re

BASE_URL = "https://www.animeclick.it"
TITLE_PAGE = BASE_URL + "/anime/{}/_"
SEARCH_PAGE = BASE_URL + "/cerca"

COVER_PATTERN = r"(?P<name>\/.+)(?P<ext>\.\w+)$"

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
):
    tag = soup.find(name, **kwargs, string=pattern)
    if tag:
        match = pattern.search(tag.string)
        return tag, match
    return None, None

def resolve_path(path: str) -> str:
    return BASE_URL + path

def get_cover(path: str):
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

def string_to_title_type(string: str) -> TitleType:
    string = string.lower().strip()
    return title_type_mapping.get(string, TitleType.UNKNOWN)

def string_to_title_category(string: str) -> TitleCategory:
    string = string.lower().strip()
    return title_category_mapping.get(string, TitleCategory.UNKNOWN)