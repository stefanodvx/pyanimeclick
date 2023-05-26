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
    header_title: str
    original_title: str
    english_title: str
    kanji_title: str
    nationality: str

    @staticmethod
    def _parse(page: BeautifulSoup) -> "Title":
        return page
        header_title = page.find("h1", {"itemprop": "name"}).string

        original_title = find_next_tag(
            parent=page.find(string=i_pattern("Titolo originale")),
            property="string", name="span"
        )

        english_title = find_next_tag(
            parent=page.find(string=i_pattern("Titolo inglese")),
            property="string", name="span"
        )

        kanji_title = find_next_tag(
            parent=page.find(string=i_pattern("Titolo kanji")),
            property="string", name="span"
        )

        nationality = find_next_tag(
            parent=page.find(string=i_pattern("Nazionalità")),
            property="string", name="span",
            attrs={"itemprop": "name"}
        )

        data = {
            "header_title": header_title,
            "original_title": original_title,
            "enlighs_title": english_title,
            "kanji_title": kanji_title,
            "nationality": nationality,
        }

        return Title(**data)