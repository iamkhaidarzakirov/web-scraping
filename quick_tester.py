from requirements import headers, cookies
import requests
import json
import random
import time
import aiohttp
import asyncio


def site_tester_sync(url):
    for i in range(1, 21):
        if i % 10 == 0:
            time.sleep(1)
        proxy = random.choice(proxies_sync)
        response = requests.get(url=url, cookies=cookies, headers=headers, proxies=proxy)
        print(f'{response.status_code} WITH {proxy}')
        with open(f'data/test_{i}.html', 'w', encoding='utf-8') as html:
            html.write(response.text)


async def site_tester(session, url, i):
    proxy = random.choice(proxies_async)
    async with session.get(url=url, cookies=cookies, headers=headers, proxy=proxy) as r:
        print(f'{r.status} WITH {proxy}')
        response = await r.text()


async def site_tester_async(url):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 101):
            task = asyncio.create_task(site_tester(session, url, i))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    # For requests module
    with open('data/proxies.json', 'r', encoding='utf-8') as json_file:
        proxies_sync = json.load(json_file)
    # For AIOHTTP
    with open('data/RU-proxy-list.txt', 'r', encoding='utf-8') as txt_file:
        data = txt_file.readlines()
        proxies_async = [item.replace('\n', '') for item in data]

    url = 'https://www.avtoall.ru/'
    # site_tester_sync
    asyncio.run(site_tester_async(url))
