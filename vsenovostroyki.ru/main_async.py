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


# The first step is to collect all the links to new buildings
async def get_urls(session, i):
    proxy = random.choice(proxies_async)
    domain = 'https://vsenovostroyki.ru'
    url = f'https://vsenovostroyki.ru/' \
          f'%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B8-%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D1%8B/' \
          f'?p={i}'
    async with session.get(url=url, headers=headers) as r:
        print(f'{r.status} WITH {proxy} | {i}')
        response = await r.text()
        soup = BeautifulSoup(response, 'lxml')
        main_block = soup.find('div', class_='b-search-results__items').find_all('h2', class_='b-offer-plate__title')
        for item in main_block:
            obj_url = domain + item.find('a').get('href')
            houses_urls.append(obj_url)


# The second step is to collect all needed data from building page
async def get_data(session, url):
    if url not in temp:
        proxy = random.choice(proxies_async)
        async with session.get(url=url, headers=headers) as r:
            print(f'{r.status} WITH {proxy}')
            response = await r.text()
            soup = BeautifulSoup(response, 'lxml')
            data_dict = {
                'Название': [''],
                'Застройщик': [''],
                'Регион': [''],
                'Метро': [''],
                'Адрес': [''],
                'До метро': [''],
                'Цена': [''],
                'Цена за м²': [''],
                'Площадь': [''],
                'Квартир': [''],
                'Тип дома': [''],
                'Этажность': [''],
                'Лифт': [''],
                'Паркинг': [''],
                'Класс': [''],
                'Сдача': [''],
                'Отделка': [''],
                'Потолки': [''],
                'Продавец': [''],
                'Ссылка на ЖК': [''],

            }
            try:
                name = soup.find('h1').text.strip()
            except Exception:
                name = ''
            # We need to set these 2 key ourselves, cause each object will have them
            data_dict['Название'][0] = name
            data_dict['Ссылка на ЖК'][0] = url
            main_data = soup.find_all('div', class_='b-product-card__col')[-1].find_all \
                ('div', class_='b-product-properties__item')
            for item in main_data:
                # We take the name of this key from the site. Since different objects may or may not have them.
                # But It looks awful. But I don't know yet how make this code string more correctly and pretty
                key = item.find('div', class_='b-product-properties__key-wrap').text.strip().replace('\n', '').replace(
                    '                                                                            ',
                    ' '
                )
                # Values in this site are specifies into list.
                # So we need some actions and editings to gather correct result
                value_data = item.find('div', class_='b-product-properties__value-wrap').find_all(
                    'div',
                    class_='b-product-properties__value-item'
                )
                values_list = []
                for el in value_data:
                    # It looks awfully. But I don't know yet how make this code string more correctly and pretty
                    value_el = el.text.strip().replace(
                        '                                                                                    ',
                        ' '
                    ).replace('\n', '').replace('  ', ' ')
                    values_list.append(value_el)
                value = ' '.join(values_list)
                if key == 'Цена за м²' or key == 'Цена':
                    value_list = value.split(' ')
                    value = value_list[1]
                    # Some no used edits from customer
                    # sorted_list = []
                    # for char in value_list:
                    #     if char.isdigit():
                    #         sorted_list.append(char)
                    # value = ''.join(sorted_list)

                data_dict[key][0] = value
            df = pd.DataFrame(data_dict)
            # Files writing block
            if not os.path.exists(f'data/novostroyki_moskva_{curr_date}.xlsx'):
                df.to_excel(f'data/novostroyki_moskva_{curr_date}.xlsx', index=False)
            else:
                with pd.ExcelFile(f'data/novostroyki_moskva_{curr_date}.xlsx', engine='openpyxl') as reader:
                    info = reader.parse()
                    rows = len(info)
                    start = rows + 1
                    with pd.ExcelWriter(f'data/novostroyki_moskva_{curr_date}.xlsx', mode='a', engine='openpyxl',
                                        if_sheet_exists='overlay') as writer:
                        df.to_excel(writer, startrow=start, index=False, header=False)
            # We need add url to used urls file to avoid repetition
            with open('data/temp.txt', 'a', encoding='utf-8') as file:
                file.write(url + '\n')
            # The site is sensitive to requests, so we need to add a delay
            global counter
            if counter % 3 == 0:
                time.sleep(1)
            counter += 1


async def tasks_resolver(urls_list=None, pagination=None):
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
    # When the function completes successfully, change the global var value to exit from cycle
    global flag
    flag = False


if __name__ == '__main__':
    # Set a date
    curr_date = datetime.date.today().strftime('%Y_%m_%d')
    # Proxies aiohttp format
    with open('../DATA/RU-proxy-list.txt', 'r', encoding='utf-8') as txt_file:
        raw_data = txt_file.readlines()
        proxies_async = [item.replace('\n', '') for item in raw_data]
    # Part 1
    # Specify the count of pages
    pages = range(1, 43)
    houses_urls = []
    asyncio.run(tasks_resolver(pagination=pages))
    # After successful function completion we need to write list with urls to Json
    with open('data/houses_urls.json', 'w', encoding='utf-8') as json_file:
        json.dump(houses_urls, json_file, indent=4, ensure_ascii=False)
    # Part 2
    # We need to create temp file to avoid repetitions
    if not os.path.exists('data/temp.txt'):
        with open('data/temp.txt', 'w', encoding='utf-8') as txt_file:
            txt_file.write('')
    # We need to open Json and read to list
    with open('data/houses_urls.json', 'r', encoding='utf-8') as json_file:
        houses_urls = json.load(json_file)
    flag = True
    counter = 1
    while True:
        if flag:
            try:
                # We need to open temp file and read it as list
                with open('data/temp.txt', 'r', encoding='utf-8') as txt_file:
                    raw_data = txt_file.readlines()
                    temp = [item.replace('\n', '') for item in raw_data]
                asyncio.run(tasks_resolver(urls_list=houses_urls))
            except Exception as ex:
                time.sleep(1)
                print(ex)
                continue
        else:
            # The end
            break
