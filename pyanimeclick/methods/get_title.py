from ..types import Title

from ..utils import BASE_HEADERS, TITLE_PAGE

from typing import Optional
from bs4 import BeautifulSoup

import pyanimeclick
import logging

log = logging.getLogger(__name__)

class GetTitle:
    async def get_title(
        self: "pyanimeclick.AnimeClick",
        id: int
    ) -> Optional["Title"]:
        response = await self._make_request(
            method="GET",
            url=TITLE_PAGE.format(str(id)),
            headers=BASE_HEADERS,
        )
        soup = BeautifulSoup(response.text, "lxml")
        return Title._parse(soup)