from typing import Dict, List
from pydantic import BaseModel, Field

class Result(BaseModel):
    title: str = Field(default=None)
    url:   str = Field(default=None)
    id:    int = Field(default=None)
    thumb: str = Field(default=None)
    type:  str = Field(default=None)
    year:  int = Field(default=None)

class Anime(BaseModel):
    title:            str = Field(default=None)
    original_title:   str = Field(default=None)
    short_title:      str = Field(default=None)
    italian_name:     str = Field(default=None)
    year:             int = Field(default=None)
    thumb:            str = Field(default=None)
    overview:         str = Field(default=None)
    average_duration: int = Field(default=None)
    animations:       List[str] = Field(default=[])
    genres:           List[str] = Field(default=[])

class Manga(BaseModel):
    title:          str = Field(default=None)
    original_title: str = Field(default=None)
    short_title:    str = Field(default=None)
    italian_name:   str = Field(default=None)
    year:           int = Field(default=None)
    thumb:          str = Field(default=None)
    overview:       str = Field(default=None)
    genres:         List[str] = Field(default=[])
