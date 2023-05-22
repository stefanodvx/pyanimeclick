class AnimeClickError(Exception):
    pass

class InvalidCode(AnimeClickError):
    pass

class RequestError(AnimeClickError):
    pass

class MissingCSRFToken(AnimeClickError):
    pass