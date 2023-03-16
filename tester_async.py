import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
from websiteData import headers
import datetime
import json


async def website_tester(session: aiohttp.ClientSession, i: int):
    url = f''
    global proxies_iterator
    try:
        proxy = next(proxies_iterator)
    except Exception:
        proxies_iterator = iter(proxies_async)
        proxy = next(proxies_iterator)
    async with session.post(url=url, headers=headers, proxy=proxy) as r:
        print(f'{r.status} WITH {proxy}')
        response = await r.text()
        soup = BeautifulSoup(response, 'lxml')
        # Try to save a random web page's source
        with open(f'test/test_{i}.html', 'w', encoding='utf-8') as file:
            file.write(response)


async def tasks_resolver(quantity: range = None):
    async with aiohttp.ClientSession() as session:
        tasks = []
        if attempts:
            for i in attempts:
                task = asyncio.create_task(website_tester(session, i))
                tasks.append(task)
            await asyncio.gather(*tasks)
    # When all tasks are finished successful, the flag name is changing
    global flag
    flag = False


if __name__ == '__main__':
    # Set a date
    curr_date = datetime.date.today().strftime('%Y_%m_%d')
    # Proxies aiohttp format
    with open('DATA/ru-proxies-aiohttp.json', 'r', encoding='utf-8') as json_file:
        proxies_async = json.load(json_file)
        proxies_iterator = iter(proxies_async)
    # Check
    attempts = range(1, 3)
    flag = True
    while True:
        if flag:
            try:
                # Need to add an argument to function — urls_list, pagination ot images_list
                asyncio.run(tasks_resolver(quantity=attempts))
            except Exception as ex:
                time.sleep(1)
                print(f'[ERROR] {ex}')
                continue
        else:
            break



