from typing import Dict

version = "1.0"

BASE_URL = "https://www.animeclick.it"
MANGA_PAGE = "https://www.animeclick.it/manga/{}/evangelionislife"
ANIME_PAGE = "https://www.animeclick.it/manga/{}/darkisgay"
SEARCH_PAGE = "https://www.animeclick.it/cerca"

def headers() -> Dict:
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    }

def cookies() -> Dict:
    return {"ac_campaign": "show"}