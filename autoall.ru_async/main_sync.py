from requirements import headers
import requests
import json
import time
import random
from bs4 import BeautifulSoup
import os


def get_all_categories(url):
    proxy = random.choice(proxies_sync)
    response = requests.get(url=url, headers=headers, proxies=proxy)
    status = response.status_code
    soup = BeautifulSoup(response.text, 'lxml')
    main_table = soup.find('div', class_='top-sections').find_all('li', class_='l')[0:14]
    all_categories = []
    for li in main_table:
        category_url = domain + li.find('a').get('href')
        response = requests.get(url=category_url, headers=headers, proxies=proxy)
        time.sleep(0.5)
        soup = BeautifulSoup(response.text, 'lxml')
        main_block = soup.find_all('div', class_='section')
        for div in main_block:
            subcategory_url = domain + div.find('div', class_='left').find('a').get('href')
            all_categories.append(subcategory_url)
        print(f'[INFO] => {category_url} DONE')
    with open('data/all_categories_urls.json', 'w', encoding='utf-8') as file:
        json.dump(all_categories, file, indent=4, ensure_ascii=False)


def get_products_urls():
    with open('data/all_categories_urls.json', 'r', encoding='utf-8') as file:
        categories = json.load(file)
    with open('data/temp.txt', 'r', encoding='utf-8') as txt_reader:
        data = txt_reader.readlines()
        used_urls = [item.replace('\n', '') for item in data]
    # Check
    for url in categories:
        i = 1
        while True:
            # Check
            page_url = f'{url}?page={i}'
            if page_url in used_urls:
                print(f'[INFO] {page_url} IS ALREADY ADDED')
                i += 1
                continue
            proxy = random.choice(proxies_sync)
            response = requests.get(url=page_url, headers=headers, proxies=proxy)
            soup = BeautifulSoup(response.text, 'lxml')
            main_block = soup.find('div', class_='list-compact')
            if main_block:
                items = main_block.find_all('div', class_='item item-elem')
                for item in items:
                    product_url = domain + item.find('div', class_='image').find('a').get('href')
                    global counter
                    counter += 1
                    # Check
                    if not os.path.exists(f'data/product_urls.txt'):
                        with open(f'data/product_urls.txt', 'w', encoding='utf-8') as txt_writer:
                            txt_writer.write(product_url + '\n')
                    else:
                        with open(f'data/product_urls.txt', 'a', encoding='utf-8') as txt_appender:
                            txt_appender.write(product_url + '\n')
                with open('data/temp.txt', 'a', encoding='utf-8') as file:
                    file.write(page_url + '\n')
                print(f'[INFO] => PAGE {i} ITEMS ARE ADDED')
                i += 1
            else:
                print(f'[INFO] => CATEGORY => {url} IS DONE')
                break
    global flag
    flag = False
    print(f'[INFO] => GATHERING IS COMPLETE')


def delete_repeats():
    with open(f'data/product_urls.txt', 'r', encoding='utf-8') as txt_reader:
        data = txt_reader.readlines()
        temp = set(data)
        unique_urls = [item.replace('\n', '') for item in list(temp)]

    with open(f'data/unique_urls.json', 'w', encoding='utf-8') as json_file:
        json.dump(unique_urls, json_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # Proxies requests format
    with open('DATA/proxies.json', 'r', encoding='utf-8') as json_file:
        proxies_sync = json.load(json_file)
    # IF SCRIPT STOPS, WITH TEMP FILE WE'LL CONTINUE FROM STOPPING PLACE
    if not os.path.exists('data/temp.txt'):
        with open('data/temp.txt', 'w', encoding='utf-8') as txt_writer:
            txt_writer.write('')
    url = 'https://www.avtoall.ru/'
    domain = 'https://www.avtoall.ru'
    # Get all categories
    get_all_categories(url)
    # Get all products urls
    counter = 1
    flag = True
    while True:
        if flag:
            try:
                get_products_urls()
            except Exception as ex:
                print(f'[ERROR] => {ex}')
                time.sleep(15)
                continue
        else:
            break
    # Delete repeats if they are
    delete_repeats()
