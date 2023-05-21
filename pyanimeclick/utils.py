from bs4 import BeautifulSoup

import re

BASE_URL = "https://www.animeclick.it"
TITLE_PAGE = BASE_URL + "/anime/{}/_"
SEARCH_PAGE = BASE_URL + "/cerca"

COVER_PATTERN = r"(?P<name>\/.+)(?P<ext>\.\w+)$"

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

def resolve_path(path: str):
    return BASE_URL + path

def get_cover(path: str):
    match = re.search(COVER_PATTERN, path)
    if not match:
        return None
    name, ext = match.groups()
    for suffix in ("-thumb-mini", "-thumb", "-mini"):
        abs_name = name.rstrip(suffix)
    hd_cover = resolve_path(abs_name + ext)
    original_cover = resolve_path(path)
    return hd_cover, original_cover