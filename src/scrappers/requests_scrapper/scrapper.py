import json
import os
import requests
from typing import List, Dict

from custom_exceptions import exceptions
from config import settings
from client.headers import json_headers, html_headers
from scrappers.base_scrapper.scrapper import BaseScrapper


class RequestsScrapper(BaseScrapper):
    """Create http requests scrapper here"""
    def __init__(self) -> None:
        super().__init__()
        self._session = requests.session()

    @property
    def session(self):
        return self._session
    
    def visit_main_page(self):
        self.logger.info("Visit main page")
        self.session.get("https://ozon.ru", headers=html_headers)