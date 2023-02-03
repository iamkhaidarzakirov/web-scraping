import requests
import json
import random
import time
import pandas
from websiteData import headers


def get_json():
    i = 1
    while True:
        try:
            params = {
                'language': 'en-GB',
                'q': '',
                'orderBy': 'name',
                'pageNumber': f'{i}',
                'pageSize': '25',
                'showJumpLabels': 'true',
                'findEventVariable': 'AMBIENTE',
            }
            response = requests.get(
                'https://exhibitorsearch.messefrankfurt.com/service/esb/2.1/search/exhibitor',
                params=params,
                headers=headers,
            ).json()
            if len(response['result']['hits']) == 0:
                print(f'[INFO] => THE PAGE {i} IS EMPTY')
                break
            with open(f'data/ambiente_page_{i}_data.json', 'w', encoding='utf-8') as file:
                json.dump(response, file, indent=4, ensure_ascii=False)
            print(f'[INFO] => PAGE {i} IS DONE')
            i += 1
            time.sleep(random.randrange(1, 3))
        except Exception as ex:
            print(ex)
            break


def get_data_from_json():
    i = 1
    data_table = {
        'Name of the brand': [],
        'Mail address': [],
        'Phone number': [],
        'Country': []

    }
    all_pages_data = []
    while True:
        try:
            with open(f'data/ambiente_page_{i}_data.json', 'r', encoding='utf-8') as file:
                response = json.load(file)
            hits = response['result']['hits']
            for hit in hits:
                data_dict = {}
                name = hit['exhibitor']['name']
                country = hit['exhibitor']['address']['country']['label']
                phone = hit['exhibitor']['address']['tel']
                mail = hit['exhibitor']['address']['email']
                # Collecting data at the table excel
                data_table['Name of the brand'].append(name)
                data_table['Mail address'].append(mail)
                data_table['Phone number'].append(phone)
                data_table['Country'].append(country)
                # Collecting data to json
                data_dict['Name of the brand'] = name
                data_dict['Mail address'] = mail
                data_dict['Phone number'] = phone
                data_dict['Country'] = country
                all_pages_data.append(data_dict)
                print(f'[INFO] => PAGE {i} DATA GATHERING IS DONE')
            i += 1
        except Exception as ex:
            print(ex)
            break
    with open('data/result_data.json', 'w', encoding='utf-8') as file:
        json.dump(all_pages_data, file, indent=4, ensure_ascii=False)
    df = pandas.DataFrame(data_table)
    df.to_excel('data/result_data_inTable.xlsx')


def main():
    get_json()
    get_data_from_json()


if __name__ == '__main__':
    main()
