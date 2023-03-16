import requests
import json
from websiteData import headers


def website_tester() -> None:
    for i in range(1, 2):
        url = f''
        global proxies_iterator
        try:
            proxy = next(proxies_iterator)
        except StopIteration:
            proxies_iterator = iter(proxies_sync)
            proxy = next(proxies_iterator)
        response = requests.post(url=url, headers=headers)
        print(f'{response.status_code} WITH {proxy}')
        # Try to save an HTML file and look what will happen
        if i == 1:
            with open(f'test/test.html', 'w', encoding='utf-8') as file:
                file.write(response.text)


if __name__ == '__main__':
    # Proxies requests format
    with open('DATA/ru-proxies-requests.json', 'r', encoding='utf-8') as json_file:
        proxies_sync = json.load(json_file)
        proxies_iterator = iter(proxies_sync)
    # Set parameters and let's go!
    website_tester()
