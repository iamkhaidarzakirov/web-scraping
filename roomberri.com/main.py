import random
import time
import req_deb
from bs4 import BeautifulSoup
import csv
import re


def main():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/'
                  'apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/107.0.0.0 Safari/537.36'
    }
    subcategories = ['kipr', 'yugo-vostochnuyu-aziyu', 'germaniya', 'monako', 'izrail', 'moskva', 'london', 'majami']
    domain = 'https://roomberi.com/'
    with open('hotels_data_table.csv', 'w', newline='',  encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            (
                'Название',
                'Стоимость',
                'Город',
                'Площадь',
                'Категория',
                'Подкатегория',
                'Описание',
                'Основные преимущества',
                'Тип объекта',
                'Цена за м2',
                'Внутреннее пространство',
                'Оснащение',
                'Расходы по сделке',
                'Расположение',
                'Ссылка на Видео',
                'Заглавное фото',
                'Ссылки на изображения в карусели',
            )
        )

    all_hotels_url = []
    for subcategory in subcategories:
        subcategory_url = f'https://roomberi.com/nedvizhimost/{subcategory}'
        response = req_deb.requests_debugging(url=subcategory_url, headers=headers, retry=2).text
        soup = BeautifulSoup(response, 'lxml')
        try:
            pages = int(soup.find('ul', class_='pagination').find('a', string='Последняя').get('href').split('=')[1])
            # print(pages)
        except Exception as ex:
            print(ex)
            pages = 1
            # print(pages)
        for i in range(1, pages + 1):
            try:
                url = f'https://roomberi.com/nedvizhimost/{subcategory}/?page={i}'
                response = req_deb.requests_debugging(url=url, headers=headers, retry=2).text
                soup = BeautifulSoup(response, 'lxml')
                main_block = soup.find('div', id='products')
                hotels = main_block.find_all('div', class_='col-sm-12')
                # Gathering data from main block
                for hotel in hotels:
                    hotel_url = domain + hotel.find('a').get('href')
                    all_hotels_url.append(hotel_url)
                    name = hotel.find('h3').text.strip()
                    cost = hotel.find_all('div', class_='pricelist')[0].find('b').text.strip()
                    city = hotel.find_all('div', class_='pricelist')[1].find('b').text.strip()
                    square = hotel.find_all('div', class_='pricelist')[2].text.strip()
                    category = 'Недвижимость'
                    podcategoria = subcategory

                    # Gathering data from hotel url
                    response = req_deb.requests_debugging(url=hotel_url, headers=headers, retry=2).text
                    soup = BeautifulSoup(response, 'lxml')
                    # Description
                    try:
                        description_list = []
                        start_point = soup.find('h3', string=re.compile('Описание'))
                        while True:
                            info = start_point.find_next()
                            if info.name == 'h3':
                                break
                            text = info.text.strip()
                            description_list.append(text)
                            start_point = info
                        description = ' '.join(description_list).replace('\n', ' ')

                    except Exception as ex:
                        print(f'[ERROR]: {ex}')
                        description = 'Отсутствует'
                    try:
                        cost_for_meter = soup.find('span', class_='ploshad').text.strip()
                    except Exception as ex:
                        print(f'[ERROR]: {ex}')
                        cost_for_meter = ' '

                    # Advantages
                    try:
                        advantages_list = []
                        start_point = soup.find('h3', string=re.compile('Основные преимущества'))
                        while True:
                            info = start_point.find_next()
                            if info.name == 'h3':
                                break
                            elif info.name == 'ul':
                                text = info.text.strip()
                                if text not in advantages_list:
                                    advantages_list.append(text)
                                start_point = info
                                break
                            else:
                                text = info.text.strip()
                                if text not in advantages_list:
                                    advantages_list.append(text)
                                start_point = info

                        advantages = ' '.join(advantages_list).replace('\n', ' ')
                    except Exception as ex:
                        print(f'[ERROR]: {ex}')
                        advantages = 'Отсутствует'

                    # Inside space
                    try:
                        spaces_list = []
                        start_point = soup.find('h3', string=re.compile('Внутреннее пространство'))
                        while True:
                            info = start_point.find_next()
                            if info.name == 'h3':
                                break
                            elif info.name == 'ul':
                                text = info.text.strip()
                                if text not in spaces_list:
                                    spaces_list.append(text)
                                start_point = info
                                break
                            else:
                                text = info.text.strip()
                                if text not in spaces_list:
                                    spaces_list.append(text)
                                start_point = info
                        inside_spaces = ' '.join(spaces_list).replace('\n', ' ')
                    except Exception as ex:
                        print(f'[ERROR]: {ex}')
                        inside_spaces = 'Отсутствует'

                    # Equipment
                    try:
                        equipment_list = []
                        start_point = soup.find('h3', string=re.compile('Оснащение'))
                        while True:
                            info = start_point.find_next()
                            if info.name == 'h3':
                                break
                            elif info.name == 'ul':
                                text = info.text.strip()
                                if text not in equipment_list:
                                    equipment_list.append(text)
                                start_point = info
                            else:
                                text = info.text.strip()
                                if text not in equipment_list:
                                    equipment_list.append(text)
                                start_point = info
                        equipment = ' '.join(equipment_list).replace('\n', ' ')
                    except Exception as ex:
                        print(f'[ERROR]: {ex}')
                        equipment = 'Отсутствует'

                    # Expenses
                    try:
                        expenses_list = []
                        start_point = soup.find('h3', string=re.compile('Расходы по сделке'))
                        while True:
                            info = start_point.find_next()
                            if info.name == 'h3':
                                break
                            elif info.name == 'ul':
                                text = info.text.strip()
                                if text not in expenses_list:
                                    expenses_list.append(text)
                                start_point = info
                            else:
                                text = info.text.strip()
                                if text not in expenses_list:
                                    expenses_list.append(text)
                                start_point = info
                        expenses = ' '.join(expenses_list).replace('\n', ' ')
                    except Exception as ex:
                        print(f'[ERROR]: {ex}')
                        expenses = 'Отсутствует'

                    # Location
                    try:
                        location_list = []
                        start_point = soup.find('h3', string=re.compile('Расположение'))
                        while True:
                            info = start_point.find_next()
                            if info.name == 'h3' or info.name == 'div':
                                break
                            elif info.name == 'ul':
                                text = info.text.strip()
                                if text not in location_list:
                                    location_list.append(text)
                                start_point = info
                            else:
                                text = info.text.strip()
                                if text not in location_list:
                                    location_list.append(text)
                                start_point = info
                        location = ' '.join(location_list).replace('\n', ' ')
                    except Exception as ex:
                        print(f'[ERROR]: {ex}')
                        location = 'Отсутствует'
                    # Video clip
                    try:
                        video_url = domain + soup.find('a', class_='ytp-impression-link').get('href')
                    except Exception as ex:
                        print(f'[ERROR]: {ex}')
                        video_url = 'Нет видеоролика'
                    # Main photo
                    try:
                        main_img_url = domain + soup.find('img', class_='bigimg').get('src')
                    except Exception as ex:
                        print(f'[ERROR]: {ex}')
                        main_img_url = 'Нет заглавной фотографии'
                    # All photo urls
                    all_photo = soup.find_all('a', attrs={'data-title': f'{name}'})
                    all_img_list = []
                    for photo in all_photo:
                        img_url = domain + photo.get('href')
                        all_img_list.append(img_url)
                    all_img_urls = ', '.join(all_img_list)

                    with open('hotels_data_table.csv', 'a', newline='', encoding='utf-8') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(
                            (
                                name,
                                cost,
                                city,
                                square,
                                category,
                                podcategoria,
                                description,
                                advantages,
                                'Нет информации',
                                cost_for_meter,
                                inside_spaces,
                                equipment,
                                expenses,
                                location,
                                video_url,
                                main_img_url,
                                all_img_urls
                            )
                        )
                time.sleep(random.randrange(1))
            except Exception as ex:
                print(f'[ERROR]: {ex} in {subcategory} in page {i}')
                continue


if __name__ == '__main__':
    main()

