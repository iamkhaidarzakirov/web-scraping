import asyncio
import random
import time

from config import settings
from scrappers.httpx_scrapper.scrapper import HttpxScrapper
from scrappers.selenium_scrapper.scrapper import SeleniumScrapper


async def perform_async(*args, **kwargs) -> None:
    """Manage async scrapper here"""
    urls = ["https://example.org", "https://tryhackme.com"]

    async with HttpxScrapper() as scrapper:
        await scrapper.schedule_tasks(context=urls, coroutine=scrapper.atest_status)


def perform_sync(*args, **kwargs):
    """Manage sync scrapper here"""
    with HttpxScrapper() as scrapper:
        scrapper.test_status("https://www.example.org")


def perform_browser(*args, **kwargs) -> None:
    """Manage browser scrapper here"""
    with SeleniumScrapper(**kwargs) as scrapper: # Initialize a new browser session with any params as kwargs
        pass
            

def main() -> None:
    """Run scrappers here"""
    asyncio.run(perform_async())
    perform_sync()


if __name__ == '__main__':
    main()
    