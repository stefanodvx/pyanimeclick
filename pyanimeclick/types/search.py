from dataclasses import dataclass
from typing import Optional

from .misc import Cover

from ..utils import (
    string_to_enum,
    resolve_path,
    get_cover,
)

from ..enums import TitleCategory, TitleType

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
    year: int
    cover: "Cover"
    category: list["TitleCategory"]
    type: "TitleType"

    @staticmethod
    def _parse(result: dict) -> "SearchResult":
        cover_path = result["image_url"]
        resolved_cover, original_cover = get_cover(cover_path)
        cover_object = Cover(resolved_cover, original_cover)

        title = result["name"]
        title_id = int(result["id"])
        title_path = result["url"]
        title_url = resolve_path(title_path)

        title_type = string_to_enum(
            result["payload"]["tipo_opera"],
            enum=TitleType
        )
        title_category = [
            string_to_enum(part, enum=TitleCategory)
            for part in result["payload"]["categoria"].split(",")
        ]
        title_year = int(result["payload"]["anno_inizio"])

        data = {
            "title": title,
            "url": title_url,
            "path": title_path,
            "id": title_id,
            "year": title_year,
            "cover": cover_object,
            "category": title_category,
            "type": title_type
        }

        return SearchResult(**data)

    # @staticmethod
    # def _parse(tag: Tag) -> "SearchResult":
    #     data = {}
    #     a_tag = tag.find("a")
    #     img_tag = tag.find("img")
    #     img_path = img_tag["src"]
    #     resolved_cover, original_cover = get_cover(img_path)
    #     _, match = find_matching_tag(
    #         tag, "li",
    #         pattern=i_pattern(r"tipo opera:\s*([\w\s]+)")
    #     )
    #     data["type"] = string_to_title_type(match.group(1)) \
    #         if match else TitleType.UNKNOWN
    #     _, match = find_matching_tag(
    #         tag, "li",
    #         pattern=i_pattern(r"anno inizio:\s*(\d{4})")
    #     )
    #     data["year"] = int(match.group(1)) if match else None
    #     _, match = find_matching_tag(
    #         tag, "li",
    #         pattern=i_pattern(r"categoria:\s*([\w\s]+)")
    #     )
    #     data["category"] = string_to_title_category(match.group(1)) \
    #         if match else TitleCategory.UNKNOWN
    #     data["url"] = resolve_path(a_tag["href"])
    #     data["id"] = url_to_id(data["url"])
    #     data["path"] = a_tag["href"]
    #     data["title"] = img_tag["alt"].strip()
    #     data["cover"] = Cover(resolved_cover, original_cover)

    #     return SearchResult(**data)