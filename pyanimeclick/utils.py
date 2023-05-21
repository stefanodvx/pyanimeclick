from bs4 import BeautifulSoup

import re

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
