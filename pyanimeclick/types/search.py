from dataclasses import dataclass
from typing import Optional
from bs4 import Tag

from .misc import Cover

from ..utils import (
    string_to_title_category,
    string_to_title_type,
    find_matching_tag,
    resolve_path,
    get_cover,
    i_pattern,
    url_to_id
)
from ..enums import TitleCategory, TitleType

import re

@dataclass
class QuerySearch:
    query: str
    total: int
    results: list["SearchResult"]

@dataclass
class SearchResult:
    title: str
    url: str
    path: str
    id: int
    year: Optional[int]
    cover: "Cover"
    category: "TitleCategory"
    type: "TitleType"

    @staticmethod
    def _parse(tag: Tag) -> "SearchResult":
        data = {}
        a_tag = tag.find("a")
        img_tag = tag.find("img")
        img_path = img_tag["src"]
        resolved_cover, original_cover = get_cover(img_path)
        _, match = find_matching_tag(
            tag, "li",
            pattern=i_pattern(r"tipo opera:\s*([\w\s]+)")
        )
        data["type"] = string_to_title_type(match.group(1)) \
            if match else TitleType.UNKNOWN
        _, match = find_matching_tag(
            tag, "li",
            pattern=i_pattern(r"anno inizio:\s*(\d{4})")
        )
        data["year"] = int(match.group(1)) if match else None
        _, match = find_matching_tag(
            tag, "li",
            pattern=i_pattern(r"categoria:\s*([\w\s]+)")
        )
        data["category"] = string_to_title_category(match.group(1)) \
            if match else TitleCategory.UNKNOWN
        data["url"] = resolve_path(a_tag["href"])
        data["id"] = url_to_id(data["url"])
        data["path"] = a_tag["href"]
        data["title"] = img_tag["alt"].strip()
        data["cover"] = Cover(resolved_cover, original_cover)

        return SearchResult(**data)