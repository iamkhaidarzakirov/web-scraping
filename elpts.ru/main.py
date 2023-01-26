import json
import time
import undetected_chromedriver as uc
import pandas as pd
import datetime
import os


def get_new_records():
    options = uc.options.ChromeOptions()
    options.add_argument('--headless')
    with uc.Chrome(options=options) as browser:
        print(f'[INFO] => BROWSER IS INITIALED SUCCESSFUL')
        url = f'https://portal.elpts.ru/ncher/api/1/esbkts/search?head=%D0%A2%D0%A1&dateFrom={curr_date}&dateTo={curr_date}&page=1&size=25'
        browser.get(url)
        response = browser.page_source
        content = browser.find_element(by='tag name', value='pre').text
        parsed_json = json.loads(content)
        if len(parsed_json) > 0:
            for item in parsed_json:
                # Check repeats
                unique_number = item['number']
                if unique_number not in temp:
                    data_dict = {
                        'Регистрационный номер свидетельства': [item['number']],
                        'Марка транспортного средства': [item['mark']],
                        'Тип транспортного средства': [item['type']],
                        'Статус': [item['status']],
                        'Дата оформления': [item['activeDate']]
                    }
                    # Check the table file and append new data if table has already exist
                    df = pd.DataFrame(data_dict)
                    if not os.path.exists('data/TC_sheet.xlsx'):
                        df.to_excel('data/TC_sheet.xlsx', index=False)
                    else:
                        with pd.ExcelFile('data/TC_sheet.xlsx', engine='openpyxl') as reader:
                            info = reader.parse()
                            rows = len(info)
                            start = rows + 1
                            with pd.ExcelWriter('data/TC_sheet.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                                df.to_excel(writer, startrow=start, index=False, header=False)
                    with open(temp_file_path, 'a', encoding='utf-8') as file:
                        file.write(unique_number + '\n')
                else:
                    continue
            print(f'[INFO] => DATE: {curr_date} HAS ANALYZED')
        else:
            print(f'[INFO] => NO DATA ON {curr_date}')
            pass


if __name__ == '__main__':
    # Create list to check and delete unusable old date paths
    if not os.path.exists(f'data/parameters.json'):
        with open('data/parameters.json', 'w', encoding='utf-8') as json_file:
            temp_list = []
            json.dump(temp_list, json_file, indent=4, ensure_ascii=False)
    with open('data/parameters.json', 'r', encoding='utf-8') as json_file:
        temp_list = json.load(json_file)
    while True:
        try:
            curr_date = str(datetime.date.today().strftime('%Y-%m-%d'))
            temp_file_path = f'data/temp_{curr_date}.txt'
            # Check old date temp file
            if temp_file_path not in temp_list and len(temp_list) == 1:
                old_temp_path = temp_list[0]
                os.remove(old_temp_path)
            # Create new date temp file
            if not os.path.exists(temp_file_path):
                with open(temp_file_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write('')
                with open('data/parameters.json', 'w', encoding='utf-8') as json_file:
                    temp_list = [temp_file_path]
                    json.dump(temp_list, json_file, indent=4, ensure_ascii=False)
            with open(temp_file_path, 'r', encoding='utf-8') as txt_file:
                data = txt_file.readlines()
                temp = [item.replace('\n', '') for item in data]
            get_new_records()
            print('[INFO] => STANDBY MODE 1 MINUTE ')
            time.sleep(60)
        except Exception as ex:
            print(f'[ERROR] => {ex}')
            time.sleep(30)
            continue
