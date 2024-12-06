import asyncio
import json
import os
import random
from typing import List, Literal, Dict, Callable

import httpx
import pandas as pd

from custom_exceptions import exceptions
from config import settings
from client.agents import user_agents
from helpers.helpers import init_headers, save_html_content, save_list_to_json
from scrappers.base_scrapper.scrapper import BaseScrapper


class HttpxScrapper(BaseScrapper):
    def __init__(self, platform: Literal["windows", "linux", "android", "apple"]) -> None:
        super().__init__()
        self._session = None
        self.platform = platform if platform else "windows"
        self.headers = init_headers(platform=self.platform)
        
    
    @property
    def session(self):
        return self._session

    def __enter__(self):
        if self._session is None:
            self._session = httpx.Client()
            self.logger.info(f"Create a new sync session: {self._session}")
            return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session is not None:
            self._session.close()
            self.logger.info(f"Close sync session: {self._session}")
            self._session = None

    async def __aenter__(self):
        if self._session is None:
            self._session = httpx.AsyncClient()
            self.logger.info(f"Create a new async session: {self._session}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session is not None:
            await self._session.aclose()
            self.logger.info(f"Close async session: {self._session}")
            self._session = None

    # Async part
    async def schedule_tasks(self, context: List, coroutine: Callable):
        tasks = []
        for item in context:
            task = asyncio.create_task(coro=coroutine(item))
            tasks.append(task)
        
        self.logger.info("Scheduling the tasks...")
        await asyncio.gather(*tasks)

    async def atest_status(self,item: str) -> None:
        r = await self.session.get(item)
        self.logger.debug(f"URL: [{item}] STATUS CODE: [{r.status_code}]")

    # Sync part
    def test_status(self, item: str) -> None:
        r = self.session.get(item)
        self.logger.debug(f"URL: [{item}] STATUS CODE: [{r.status_code}]")
    

    def test_html_response(self, url: str) -> None:
        r = self.session.get(url, headers=self.headers)
        
        if r.status_code == 200:
            self.logger.debug("Check templates/temp.html")
            return save_html_content(r.text)
            
        
        self.logger.warning(f"STATUS CODE: [{r.status_code}]")
