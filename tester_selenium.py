import undetected_chromedriver as uc
import json
import random
import time
from selenium import webdriver


def uc_tester(driver: uc.Chrome) -> None:
    response = driver.page_source
    # Try to write response as an HTML file and look what will happen
    with open(f'test/test.html', 'w', encoding='utf-8') as file:
        file.write(response)

    # Try to get JSON data from html page source
    # content = driver.find_element(by='tag name', value='pre').text
    # parsed_json = json.loads(content)
    # with open(f'DATA/test.json', 'w', encoding='utf-8') as file:
    #     json.dump(parsed_json, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # Proxies selenium format
    url = ''
    options = uc.options.ChromeOptions()
    options.add_argument('--headless')
    with uc.Chrome(options=options) as browser:
        browser.get(url)
        uc_tester(browser)
