from bs4 import Tag

from .types import SearchResult

import logging
import re

class Parser:
    def __init__(self):
        self.logger = logging.getLogger("pyanimeclick.parser")

    def parse_search_result(self, tag: Tag) -> SearchResult:
        return tag