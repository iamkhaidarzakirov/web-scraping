import requests
import json
import random
import time
import asyncio
import aiohttp
import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup


def browser_tester():
    options = uc.options.ChromeOptions()
    options.add_argument('--headless')
    with uc.Chrome(options=options) as browser:
        browser.get(url)
    response = browser.page_source
    # Get Json data from html page source
    # content = browser.find_element(by='tag name', value='pre').text
    # parsed_json = json.loads(content)
    # with open(f'DATA/test.json', 'w', encoding='utf-8') as file:
    #     json.dump(parsed_json, file, indent=4, ensure_ascii=False)


def site_tester_sync():
    # Check number or requests
    for i in range(1, 2):
        if i % 10 == 0:
            time.sleep(1)
        proxy = random.choice(proxies_sync)
        response = requests.get(url=url).json()
        print(f'{response.status_code} WITH {proxy}')
        # HTML
        with open(f'DATA/test_{i}.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        # JSON
        # with open(f'DATA/test_{i}.json', 'w', encoding='utf-8') as file:
        #     json.dump(response, file, indent=4, ensure_ascii=False)


async def site_tester(session, spec_url, i):
    proxy = random.choice(proxies_async)
    async with session.get(url=spec_url, proxy=proxy) as r:
        print(f'{r.status} WITH {proxy}')
        response = await r.text()


async def site_tester_async():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 101):
            task = asyncio.create_task(site_tester(session, url, i))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    # For requests module
    with open('DATA/proxies.json', 'r', encoding='utf-8') as json_file:
        proxies_sync = json.load(json_file)
    # For AIOHTTP
    with open('DATA/RU-proxy-list.txt', 'r', encoding='utf-8') as txt_file:
        data = txt_file.readlines()
        proxies_async = [item.replace('\n', '') for item in data]

    url = ''
    # browser_tester()
    # site_tester_sync()
    # asyncio.run(site_tester_async())
