from bs4 import BeautifulSoup

import re

def find_matchin_tag(
    soup: BeautifulSoup,
    name: str,
    pattern: str,
    **kwargs
):
    compiled_pattern = re.compile(pattern)
    tag = soup.find(name, **kwargs, string=compiled_pattern)
    if tag:
        match = compiled_pattern.search(tag.string)
        return tag, match
    return None, None
