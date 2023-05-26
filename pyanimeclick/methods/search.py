from pyanimeclick.types import QuerySearch, SearchResult
from pyanimeclick.utils import API_HEADERS, SEARCH_PAGE

from typing import Optional

import pyanimeclick
import logging

log = logging.getLogger(__name__)

class Search:
    async def search(
        self: "pyanimeclick.AnimeClick",
        query: str
    ) -> Optional["QuerySearch"]:
        
        log.debug(f"Query string: {query}")
        response = await self._make_request(
            method="GET", url=SEARCH_PAGE,
            params={"name": query, "type": "opera"},
            headers=API_HEADERS,
        )
        
        results = []
        json_response = response.json()
        for result in json_response["categories"][0]["items"]:
            results.append(SearchResult._parse(result))

        return QuerySearch(
            query=query,
            total=len(results),
            results=results
        )