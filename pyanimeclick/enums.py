from enum import Enum, auto

class TitleType(Enum):
    ANIME = auto()
    MANGA = auto()
    NOVEL = auto()
    LIVE_ACTION = auto()
    UNKNOWN = auto()

class TitleCategory(Enum):
    FILM = auto()
    TV = auto()
    SHOUNEN = auto()
    OAV = auto()
    LIGHT_NOVEL = auto()
    ROMANCE = auto()
    AMERICAN_COMICS = auto()
    SHOUJO = auto()
    UNKNOWN = auto()