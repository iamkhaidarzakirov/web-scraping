import requests
import json
from websiteData import headers
from bs4 import BeautifulSoup


def website_tester() -> None:
    """Function sends many requests to server and checks response"""

    for i in range(1, 2):
        url = f''
        global have_proxies
        if have_proxies:
            global proxies_iterator
            try:
                proxy = next(proxies_iterator)
            except StopIteration:
                proxies_iterator = iter(proxies_sync)
                proxy = next(proxies_iterator)
        else:
            proxy = None
        response = requests.post(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        print(f'{response.status_code} WITH {proxy}')
        print(soup.title)
        # Check parameter
        ishtml = False  # Server side rendering — request returns html
        isjson = False  # Client side rendering — request returns json / Request to API
        if ishtml:
            # Try to save an HTML file and look what will happen
            with open(f'test/test.html', 'w', encoding='utf-8') as file:
                file.write(response.text)
        if isjson:
            with open(f'test/test.json', 'w', encoding='utf-8') as file:
                json.dump(response.json(), file, indent=4, ensure_ascii=False)



if __name__ == '__main__':
    # Set the required parameter
    have_proxies = False
    if have_proxies:
        # Proxies requests format
        with open('DATA/ru-proxies-requests.json', 'r', encoding='utf-8') as json_file:
            proxies_sync = json.load(json_file)
            proxies_iterator = iter(proxies_sync)

    website_tester()
