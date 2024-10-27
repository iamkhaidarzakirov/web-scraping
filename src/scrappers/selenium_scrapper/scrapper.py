import json
import os
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from typing import List, Dict
from fake_useragent import UserAgent

from custom_exceptions import exceptions
from config import settings
from client.headers import json_headers, html_headers
from scrappers.base_scrapper.scrapper import BaseScrapper


class SeleniumScrapper(BaseScrapper):
    """Create browser scrapper here"""
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._options = webdriver.ChromeOptions()
        self._session_params = kwargs
        self._session = None
        self._actions = None
        
    
    @property
    def session(self):
        return self._session

    def __enter__(self):
        self.create_session(**self._session_params)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()
    
    def create_session(self, **kwargs):
        if self._session is None:
            if kwargs.get("proxy") is not None:
                proxy = kwargs["proxy"]
                self.logger.info(f"BROWSER USE PROXY: [{proxy}] IN THIS SESSION")
                self._options.add_argument(f"--proxy-server={proxy}")

            for option in settings.options.arguments:
                self.logger.debug(f"Add an extra option to the session: [{option}]")
                self._options.add_argument(option) 

            self._session = webdriver.Chrome(service=Service(executable_path=settings.CHROME_DRIVER_PATH), options=self._options)
            self._actions = ActionChains(self._session)
            self.logger.info(f"Session created: {self._session}")
    
    def close_session(self):
        if self._session is not None:
            self._session.quit()
            self.logger.info(f"Session closed: {self._session} ")
            self._session = None
