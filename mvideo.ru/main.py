import requests
import json
import listing_config
import list_config
import prices_config
import pandas
import time


def get_all_pages_id():
    # Specify needed categoryID of products to get information about pages number
    params = {
        'categoryId': '65',
        'offset': '0',
        'limit': '24',
        'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
        'doTranslit': 'true',
    }
    session = requests.Session()
    response = session.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=listing_config.cookies,
                           headers=listing_config.headers).json()
    pages_count = response.get('body').get('total')
    all_pages_id = []
    for i in range(0, pages_count, 24):
        # Specify needed categoryID of products to get ID of every product
        params = {
            'categoryId': '65',
            'offset': f'{i}',
            'limit': '24',
            'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
            'doTranslit': 'true',
        }
        response = session.get('https://www.mvideo.ru/bff/products/listing', params=params,
                               cookies=listing_config.cookies,
                               headers=list_config.headers).json()
        page_product_ids = response.get('body').get('products')
        all_pages_id.append(page_product_ids)
        time.sleep(1)
    with open('data/all_pages_ids.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_pages_id, json_file, indent=4, ensure_ascii=False)


def get_products_data():
    with open('data/all_pages_ids.json', 'r', encoding='utf-8') as json_file:
        all_pages_ids = json.load(json_file)
    session = requests.Session()
    all_pages_properties = []
    for item in all_pages_ids:
        json_data = {
            'productIds': item,
            'mediaTypes': [
                'images',
            ],
            'category': True,
            'status': True,
            'brand': True,
            'propertyTypes': [
                'KEY',
            ],
            'propertiesConfig': {
                'propertiesPortionSize': 5,
            },
            'multioffer': True,
        }

        response = session.post('https://www.mvideo.ru/bff/product-details/list', cookies=list_config.cookies,
                                headers=list_config.headers,
                                json=json_data).json()
        all_pages_properties.append(response)
        time.sleep(1)
    with open('data/unsorted_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_pages_properties, json_file, indent=4, ensure_ascii=False)


def get_product_prices():
    with open('data/all_pages_ids.json', 'r', encoding='utf-8') as json_file:
        all_pages_ids = json.load(json_file)
    session = requests.Session()
    all_product_prices = []
    for item in all_pages_ids:
        params = {
            'productIds': f'{",".join(item)}',
            'addBonusRubles': 'true',
            'isPromoApplied': 'true',

        }
        response = session.get('https://www.mvideo.ru/bff/products/prices',
                               params=params, cookies=prices_config.cookies,
                               headers=prices_config.headers).json()
        all_product_prices.append(response)
        time.sleep(1)
    with open('data/unsorted_prices.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_product_prices, json_file, indent=4, ensure_ascii=False)


def sort_data():
    with open('data/all_pages_ids.json', 'r', encoding='utf-8') as file:
        all_pages_ids = json.load(file)
    with open('data/unsorted_data.json', 'r', encoding='utf-8') as file:
        unsorted_data = json.load(file)
    with open('data/unsorted_prices.json', 'r', encoding='utf-8') as file:
        unsorted_prices = json.load(file)
    sorted_data_list = []
    table = {
        'ID': [],
        'Название': [],
        'Модель': [],
        'Категория': [],
        'Изображения': [],
        'Базовая цена': [],
        'Цена со скидкой': []
    }

    for i in range(len(all_pages_ids)):
        for item in all_pages_ids[i]:
            product_description = {}
            for product in unsorted_data[i]['body']['products']:
                if item in product['productId']:
                    product_id = product['productId']
                    name = product['name']
                    model_name = product['modelName']
                    category = product['category']['name']
                    # Gathering images
                    img_domain = 'https://img.mvideo.ru/Pdb/big_pic/200/'
                    img_url_list = []
                    img_links = product['images']
                    for link in img_links:
                        url = img_domain + link.split('/')[1]
                        img_url_list.append(url)
                    # Gathering dictionary to json
                    product_description['product_id'] = product_id
                    product_description['name'] = name
                    product_description['model_name'] = model_name
                    product_description['category'] = category
                    product_description['img_urls'] = img_url_list
                    # Gathering dictionary to csv or excel
                    table['ID'].append(product_id)
                    table['Название'].append(name)
                    table['Модель'].append(model_name)
                    table['Категория'].append(category)
                    table['Изображения'].append(', '.join(img_url_list))

            for price in unsorted_prices[i]['body']['materialPrices']:
                if item in price['productId']:
                    base_price = price['price']['basePrice']
                    sale_price = price['price']['salePrice']
                    # Gathering dictionary to json
                    product_description['base_price'] = base_price
                    product_description['sale_price'] = sale_price
                    # Gathering dictionary to csv or excel
                    table['Базовая цена'].append(base_price)
                    table['Цена со скидкой'].append(sale_price)
            sorted_data_list.append(product_description)
    # Saving the results
    df = pandas.DataFrame(table)
    df.to_csv('data/csv_data_table.csv')
    with open('data/sorted_data.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_data_list, file, indent=4, ensure_ascii=False)


def main():
    get_all_pages_id()
    get_products_data()
    get_product_prices()
    sort_data()


if __name__ == '__main__':
    main()
