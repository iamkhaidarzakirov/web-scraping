import requests
import json
import random
import time
from websiteData import headers, cookies
from bs4 import BeautifulSoup


def get_urls() -> None:
    # cause the data project was one-time, the number of pages have specified manually
    pages_count = 22
    global proxies_iterator
    for i in range(1, pages_count + 1):
        # Take next proxy in list for each new request
        try:
            proxy = next(proxies_iterator)
        except StopIteration:
            proxies_iterator = iter(proxies_sync)
            proxy = next(proxies_iterator)
        domain = 'https://www.intersolar.de'
        # API
        url = 'https://www.intersolar.de/search/execute'
        json_data = {
            'page': f'{i}',
            'menuPageId': '5f5b269c1109ff53da1c9fe2',
            'menuPageTypes': [
                '5ef3588ed984e36063189652',
            ],
            'term': '',
            'sortBy': 'ALPHA',
            'condensed': True,
        }
        response = requests.post(url=url, headers=headers, json=json_data, cookies=cookies, proxies=proxy)
        print(f'{response.status_code} WITH {proxy}')
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a', class_='teaser')
        for link in links:
            url = domain + link.get('href')
            all_items.append(url)
        time.sleep(1)


if __name__ == '__main__':
    # Proxies requests format
    with open('../DATA/ru-proxies-requests.json', 'r', encoding='utf-8') as json_file:
        proxies_sync = json.load(json_file)
        proxies_iterator = iter(proxies_sync)
    all_items = []
    get_urls()
    with open('data/all_items.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_items, json_file, indent=4, ensure_ascii=False)


