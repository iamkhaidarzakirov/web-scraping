"""Test websites here..."""
from data.client.client_data import *
from utils.proxies_utils.proxies import AIOHTTP_PROXIES
from testers.server_test_async import AsyncTester
import asyncio
from testers.server_test_sync import SyncTester


def main_sync():
    tester = SyncTester(
        url="https://www.1zoom.me/en/",  # specify url which server you want to test
        is_html=True,
        is_API=False,
        headers=html_headers,
    )
    for i in range(1, 6):
        tester.start(i=i)


async def main_async():
    """Coroutine to test server by asynchronous"""
    aiohttp_proxies = AIOHTTP_PROXIES
    proxies_iterator = None

    tester = AsyncTester(
        url="https://www.1zoom.me/en/",  # specify url which server you want to test
        headers=html_headers,
        req_count=range(10),)  # specify requests count

    tester.set_proxies(aiohttp_proxies)
    await tester.tasker()


if __name__ == '__main__':
    is_async = False  # Check!
    is_sync = True
    is_webdriver = False
    if is_async:
        asyncio.run(main_async())
    if is_sync:
        main_sync()
