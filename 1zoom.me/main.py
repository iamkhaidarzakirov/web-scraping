import random
import requests
from bs4 import BeautifulSoup
from requirements import *
import time
import json


def get_data():
    headers = {

    }
    domain = 'https://www.1zoom.me'
    category_name = 'sweden-cities'
    category_link = f'/en/Sweden/t2/'  # add any category you want to download / simple pagination with loop
    for i in range(1, 2):  # number of pages
        url = f'{domain}{category_link}{i}'
        response = requests.get(url, headers=headers).text
        with open(fr'data/{category_name}.html', 'w', encoding='utf-8') as file:
            file.write(response)
            print('File is saved as html')

        with open(fr'data/{category_name}.html', 'r') as file:
            response = file.read()
            print('File is opened and ready to analyzing')

        soup = BeautifulSoup(response, 'lxml')
        main_block = soup.find('div', id='suda')
        all_pi_divs = main_block.find_all('div', class_='pi')
        img_urls = []
        j = 1  # counter to visualize progress
        for item in all_pi_divs:
            link = item.find('a').get('href')
            url = f'{domain}{link}'
            img_urls.append(url)
            print(f'URL_{j} of {i} page is added to list')
            j = j + 1
        # Collecting high quality images urls
        hq_img_urls = []
        for url in img_urls:
            response = requests.get(url, headers=headers).text
            soup = BeautifulSoup(response, 'lxml')
            img_show_bar = soup.find('div', id='show')
            hq_link = img_show_bar.find('a').get('href')
            hq_img_url = f'{url}{hq_link}'
            hq_img_urls.append(hq_img_url)
        with open(fr'data/hq_img_urls_page_{i}.json', 'w', encoding='utf-8') as file:
            json.dump(hq_img_urls, file, indent=4, ensure_ascii=False)  # saving links on hard drive
        print(f'File: hq_img_links_page_{i}.json is created')

        with open(fr'data/hq_img_urls_page_{i}.json', 'r', encoding='utf-8') as file:
            hq_img_urls = json.load(file)
        k = 1  # counter to visualize progress
        for url in hq_img_urls:
            try:
                response = requests.get(url=url, headers=headers).text
                soup = BeautifulSoup(response, 'lxml')
                img_div = soup.find('div', id='image')
                image_url = img_div.find('a').get('href')
                image_bytes = requests.get(url=image_url, headers=headers).content

                with open(fr'data/{category_name}_{k}.jpg', 'wb') as file:
                    file.write(image_bytes)
                print(f'Image {category_name}_{k} is downloaded')
                k += 1
                time.sleep(random.randrange(1, 3))
            except Exception as ex:

                print(f'We have: {ex} here: {image_url}')
                k += 1
                time.sleep(random.randrange(1, 3))

    print('The information collecting completed')


def main():
    get_data()


if __name__ == "__main__":
    main()










