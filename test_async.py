import json
import time
import datetime
import random
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from websiteData import headers


async def web_site_tester(session, spec_url, i):
    proxy = random.choice(proxies_async)
    async with session.get(url=spec_url, headers=headers, proxy=proxy) as r:
        print(f'{r.status} WITH {proxy}')
        response = await r.text()
        # Try to write a file and look what will happen
        if i % 100 == 0:
            with open('DATA/test.html', 'w', encoding='utf-8') as file:
                file.write(response)


async def tasks_resolver():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 101):
            task = asyncio.create_task(web_site_tester(session, url, i))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    # Proxies aiohttp format
    with open('data/RU-proxy-list.txt', 'r', encoding='utf-8') as txt_file:
        data = txt_file.readlines()
        proxies_async = [item.replace('\n', '') for item in data]
    # Set parameters and let's go!
    url = ''
    asyncio.run(tasks_resolver())
