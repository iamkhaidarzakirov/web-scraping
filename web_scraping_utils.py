import pandas as pd
import os
import json


# 1. This function adds a row into a spreadsheet without rewriting a file
def add_a_row_to_xlsx(path: str, df: pd.DataFrame, sheet_title: str = 'Sheet1') -> None:
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


# 2. This function creates json files with proxies in different formats
def create_proxies_json(proxies_format: str, source_path: str, result_path: str) -> None:
    # Open the file with Proxy6.net proxies list
    with open(source_path) as file:
        raw_data = file.readlines()
        wrong_format = [item.replace('\n', '') for item in raw_data]
    proxies_list = []
    for item in wrong_format:
        password = item.split(':')[-1]
        login = item.split(':')[-2]
        ip = item.split(':')[0]
        port = item.split(':')[1]
        value = f'http://{login}:{password}@{ip}:{port}'
        if proxies_format == 'requests':
            key = 'https'
            proxy_dict = {key: value}
            proxies_list.append(proxy_dict)
            with open(result_path, 'w', encoding='utf-8') as file:
                json.dump(proxies_list, file, indent=4, ensure_ascii=False)
        elif proxies_format == 'aiohttp':
            proxies_list.append(value)
            with open(result_path, 'w', encoding='utf-8') as file:
                json.dump(proxies_list, file, indent=4, ensure_ascii=False)
        else:
            print('[ERROR] Unknown format. Enter "aiohttp" or "requests", please.')
            break
        print(f'[INFO] {item} -> {value}')





