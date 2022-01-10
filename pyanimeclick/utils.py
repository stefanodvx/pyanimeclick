from typing import Dict

BASE_URL = "https://www.animeclick.it"
MANGA_PAGE = "https://www.animeclick.it/manga/{}/evangelionislife"
ANIME_PAGE = "https://www.animeclick.it/manga/{}/darkisgay"
SEARCH_PAGE = "https://www.animeclick.it/cerca"

def headers() -> Dict:
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    }

def cookies() -> Dict:
    return {
        "AC_SCREEN_RESOLUTION": "1920x1080",
        "AC_VIEWPORT_RESOLUTION": "629x588",
        "ac_campaign": "show",
        "device_view": "full",
        "AC_EU_COOKIE_LAW_CONSENT": "Y"
    }