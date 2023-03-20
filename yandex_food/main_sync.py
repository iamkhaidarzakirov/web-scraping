import requests
from websiteData import headers
from web_scraping_utils import add_a_row_to_xlsx
import time
import json
import os
import pandas as pd


def get_all_events(api) -> None:
    response = requests.post(
        url=api,
        headers=headers,
        json=json_data,
    )
    # Post request returns a JSON with categories of shops, restaurants and other
    with open(f'data/rests_list.json', 'w', encoding='utf-8') as local_file:
        json.dump(response.json(), local_file, indent=4, ensure_ascii=False)


def get_menu_urls(data: dict) -> None:
    places_block = data['data']['places_lists']
    menu_urls = []
    for block in places_block:
        places_list = block['payload']['places']
        for place in places_list:
            slug = place['slug']
            url_1 = f'https://eda.yandex.ru/api/v2/menu/retrieve/{slug}?regionId=51&autoTranslate=false'
            menu_urls.append(url_1)
    with open('data/menu_api_queries.json', 'w', encoding='utf-8') as local_file:
        json.dump(menu_urls, local_file, indent=4, ensure_ascii=False)


def get_rests_urls(data: dict) -> None:
    places_block = data['data']['places_lists']
    rests_urls = []
    for block in places_block:
        places_list = block['payload']['places']
        for place in places_list:
            slug = place['slug']
            url_2 = f'https://eda.yandex.ru/api/v2/catalog/{slug}?regionId=51&shippingType=delivery'
            rests_urls.append(url_2)

    with open('data/rests_api_queries.json', 'w', encoding='utf-8') as local_file:
        json.dump(rests_urls, local_file, indent=4, ensure_ascii=False)


def get_menu_data(data: list) -> None:
    # Extra information
    domain = 'https://eda.yandex.ru'
    path = 'data/kursk_restaurants.xlsx'

    for url in data:
        if url not in temp:
            # Create sheet_title to write each restaurant data in separate workbook
            sheet_title = url.split('?')[0].split('/')[-1]
            # Some apps don't support titles more than 31 chars
            if len(sheet_title) > 30:
                sheet_title = list(sheet_title)[0:30]
                sheet_title = ''.join(sheet_title)

            data_dict = {
                'Название': [],
                'Категория': [],
                'Описание': [],
                'Цена': [],
                'Ссылка на изображение': []
            }

            response = requests.get(url=url, headers=headers).json()
            categories = response['payload']['categories']
            for category in categories:
                category_name = category['name']
                items = category['items']
                for item in items:
                    name = item['name']
                    try:
                        description = item['description']
                    except KeyError:
                        description = ''
                    try:
                        price = item['price']
                    except KeyError:
                        price = ''
                    try:
                        image_url = domain + item['picture']['uri']
                    except KeyError:
                        image_url = ''

                    data_dict['Название'].append(name)
                    data_dict['Категория'].append(category_name)
                    data_dict['Описание'].append(description)
                    data_dict['Цена'].append(price)
                    data_dict['Ссылка на изображение'].append(image_url)

            df = pd.DataFrame(data_dict)
            add_a_row_to_xlsx(path=path, df=df, sheet_title=sheet_title)

            with open('data/temp.txt', 'a', encoding='utf-8') as local_file:
                local_file.write(url + '\n')

            print(f'[INFO]: {url} OK')
            time.sleep(1)

    global flag
    flag = False


def add_extra_data(data: list) -> None:
    domain = 'https://eda.yandex.ru'
    path = 'data/kursk_restaurants.xlsx'

    for url in data:
        if url not in temp:
            response = requests.get(url=url, headers=headers).json()

            place = response['payload']['foundPlace']['place']
            name = place['name']
            sheet_title = place['slug']
            # Some apps don't support titles more than 31 chars
            if len(sheet_title) > 30:
                sheet_title = list(sheet_title)[0:30]
                sheet_title = ''.join(sheet_title)
            try:
                rating = place['rating']
            except KeyError:
                rating = ''
            try:
                img_link = domain + place['picture']['uri']
            except KeyError:
                img_link = ''
            try:
                description = place['footerDescription']
            except KeyError:
                description = ''
            try:
                address = place['address']['short']
            except KeyError:
                address = ''
            try:
                link = place['sharedLink']
            except KeyError:
                link = ''

            data_dict = {
                'Название заведения': [name],
                'Рейтинг': [rating],
                'Описание': [description],
                'Адрес': [address],
                'Ссылка на изображение': [img_link],
                'Ссылка в ЯндексЕда': [link],
            }
            df = pd.DataFrame(data_dict)
            with pd.ExcelFile(path, engine='openpyxl') as reader:
                sheet_titles = reader.sheet_names
                if sheet_title in sheet_titles:
                    info = reader.parse(sheet_name=sheet_title)
                    rows = len(info)
                    start = rows + 2
                    with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                        df.to_excel(writer, startrow=start, sheet_name=sheet_title, index=False)
                else:
                    pass
            with open('data/temp.txt', 'a', encoding='utf-8') as local_file:
                local_file.write(url + '\n')
            print(f'[INFO]: {url} OK')
            time.sleep(1)

    global flag
    flag = False


if __name__ == '__main__':
    # Choose region to yandex food delivery / Here is Kursk city.
    json_data = {
        'region_id': 51,
    }

    if not os.path.exists('data/temp.txt'):
        with open('data/temp.txt', 'w', encoding='utf-8') as temp_file:
            temp_file.write('')

    if not os.path.exists('data/rests_list.json'):
        api_url = 'https://eda.yandex.ru/eats/v1/layout-constructor/v1/layout'
        get_all_events(api=api_url)

    if not os.path.exists('data/menu_api_queries.json'):
        with open('data/rests_list.json', 'r', encoding='utf-8') as file:
            rests = json.load(file)
        get_menu_urls(data=rests)

    if not os.path.exists('data/rests_api_queries.json'):
        with open('data/rests_list.json', 'r', encoding='utf-8') as file:
            rests = json.load(file)
        get_rests_urls(data=rests)
    # Collect menus of restaurants
    print(f'[INFO]: MENUS DATA GATHERING')
    with open('data/menu_api_queries.json', 'r', encoding='utf-8') as file:
        rests_menu_urls = json.load(file)

    flag = True
    while True:
        if flag:
            try:
                with open('data/temp.txt', 'r', encoding='utf-8') as temp_file:
                    raw_data = temp_file.readlines()
                    temp = [item.replace('\n', '') for item in raw_data]
                get_menu_data(data=rests_menu_urls)

            except Exception as e:
                print(f'[ERROR]: {e}')
                time.sleep(1)
        else:
            break

    # Collect restaurants information and add to existing spreadsheet
    print(f'[INFO]: RESTAURANTS DATA GATHERING')
    with open('data/rests_api_queries.json', 'r', encoding='utf-8') as file:
        rests_info_urls = json.load(file)

    flag = True
    while True:
        if flag:
            try:
                with open('data/temp.txt', 'r', encoding='utf-8') as temp_file:
                    raw_data = temp_file.readlines()
                    temp = [item.replace('\n', '') for item in raw_data]
                add_extra_data(data=rests_info_urls)

            except Exception as e:
                print(f'[ERROR]: {e}')
                time.sleep(1)
        else:
            break
