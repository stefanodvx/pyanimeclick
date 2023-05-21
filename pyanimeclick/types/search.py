from dataclasses import dataclass

@dataclass
class SearchResult:
    title: str
    url: str
    id: int
    year: int
    category: str
    thumb: str
    type: str