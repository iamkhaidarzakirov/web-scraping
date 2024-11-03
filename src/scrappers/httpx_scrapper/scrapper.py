import asyncio
import json
import httpx
import os
from typing import List, Dict, Callable

from custom_exceptions import exceptions
from config import settings
from client.headers import json_headers, html_headers
from scrappers.base_scrapper.scrapper import BaseScrapper


class HttpxScrapper(BaseScrapper):
    def __init__(self) -> None:
        super().__init__()
        self._session = None
    
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
        
    