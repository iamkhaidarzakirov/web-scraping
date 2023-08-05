import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
import json


async def website_tester(session: aiohttp.ClientSession, i: int) -> None:
    """Function tests the specified website, sending many requests"""

    url = f''
    global have_proxies
    if have_proxies:
        # If proxies are specified we create iterator and iterate over each proxy
        global proxies_iterator
        try:
            proxy = next(proxies_iterator)
        except StopIteration:
            proxies_iterator = iter(proxies_async)
            proxy = next(proxies_iterator)
    else:
        proxy = None

    async with session.post(url=url, headers=headers, proxy=proxy) as r:
        print(f'{r.status} WITH {proxy}')
        response = await r.text()
        soup = BeautifulSoup(response, 'lxml')
        print(soup.title)
        # Check parameter
        to_write = False
        if to_write:
            # You need try to save a page's source to see what have responded to request
            with open(f'test/test.html', 'w', encoding='utf-8') as file:
                file.write(response)


async def tasks_resolver(quantity: range = None) -> None:
    """"""

    async with aiohttp.ClientSession() as session:
        tasks = []
        if quantity:
            for i in attempts:
                task = asyncio.create_task(website_tester(session, i))
                tasks.append(task)
            await asyncio.gather(*tasks)

    global flag
    flag = False


if __name__ == '__main__':
    # Set the required parameter
    have_proxies = False
    if have_proxies:
        # Proxies aiohttp format
        with open('DATA/ru-proxies-aiohttp.json', 'r', encoding='utf-8') as json_file:
            proxies_async = json.load(json_file)
            proxies_iterator = iter(proxies_async)
    # Check these parameters before running
    attempts = range(1, 3)
    flag = True
    while True:
        if flag:
            try:
                # You need to add an argument to function
                asyncio.run(tasks_resolver(quantity=attempts))
            except Exception as ex:
                time.sleep(1)
                print(f'[ERROR] {ex}')
                continue
        else:
            break
