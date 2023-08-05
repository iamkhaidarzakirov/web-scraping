"""Module contains the functions which may using in routine web scraping projects"""
import pandas as pd
import os
import json
import re
from config.settings import PROXIES_DIR, SHEETS_DIR


def add_a_row_to_xlsx(file_name: str, source: dict, sheet_title: str = 'Sheet1') -> None:
    """Using this function you can add one / or many (depending on DataFrame) strings to .xlsx spreadsheet.

    Also, it allows to create table with many sheets and add a row to specific sheet
    depending on which sheet name had specified."""
    df = pd.DataFrame(source)
    path = f'{SHEETS_DIR}/{file_name}'
    if not os.path.exists(path):
        df.to_excel(path, sheet_name=sheet_title, index=False)
    else:
        with pd.ExcelFile(path, engine='openpyxl') as reader:
            sheet_titles = reader.sheet_names
            if sheet_title in sheet_titles:
                info = reader.parse(sheet_name=sheet_title)
                rows = len(info)
                start = rows + 1
                with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, startrow=start, sheet_name=sheet_title, index=False, header=False)
            else:
                with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, startrow=0, sheet_name=sheet_title, index=False)


def create_proxies_json(proxies_format: str, source_path: str, file_name: str) -> None:
    """Function allows to create a json file with proxies depending on which proxies format had specified.

    — Currently, the function supports to reformat proxies to aiohttp and requests proxies_utils formats.
    — This function is configured to operate with proxies in the format provided by the site proxy6.net:
        IP:PORT:LOGIN:PASSWORD
    — The source file must be in .txt format; each proxy on a separate line"""

    with open(source_path) as file:
        raw_data = file.readlines()
        wrong_format = [item.replace('\n', '') for item in raw_data]

    proxies_list = []
    for item in wrong_format:
        container = item.split(':')
        password = container[-1]
        login = container[-2]
        ip = container[0]
        port = container[1]

        value = f'http://{login}:{password}@{ip}:{port}'
        if proxies_format == 'requests':
            key = 'https'
            proxy_dict = {key: value}
            proxies_list.append(proxy_dict)
            with open(f'{PROXIES_DIR}/{file_name}', 'w', encoding='utf-8') as file:
                json.dump(proxies_list, file, indent=4, ensure_ascii=False)
        elif proxies_format == 'aiohttp':
            proxies_list.append(value)
            with open(f'{PROXIES_DIR}/{file_name}', 'w', encoding='utf-8') as file:
                json.dump(proxies_list, file, indent=4, ensure_ascii=False)
        else:
            print('[ERROR] Unknown format. Enter "aiohttp" or "requests", please.')
            break
        print(f'[INFO] {item} -> {value}')


def del_special_symbols(some_string: str) -> str:
    """Function deletes all special symbols in string using re module"""

    edited_string = re.sub(r"[^\w\s]+|\d+", r'', string=some_string).strip()
    return edited_string


def count_unique_sites(data: list) -> dict:
    """Function counts unique sites by domain in websites list"""

    counter = {}
    for item in data:
        domain = item.split('/')[2]
        counter[domain] = counter.get(domain, 0) + 1

    return counter


def sort_unique_sites(data: list) -> None:
    """Function collects websites with the same domain to list and writes to json"""

    sorter = {}
    for item in data:
        domain = item.split('/')[2]
        sorter[domain] = []
        for site in data:
            if domain in site:
                sorter[domain].append(site)

    with open('unique_sites.json', 'w', encoding='utf-8') as file:
        json.dump(sorter, file, indent=4, ensure_ascii=False)







