from bs4 import BeautifulSoup

import re

BASE_URL = "https://www.animeclick.it"
TITLE_PAGE = BASE_URL + "/anime/{}/_"
SEARCH_PAGE = BASE_URL + "/cerca"

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