from enum import Enum, auto


class DubStatus(Enum):
    UNLICENSED = "doppiaggio inedito"
    UNKNOWN = auto()

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN
    
class SubStatus(Enum):
    UNLICENSED = "sottotitoli inedito"
    UNKNOWN = auto()

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN

class Nationality(Enum):
    JAPAN = "giappone"
    UNKNOWN = auto()

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN
    
class Status(Enum):
    AIRING = "in corso"
    PAUSED = "in pausa"
    COMPLETED = "completato"
    UNKNOWN = auto()

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN

class TitleType(Enum):
    ANIME = "animazione"
    MANGA = "fumetto"
    NOVEL = "novel"
    LIVE_ACTION = "live action"
    UNKNOWN = auto()

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN

class TitleCategory(Enum):
    MOVIE = "film"
    TV = "serie tv"
    SHOUNEN = "shounen"
    OAV = "serie oav"
    LIGHT_NOVEL = "light novel"
    ROMANCE = "romanzo"
    AMERICAN_COMICS = "comics americano"
    BOYS_LOVE = "boys love"
    SHOUJO = "shoujo"
    MATURE = "pubblico adulto"
    HENTAI = "hentai"
    UNKNOWN = auto()

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN