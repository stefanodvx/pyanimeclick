from bs4 import Tag

from .types import SearchResult, Cover
from .enums import TitleCategory, TitleType
from .utils import (
    find_matchin_tag, 
    resolve_path,
    get_cover,
    url_to_id,
    string_to_title_type,
    string_to_title_category
)

import logging
import re

log = logging.getLogger(__name__)

class Parser:
    def __init__(self):
        pass

    def parse_search_result(self, tag: Tag) -> SearchResult:
        data = {}

        a_tag = tag.find("a")
        img_tag = tag.find("img")
        img_path = img_tag["src"]
        resolved_cover, original_cover = get_cover(img_path)

        # Type
        _, match = find_matchin_tag(
            tag, "li",
            pattern=re.compile(r"tipo opera:\s*([\w\s]+)", flags=re.I)
        )
        data["type"] = string_to_title_type(match.group(1)) \
            if match else TitleType.UNKNOWN
        # Year
        _, match = find_matchin_tag(
            tag, "li",
            pattern=re.compile(r"anno inizio:\s*(\d{4})", flags=re.I)
        )
        data["year"] = int(match.group(1)) if match else None
        # Category
        _, match = find_matchin_tag(
            tag, "li",
            pattern=re.compile(r"categoria:\s*([\w\s]+)", flags=re.I)
        )
        data["category"] = string_to_title_category(match.group(1)) \
            if match else TitleCategory.UNKNOWN
        # URL
        data["url"] = resolve_path(a_tag["href"])
        # ID
        data["id"] = url_to_id(data["url"])
        # Path
        data["path"] = a_tag["href"]
        # Title
        data["title"] = img_tag["alt"].strip()
        # Cover
        data["cover"] = Cover(resolved_cover, original_cover)

        return SearchResult(**data)