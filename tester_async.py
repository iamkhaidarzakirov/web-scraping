import asyncio
import aiohttp
import json
import time
from bs4 import BeautifulSoup
from websiteData import headers
import random
import os
import pandas as pd
import datetime
import aiofiles


# This function can be used to collect links to items in every available page of a website or test the website security
async def get_urls(session, i):
    pages_count = 1
    for i in range(1, pages_count + 1):
        url = f'vk.com'
        proxy = random.choice(proxies_async)
        async with session.post(url=url, headers=headers, proxy=proxy) as r:
            print(f'{r.status} WITH {proxy}')
            response = await r.text()
            soup = BeautifulSoup(response, 'lxml')

            # Try to save a random web page's source
            if i % 5 == 0:
                with open(f'test/test_{i}.html', 'w', encoding='utf-8') as file:
                    file.write(response)


# This function can be used to collect data from each specified url
async def get_data(session, url):
    if url not in temp:
        proxy = random.choice(proxies_async)
        async with session.get(url=url, headers=headers, proxy=proxy) as r:
            response = r.text()

            with open(f'test/test.html', 'w', encoding='utf-8') as file:
                file.write(response)


# This function can be used to async download images
async def get_images(session, url):
    if url not in temp:
        filename = ''
        proxy = random.choice(proxies_async)
        async with session.get(url=url, headers=headers, proxy=proxy) as r:
            print(f'{r.status} WITH {proxy}')
            async with aiofiles.open(f'data/{filename}', 'wb') as image:
                async for chunk in r.content.iter_chunked(64 * 1024):
                    await image.write(chunk)


# This is a main function to create and gather all tasks
async def tasks_resolver(urls_list=None, pagination=None, images_urls=None):
    async with aiohttp.ClientSession() as session:
        tasks = []
        if urls_list:
            for url in urls_list:
                task = asyncio.create_task(get_data(session, url))
                tasks.append(task)
            await asyncio.gather(*tasks)
        if pagination:
            for i in pagination:
                task = asyncio.create_task(get_urls(session, i))
                tasks.append(task)
            await asyncio.gather(*tasks)
        if images_urls:
            for url in images_urls:
                task = asyncio.create_task(get_images(session, url))
                tasks.append(task)
            await asyncio.gather(*tasks)
    # When all tasks are finished successful, the flag name is changing
    global flag
    flag = False


if __name__ == '__main__':
    # Set a date
    curr_date = datetime.date.today().strftime('%Y_%m_%d')
    # Proxies aiohttp format
    with open('data/RU-proxy-list.txt', 'r', encoding='utf-8') as txt_file:
        raw_data = txt_file.readlines()
        proxies_async = [item.replace('\n', '') for item in raw_data]
    # Temp
    if not os.path.exists('data/temp.txt'):
        with open('data/temp.txt', 'w', encoding='utf-8') as txt_file:
            txt_file.write('')
    # Check
    pages = range(1, 3)
    flag = True
    while True:
        if flag:
            try:
                # Need to open temp file and read it as list
                with open('data/temp.txt', 'r', encoding='utf-8') as txt_file:
                    raw_data = txt_file.readlines()
                    temp = [item.replace('\n', '') for item in raw_data]
                # Need to add an argument to function — urls_list, pagination ot images_list
                asyncio.run(tasks_resolver(pagination=pages))
            except Exception as ex:
                time.sleep(1)
                print(f'[ERROR] {ex}')
                continue
        else:
            break



