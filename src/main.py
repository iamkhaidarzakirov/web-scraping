import asyncio
import random
import time

from config import settings
from scrappers.requests_scrapper.scrapper import RequestsScrapper
from scrappers.aiohttp_scrapper.scrapper import AiohttpScrapper
from scrappers.selenium_scrapper.scrapper import SeleniumScrapper


async def perform_async(*args, **kwargs) -> None:
    """Manage async scrapper here"""
    urls = ["https://example.org", "https://tryhackme.com"]

    async with AiohttpScrapper() as scrapper:
        await scrapper.schedule_tasks(context=urls, coroutine=scrapper.test_status_code)


def perform_sync(*args, **kwargs):
    """Manage sync scrapper here"""
    scrapper = RequestsScrapper()


def perform_browser(*args, **kwargs) -> None:
    """Manage browser scrapper here"""
    
    with SeleniumScrapper(headless=settings.HEADLESS, **kwargs) as scrapper:
        scrapper.session.get("https://example.org")
        time.sleep(5)
            

def main() -> None:
    """Run scrappers here"""
    perform_browser()


if __name__ == '__main__':
    main()
    