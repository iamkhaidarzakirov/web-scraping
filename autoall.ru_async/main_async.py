from websiteData import headers
import aiohttp
import asyncio
import json
import time
import random
from bs4 import BeautifulSoup
import os
import csv


async def gather_data(session, url):
    proxy = random.choice(proxies_async)
    if url not in used_urls:
        async with session.get(url=url, headers=headers, proxy=proxy) as r:
            response = await r.text()
            soup = BeautifulSoup(response, 'lxml')
            main_block = soup.find('div', class_='color-block')
            # Category
            try:
                category = main_block.find('div', class_='bc').find_all('a')[-1].text.strip()
            except Exception:
                category = ''
            # Name
            try:
                name = main_block.find('h1').find('span', itemprop='name').text.strip()
            except Exception:
                name = ''
            # Main article
            try:
                articles = main_block.find('h2').find_all('span')
                if len(articles) > 1:
                    main_article = articles[0].text.strip().replace('еще', '')
                    extra_article = articles[-1].text.strip().split(':')[-1].strip().replace('скрыть', '')
                else:
                    main_article = articles[0].text.strip()
                    extra_article = ''
            except Exception:
                main_article = ''
                extra_article = ''
            # Price
            try:
                price = main_block.find('div', class_='price-offer-left').text.strip()
            except Exception:
                price = ''
            # Write to file
            with open('data/data_example.csv', 'a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    (
                        category,
                        main_article,
                        extra_article,
                        name,
                        price,
                    )
                )
            # END OF DATA GATHERING FROM URL
            with open('data/temp.txt', 'a', encoding='utf-8') as txt_file:
                txt_file.write(url + '\n')
    else:
        pass


async def create_tasks(urls_list):
    async with aiohttp.ClientSession() as session:
        tasks = []
        global part_counter
        for url in urls_list[part_counter]:
            task = asyncio.create_task(gather_data(session, url))
            tasks.append(task)
        print('[INFO] => WAIT A FEW SECONDS: COLLECTING ALL TASKS')
        await asyncio.gather(*tasks)
    # Check parts options
    if part_counter == len(urls_list) - 1:
        global flag
        flag = False
    else:
        print(f'[INFO] => URLS IN PART {part_counter} IS DONE')
        os.remove('data/temp.txt')
        part_counter += 1
        with open('data/parameters.json', 'w', encoding='utf-8') as file:
            params = {
                'part_counter': part_counter
            }
            json.dump(params, file, indent=4, ensure_ascii=False)
        time.sleep(random.randrange(15, 21))


def make_parts(data_list):
    temp_data = []
    result_data = []
    for item in data_list:
        # Check parts length
        if len(temp_data) == 10_000:
            result_data.append(temp_data)
            temp_data = []
        temp_data.append(item)
    result_data.append(temp_data)
    return result_data


if __name__ == '__main__':
    # Create parameters JSON
    if not os.path.exists('data/parameters.json'):
        with open('data/parameters.json', 'w', encoding='utf-8') as file:
            params = {
                'part_counter': 0
            }
            json.dump(params, file, indent=4, ensure_ascii=False)
    # Create table
    if not os.path.exists('data/data_example.csv'):
        with open('data/data_example.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                (
                    'Категория',
                    'Артикул',
                    'Дополнительные артикулы',
                    'Название',
                    'Цена',
                )
            )
    # JSON file is too large — over 150_000 urls, so I make parts
    with open(f'data/unique_urls.json', 'r', encoding='utf-8') as json_file:
        product_list = json.load(json_file)
        task_by_parts = make_parts(product_list)
    with open('data/parameters.json', 'r', encoding='utf-8') as file:
        params = json.load(file)
    # Global vars
    part_counter = params['part_counter']
    flag = True
    # Start
    while True:
        if flag:
            try:
                # Create proxy list | Why here? If in future all proxies will be blocked, we able to change proxies list unstoping the script
                with open('DATA/RU-proxy-list.txt', 'r', encoding='utf-8') as txt_file:
                    data = txt_file.readlines()
                    proxies_async = [item.replace('\n', '') for item in data]
                # Create temp file
                if not os.path.exists('data/temp.txt'):
                    with open('data/temp.txt', 'w', encoding='utf-8') as temp_txt:
                        temp_txt.write('')
                # Check
                with open('data/temp.txt', 'r', encoding='utf-8') as txt_reader:
                    data = txt_reader.readlines()
                    used_urls = [item.replace('\n', '') for item in data]
                asyncio.run(create_tasks(task_by_parts))
            except Exception as ex:
                print(f'[ERROR] => {ex}')
                time.sleep(5)
                continue
        else:
            # End
            print(f'[INFO] => СБОР ЗАВЕРШЕН')
            # Remove temporary files
            os.remove('data/parameters.json')
            os.remove('data/temp.txt')
            break
