import requests
import json
from bs4 import BeautifulSoup
import random
import time
from websiteData import headers


def web_site_tester():
    # Check number or requests
    for i in range(1, 2):
        if i % 10 == 0:
            time.sleep(1)
        proxy = random.choice(proxies_sync)
        response = requests.get(url=url, headers=headers, proxies=proxy)
        print(f'{response.status_code} WITH {proxy}')
        # Try to write an HTML file and look what will happen
        with open(f'DATA/test_{i}.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        # Try to write an JSON file and look what will happen
        # with open(f'DATA/test_{i}.json', 'w', encoding='utf-8') as file:
        #     json.dump(response, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # Proxies requests format
    with open('DATA/proxies.json', 'r', encoding='utf-8') as json_file:
        proxies_sync = json.load(json_file)
    # Set parameters and let's go!
    url = ''
    web_site_tester()

