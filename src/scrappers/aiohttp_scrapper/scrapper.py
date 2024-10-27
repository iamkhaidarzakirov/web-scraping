import aiohttp
import asyncio
import json
import os
from typing import List, Dict, Callable

from custom_exceptions import exceptions
from config import settings
from client.headers import json_headers, html_headers
from scrappers.base_scrapper.scrapper import BaseScrapper


class AiohttpScrapper(BaseScrapper):
    def __init__(self) -> None:
        super().__init__()
        self._session = None

    async def __aenter__(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
            self.logger.info(f"Create a new session: {self._session}")
        return self
    
    @property
    def session(self):
        return self._session
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session is not None:
            await self._session.close()
            self.logger.info(f"Closed session: {self._session}")
            self._session = None
    
    async def test_status_code(self, session: aiohttp.ClientSession, url: str) -> None:
        async with session.get(url=url, headers=html_headers) as response:
            status = response.status
            self.logger.debug(f"URL: [{url}] STATUS: [{status}]")

    async def schedule_tasks(self, context: List, coroutine: Callable):
        tasks = []
        for item in context:
            task = asyncio.create_task(coro=coroutine(self._session, item))
            tasks.append(task)
        
        self.logger.info("Scheduling the tasks...")
        await asyncio.gather(*tasks)
