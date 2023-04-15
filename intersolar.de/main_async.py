import asyncio
import aiohttp
import json
import time
from bs4 import BeautifulSoup
from websiteData import headers, cookies
import random
import os
import pandas as pd
import datetime


async def get_urls(session: aiohttp.ClientSession, i: int) -> None:
    ...


async def get_images(session: aiohttp.ClientSession, url: str) -> None:
    ...


async def get_data(session: aiohttp.ClientSession, url: str) -> None:
    if url not in temp:
        proxy = random.choice(proxies_async)
        async with session.get(url=url, headers=headers, proxy=proxy) as r:
            print(f'{r.status} WITH {proxy}')
            response = await r.text()
            soup = BeautifulSoup(response, 'lxml')
            data_dict = {
                'Booth No': [],
                'Company Name': [],
                'Phone': [],
                'Email': [],
                'Website': [],
                'Address': [],
                'URL': []

            }
            name = soup.find('h1').text.strip()
            booth = soup.find('div', class_='floatcontainer').find('p').text.strip()
            contact_block = soup.find('dl', class_='content-detail-texticon-block').find_all('dt')
            # Due to the incorrect layout of the site, we have to go through all the options
            phone = ''
            email = ''
            address = ''
            website = ''
            for item in contact_block:

                if '+' in item.text:
                    phone = item.text.strip()

                if '@' in item.text:
                    email = item.text.strip()

                if 'http' in item.text:
                    website = item.text.strip()

                if name in item.text:
                    address = item.text.strip().split(name)[-1]

            data_dict['Booth No'].append(booth)
            data_dict['Company Name'].append(name)
            data_dict['Phone'].append(phone)
            data_dict['Email'].append(email)
            data_dict['Website'].append(website)
            data_dict['Address'].append(address)
            data_dict['URL'].append(url)
            # Append a row in sheet
            df = pd.DataFrame(data_dict)
            if not os.path.exists(f'data/companies.xlsx'):
                df.to_excel(f'data/companies.xlsx', index=False)
            else:
                with pd.ExcelFile(f'data/companies.xlsx', engine='openpyxl') as reader:
                    info = reader.parse()
                    rows = len(info)
                    start = rows + 1
                    with pd.ExcelWriter(f'data/companies.xlsx', mode='a', engine='openpyxl',
                                        if_sheet_exists='overlay') as writer:
                        df.to_excel(writer, startrow=start, index=False, header=False)

            with open('data/temp.txt', 'a', encoding='utf-8') as file:
                file.write(url + '\n')


async def tasks_resolver(urls_list: list = None, pagination: range = None, images_urls: list = None):
    """Function to gather tasks. It may take different arguments. Depending on what argument it takes,
    a certain function will be executed"""

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
    # When all tasks are done, you need to change the global flag value to exit from infinite loop
    global flag
    flag = False


if __name__ == '__main__':
    # Set a date
    curr_date = datetime.date.today().strftime('%Y_%m_%d')
    # Proxies aiohttp format
    with open('../DATA/RU-proxy-list.txt', 'r', encoding='utf-8') as txt_file:
        raw_data = txt_file.readlines()
        proxies_async = [item.replace('\n', '') for item in raw_data]
    if not os.path.exists('data/temp.txt'):
        with open('data/temp.txt', 'w', encoding='utf-8') as txt_file:
            txt_file.write('')
    with open('data/all_items.json', 'r', encoding='utf-8') as file:
        all_items = json.load(file)
    flag = True
    while True:
        if flag:
            try:
                # You need to open temp file and read it as list
                with open('data/temp.txt', 'r', encoding='utf-8') as txt_file:
                    raw_data = txt_file.readlines()
                    temp = [item.replace('\n', '') for item in raw_data]
                asyncio.run(tasks_resolver(urls_list=all_items))
            except Exception as ex:
                time.sleep(1)
                print(f'[ERROR] {ex}')
                continue
        else:
            break
