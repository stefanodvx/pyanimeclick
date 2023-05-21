from dataclasses import dataclass
from typing import Optional

from .misc import Cover
from .obj import Object

from ..enums import TitleCategory, TitleType

@dataclass
class QuerySearch(Object):
    query: str
    total: int
    results: list["SearchResult"]

@dataclass
class SearchResult(Object):
    title: str
    url: str
    path: str
    id: int
    year: Optional[int]
    cover: "Cover"
    category: "TitleCategory"
    type: "TitleType"