import asyncio
import aiohttp
from bs4 import BeautifulSoup


class AsyncTester:
    PROXIES_ITER = None
    PROXIES = None
    """Tests the server sending a few async requests and checks the responses..."""
    def __init__(
            self,
            url: str,
            headers: dict = None,
            cookies: dict = None,
            req_count: range = None):
        self.url = url
        self.req_count = req_count
        self.cookies = cookies
        self.headers = headers

    @classmethod
    def set_proxies(cls, proxies: list):
        cls.PROXIES = proxies
        cls.PROXIES_ITER = iter(proxies)

    async def website_tester(self, session: aiohttp.ClientSession) -> None:
        """Sends many requests and checks response status"""
        if self.url:
            if self.PROXIES_ITER:
                try:
                    proxy = next(self.PROXIES_ITER)
                except StopIteration:
                    self.PROXIES_ITER = iter(self.PROXIES)
                    proxy = next(self.PROXIES_ITER)
            else:
                proxy = None

            async with session.get(url=self.url, headers=self.headers, proxy=proxy) as r:
                print(f'{r.status} WITH {proxy}')
                response = await r.text()
                soup = BeautifulSoup(response, 'lxml')
                print(soup.title)

    async def tasker(self):
        """Creates and organizes tasks..."""

        async with aiohttp.ClientSession() as session:
            tasks = []
            if self.req_count:
                for i in self.req_count:
                    task = asyncio.create_task(self.website_tester(session))
                    tasks.append(task)
                await asyncio.gather(*tasks)


