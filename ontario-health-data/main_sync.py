import requests
import json
from bs4 import BeautifulSoup
import time
from websiteData import headers
import os
import pandas as pd


def get_data(source_url):
    for zip_code in zips:
        # Choose a proxy
        global proxies_iterator
        try:
            proxy = next(proxies_iterator)
        except StopIteration:
            proxies_iterator = iter(proxies_sync)
            proxy = next(proxies_iterator)

        url = f'{source_url}{zip_code}'
        if url not in temp:
            response = requests.get(url=url, headers=headers)
            time.sleep(1)
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                rows = soup.find('div', class_='row results-content').find_all('a', class_='result-name')
                quantity = len(rows)
            except Exception:
                quantity = 0
            data_dict = {'Quantity': [quantity]}
            df = pd.DataFrame(data_dict)
            global start
            with pd.ExcelWriter(f'data/data-health.xlsx', mode='a', engine='openpyxl',
                                if_sheet_exists='overlay') as writer:
                df.to_excel(writer, startrow=start, startcol=3, index=False, header=False)
            with open('data/temp.txt', 'a', encoding='utf-8') as file:
                file.write(url + '\n')
            start += 1
            print(f'[INFO] {zip} OK | {start}')

    global flag
    flag = False


if __name__ == '__main__':
    # Proxies requests format
    with open('data/proxies.json', 'r', encoding='utf-8') as json_file:
        proxies_sync = json.load(json_file)
    proxies_iterator = iter(proxies_sync)
    # Temp
    if not os.path.exists('data/temp.txt'):
        with open('data/temp.txt', 'w', encoding='utf-8') as txt_file:
            txt_file.write('')
    # Other Data
    with open('data/ontario-zip.txt', 'r', encoding='utf-8') as txt_file:
        raw_data = txt_file.readlines()
        zips = [item.replace('\n', '') for item in raw_data]
    sources = [
        'https://www.healthprofs.com/ca/naturopaths?search=',
        'https://www.healthprofs.com/ca/nutritionists-dietitians?search='
    ]
    flag = True
    start = 1
    while True:
        if flag:
            try:
                # Need to open temp file and read it as list
                with open('data/temp.txt', 'r', encoding='utf-8') as txt_file:
                    raw_data = txt_file.readlines()
                    temp = [item.replace('\n', '') for item in raw_data]
                for source in sources:
                    get_data(source)
            except Exception as ex:
                time.sleep(5)
                print(ex)
                continue
        else:
            break

