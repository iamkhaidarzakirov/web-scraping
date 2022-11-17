import random
import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json
import csv

user_agent = fake_useragent.UserAgent().random
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q='
              '0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': user_agent
}
domain = 'https://www.labirint.ru/genres/2308'
url = f'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table'
response = requests.get(url=url, headers=headers).text
soup = BeautifulSoup(response, 'lxml')
pages_count = soup.find('div', class_='pagination-number__right').find_all('a')[-1].text  # Gathering number of pages value
all_data_list = []  # Need to create list in advance
# The table headers are creating in advance
with open('data/data_table.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(
        ('name', 'status', 'publisher', 'price_old', 'price_new', 'discount', 'authors', 'img_url')
    )

for i in range(1, int(pages_count) + 1):
    try:
        url = f'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={i}'
        response = requests.get(url=url, headers=headers).text
        # To be on the safe side need to save file with web page in storage
        with open(f'data/index_{i}.html', 'w', encoding='utf-8') as file:
            file.write(response)
        with open(f'data/index_{i}.html', 'r', encoding='utf-8') as file:
            response = file.read()

        soup = BeautifulSoup(response, 'lxml')
        books_items = soup.find('tbody', class_='products-table__body').find_all('tr')

        for item in books_items:
            try:
                name = item.find('td', class_='col-sm-4').text.strip()
            except Exception as ex:
                print(ex, f'error on page_{i}', sep='\n')
                name = 'no information'
            try:
                authors = item.find('td', class_='col-sm-2').text.strip()
            except Exception as ex:
                print(ex, f'error on page_{i}', sep='\n')
                authors = 'no information'
            try:
                publisher = item.find('td', class_='products-table__pubhouse').text.strip().replace('\n', '')
            except Exception as ex:
                print(ex)
                publisher = 'no information'
            try:
                price_old = item.find('td', class_='products-table__price').find('span', class_='price-old').text.strip().replace(' ', '')
            except Exception as ex:
                print(ex, f'error on page_{i}', sep='\n')
                price_old = 'no information'
            try:
                price_new = item.find('td', class_='products-table__price'). find('span', class_='price-val').text.strip().replace(' ', '').replace('₽', '')
            except Exception as ex:
                print(ex, f'error on page_{i}', sep='\n')
                price_new = 'no information'
            try:
                discount = round((int(price_old) - int(price_new)) * 100 / int(price_old))
            except Exception as ex:
                print(ex, f'error on page_{i}', sep='\n')
                discount = 'no information'
            try:
                status = item.find('td', class_='product-table__available').text.strip()
            except Exception as ex:
                print(ex, f'error on page_{i}', sep='\n')
                status = 'no information'
            try:
                img_url = item.find('div', class_='product-icons-inner').find('a', class_='icon-compare').get('data-image')
            except Exception as ex:
                print(ex, f'error on page_{i}', sep='\n')
                img_url = 'no information'
            data_dict = {
                'name': name,
                'status': status,
                'publisher': publisher,
                'price_old': price_old,
                'price_new': price_new,
                'discount': discount,
                'authors': authors,
                'img_url': img_url
            }
            all_data_list.append(data_dict)
            with open('data/data_table.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (name, status, publisher, price_old, price_new, discount, authors, img_url)
                )
        print(f'{i} page is added...')
        time.sleep(random.randrange(2, 3))
    except Exception as ex:
        print(ex)
        print(f'Here: {url}')

with open('data/data_file.json', 'w', encoding='utf-8') as file:
    json.dump(all_data_list, file, indent=4, ensure_ascii=False)
print('Data gathering is done')