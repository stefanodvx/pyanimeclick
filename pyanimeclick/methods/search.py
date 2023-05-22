from ..types import QuerySearch, SearchResult

from ..utils import SEARCH_PAGE

from typing import Optional
from bs4 import BeautifulSoup

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
            params={"name": query}
        )
        results = []
        soup = BeautifulSoup(response.text, "lxml")
        tab = soup.find("h3", {"id": "type-opera"})
        if tab:
            tab_div = tab.find_next("div")
            divs = tab_div.find_all("div", {"class": "col-xs-12 col-sm-12 col-md-6 col-lg-4"})
            for div in divs:
                results.append(SearchResult._parse(div))
        else:
            log.debug("No tab found. Wrong query?")
        return QuerySearch(
            query=query,
            total=len(results),
            results=results
        )