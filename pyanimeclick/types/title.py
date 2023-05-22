from dataclasses import dataclass
from typing import Optional
from bs4 import BeautifulSoup

from .misc import Cover

from ..utils import (
    string_to_title_category,
    string_to_title_type,
    find_matching_tag,
    resolve_path,
    get_cover,
    url_to_id,
    find_next_tag,
    i_pattern
)
from ..enums import TitleCategory, TitleType

import re

@dataclass
class Title:
    original_title: str
    english_title: str
    kanji_title: str

    @staticmethod
    def _parse(page: BeautifulSoup) -> "Title":
        data = {}
        
        data["original_title"] = find_next_tag(
            parent=page.find(string=i_pattern("Titolo originale")),
            property="string", name="span"
        )

        data["english_title"] = find_next_tag(
            parent=page.find(string=i_pattern("Titolo inglese")),
            property="string", name="span"
        )

        data["kanji_title"] = find_next_tag(
            parent=page.find(string=i_pattern("Titolo kanji")),
            property="string", name="span"
        )

        return Title(**data)