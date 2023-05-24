from ..utils import parse_csrf_token
from ..utils import (
    LOGIN_PAGE,
    LOGIN_CHECK_PAGE
)

from typing import Optional

import pyanimeclick
import logging

log = logging.getLogger(__name__)

class Login:
    async def login(
        self: "pyanimeclick.AnimeClick",
        username: str,
        password: str,
        use_session_file: bool = False
    ) -> Optional[bool]:
        if use_session_file:
            if self._check_session():
                return self._load_session()
        # Get PHPSESSID (session_id) and CSRF Token
        response = await self._make_request(
            method="POST", url=LOGIN_PAGE
        )
        csrf_token = parse_csrf_token(response.text)
        log.debug(f"CSRF Token: {csrf_token}")
        # Login and get REMEMBERME
        await self._make_request(
            method="POST", url=LOGIN_CHECK_PAGE,
            data={
                "_username": username,
                "_password": password,
                "_remember_me": "on",
                "_csrf_token": csrf_token,
            }
        )
        if use_session_file:
            self._store_session()
        log.debug("Logged in successfully.")
        return True