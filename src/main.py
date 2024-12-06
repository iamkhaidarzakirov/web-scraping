import asyncio
import json
import logging
from math import ceil
from multiprocessing import Process
import os
import random
import time

from config import settings
from helpers.utils import chunk_list, save_html
from scrappers.httpx_scrapper.scrapper import HttpxScrapper
from scrappers.selenium_scrapper.scrapper import SeleniumScrapper

logger = logging.getLogger("streamLogger")


async def perform_async(*args, **kwargs) -> None:
    """Manage async scrapper here"""
    urls = ["https://example.org", "https://tryhackme.com"]

    async with HttpxScrapper(platform="linux") as scrapper:
        await scrapper.schedule_tasks(context=urls, coroutine=scrapper.atest_status)


def perform_sync(*args, **kwargs):
    """Manage sync scrapper here"""
    with HttpxScrapper(platform="linux") as scrapper:
        scrapper.test_status("https://www.example.org")
        scrapper.test_html_response("https://www.example.org")
        

def perform_browser(*args, **kwargs) -> None:
    """Manage browser scrapper here"""
    with SeleniumScrapper(**kwargs) as scrapper: # Initialize a new browser session with any params as kwargs
        scrapper.get_data(**kwargs)


def parallel_browser(path: str):
    if os.path.exists(path):
        with open(path) as json_file:
            urls = json.load(json_file)
            if not urls:
                raise ValueError("The urls list is empty")

        processes_count = settings.CPU_COUNT
        chunk_size = ceil(len(urls) / processes_count)
        tasks = []
        for chunk in chunk_list(data=urls, chunk_size=chunk_size):
                p = Process(target=perform_browser, kwargs={"context": chunk})
                tasks.append(p)
                p.start()
            
        [task.join for task in tasks]
    
    logger.warning(f"Specified path: {path} does not exist")


def main() -> None:
    """Run scrappers here"""
    # asyncio.run(perform_async())
    # perform_sync()
    # parallel_browser(path=os.path.join(settings.JSON_DIR, "urls.json"))


if __name__ == '__main__':
    main()
    