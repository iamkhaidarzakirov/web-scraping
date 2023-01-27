import json
import time
import undetected_chromedriver as uc
import pandas as pd
import datetime
import os


def get_new_records(browser):
    def parse_response():
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
                            with pd.ExcelWriter('data/TC_sheet.xlsx', engine='openpyxl', mode='a',
                                                if_sheet_exists='overlay') as writer:
                                df.to_excel(writer, startrow=start, index=False, header=False)
                    with open(temp_file_path, 'a', encoding='utf-8') as file:
                        file.write(unique_number + '\n')
                else:
                    continue
            print(f'[INFO] => DATE: {curr_date} PAGE {i} HAS ANALYZED')
        else:
            print(f'[INFO] => NO DATA ON {curr_date}')
            nonlocal check_point
            check_point = False

    if counter == 1:
        i = 1
        check_point = True
        while True:
            if check_point:
                url = f'https://portal.elpts.ru/ncher/api/1/esbkts/search?head=%D0%A2%D0%A1&dateFrom={input_date}&dateTo={curr_date}&page={i}&size=25'
                parse_response()
                i += 1
            else:
                break

    else:
        i = 1
        url = f'https://portal.elpts.ru/ncher/api/1/esbkts/search?head=%D0%A2%D0%A1&dateFrom={curr_date}&dateTo={curr_date}&page=1&size=25'
        parse_response()


if __name__ == '__main__':
    #
    input_date = input('Введите дату в формате ГГГГ-ММ-ДД с которой нужно начать сбор: ')
    # Create list to check and delete unusable old date paths
    if not os.path.exists(f'data/parameters.json'):
        with open('data/parameters.json', 'w', encoding='utf-8') as json_file:
            temp_list = []
            json.dump(temp_list, json_file, indent=4, ensure_ascii=False)
    with open('data/parameters.json', 'r', encoding='utf-8') as json_file:
        temp_list = json.load(json_file)
    counter = 1
    while True:
        try:
            options = uc.options.ChromeOptions()
            options.add_argument('--headless')
            with uc.Chrome(options=options) as driver:
                print(f'[INFO] => BROWSER IS INITIALED SUCCESSFUL')
                curr_date = str(datetime.date.today().strftime('%Y-%m-%d'))
                temp_file_path = f'data/temp_{curr_date}.txt'
                # Check old date temp file
                if curr_date not in temp_list and len(temp_list) == 1:
                    old_temp_date = temp_list[0]
                    old_temp_path = f'data/temp_{old_temp_date}.txt'
                    os.remove(old_temp_path)
                # Create new date temp file
                if not os.path.exists(temp_file_path):
                    with open(temp_file_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write('')
                    with open('data/parameters.json', 'w', encoding='utf-8') as json_file:
                        temp_list = [curr_date]
                        json.dump(temp_list, json_file, indent=4, ensure_ascii=False)
                with open(temp_file_path, 'r', encoding='utf-8') as txt_file:
                    data = txt_file.readlines()
                    temp = [item.replace('\n', '') for item in data]
                get_new_records(driver)
                counter += 1
                print('[INFO] => STANDBY MODE 1 MINUTE ')
                time.sleep(60)
        except Exception as ex:
            print(f'[ERROR] => {ex}')
            time.sleep(30)
            continue
