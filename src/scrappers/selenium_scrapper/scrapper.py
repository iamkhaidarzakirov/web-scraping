import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from typing import List, Dict
from webdriver_manager.chrome import ChromeDriverManager
from custom_exceptions import exceptions
from config import settings
from client.headers import json_headers, html_headers
from scrappers.base_scrapper.scrapper import BaseScrapper


class SeleniumScrapper(BaseScrapper):
    """Create browser scrapper here"""
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._options = settings.OPTIONS
        self._session = None
        self._session_params = kwargs
    
    @property
    def session(self):
        return self._session

    def __enter__(self):
        self.create_session(**self._session_params)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session is not None:
            self._session.close()
            self.logger.info(f"Session closed: {self._session} ")
            self._session = None
    
    def create_session(self, **kwargs):
        if self._session is None:
            self._session = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            self.session.maximize_window()
            self.logger.info(f"Session created: {self._session}")
        