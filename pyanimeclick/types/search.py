from dataclasses import dataclass
from typing import Optional

from .misc import Cover

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
    year: Optional[int]
    cover: "Cover"
    category: "TitleCategory"
    type: "TitleType"