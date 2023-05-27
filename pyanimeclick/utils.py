from .errors import MissingCSRFToken

from bs4 import BeautifulSoup, NavigableString, Tag
from typing import Optional, Union
from enum import Enum

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

BASE_HEADERS = {
    "user-agent": USER_AGENT,
}

API_HEADERS = BASE_HEADERS | {
    "accept": "application/json",
    "x-requested-with": "XMLHttpRequest",
}

def find_next_tags(
    parent: Tag,
    property: str = None,
    default: object = None,
    *args,
    **kwargs
):
    if not parent:
        return []
    tags = parent.find_all(*args, **kwargs)
    if not tags:
        return []
    return [
        getattr(tag, property, default)
        if property else tag
        for tag in tags
    ]

def find_next_tag(
    parent: Tag,
    property: str = None,
    default: object = None,
    clean: bool = True,
    convert_digits: bool = True,
    sep: Optional[str] = None,
    *args,
    **kwargs
):
    if not parent:
       return default
    next_tag = parent.find_next(*args, **kwargs)
    if not next_tag:
        return default
    if property:
        attr = getattr(next_tag, property, default)
        is_string = isinstance(attr, str)
        # Covert string to int if wanted
        if convert_digits and is_string:
            if attr.isdigit():
                return int(attr)
        # Clean string if wanted
        if clean and property == "string" and is_string:
            attr = clean_str(attr)
        # Split string if wanted
        if sep and is_string:
            attr = attr.split(sep)
        return attr
    else:
        return next_tag

def find_matching_tag(
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

def clean_str(string: str, lower: bool = False) -> str:
    string = string.replace("\xa0", " ") # Broken spaces
    if lower:
        string = string.lower()
    return string.strip()

def i_pattern(pattern: str) -> re.Pattern:
    return re.compile(pattern, flags=re.I)

def resolve_path(path: str) -> str:
    return BASE_URL + path

def get_cover(path: str) -> Union[tuple[str, str], tuple[None, None]]:
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
    
def keep_digits(string: str) -> int:
    string = re.sub(r"[^\d]+", "", string)
    if string.isdigit():
        return int(string)
    return

def parse_year(strings: list[str]) -> Optional[int]:
    if not isinstance(strings, list):
        strings = list(strings)
    return keep_digits(clean_str(strings[0]))

def str_to_enum(string: str, enum: Enum) -> Enum:
    return enum(clean_str(string, lower=True))

def parse_csrf_token(page: str) -> Optional[str]:
    # name=\"_csrf_token\" value=\"-VMkjKrcNYaR4AHuuEglPVHUsJ1hV8qsC8u3kIoS89I\"
    match = re.search(TOKEN_PATTERN, page.replace("\\", ""))
    if not match:
        raise MissingCSRFToken
    return match.group("token")