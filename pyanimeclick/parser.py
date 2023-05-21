from bs4 import Tag

from .types import SearchResult

import logging

class Parser:
    def __init__(self):
        self.logger = logging.getLogger("pyanimeclick.parser")

    def parse_search_result(self, tag: Tag) -> SearchResult:
        print(tag, "\n\n")