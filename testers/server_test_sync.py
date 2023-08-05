import requests
import json
from bs4 import BeautifulSoup
from config.settings import HTML_DIR, JSON_DIR


class SyncTester:
    """Sends many requests and check response status. Writes every 1st and 5th request content to a file(JSON/HTML)"""
    def __init__(
            self, url: str,
            is_html: bool,
            is_API: bool = False,
            headers: dict = None, cookies: dict = None, proxy: dict = None):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.proxy = proxy
        self.is_html = is_html
        self.is_API = is_API

    def start(self, i: int = 1) -> None:
        """Function sends many requests to server and checks response"""
        response = requests.post(url=self.url, headers=self.headers, proxies=self.proxy)
        print(f'{response.status_code} WITH {self.proxy}')
        if self.is_html:
            soup = BeautifulSoup(response.text, 'lxml')
            print(soup.title)  # if "Just a moment" we've got some problems...

            # Try to save an HTML file and look what will happen
            if i % 5 == 0 or i == 1:
                with open(f'{HTML_DIR}/test_{i}.html', 'w', encoding='utf-8') as html_file:
                    html_file.write(response.text)
        if self.is_API:
            if i % 5 == 0 or i == 1:
                with open(f'{JSON_DIR}/test_{i}.json', 'w', encoding='utf-8') as file:
                    json.dump(response.json(), file, indent=4, ensure_ascii=False)

