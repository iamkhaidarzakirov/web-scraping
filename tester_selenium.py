import undetected_chromedriver as uc
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def uc_tester(driver: uc.Chrome) -> None:
    """Function tests the website using webdriver"""

    for i in range(1, 2):
        url = ""
        browser.get(url)
        time.sleep(5)
        response = driver.page_source
        ishtml = False  # Server side rendering — request returns html
        isjson = True  # Client side rendering — request returns json / Request to API
        if ishtml:
            # Try to write response as an HTML file and look what will happen
            with open(f'test/test.html', 'w', encoding='utf-8') as file:
                file.write(response)
        if isjson:
            # Try to get JSON config from html page source
            content = driver.find_element(by='tag name', value='pre').text
            parsed_json = json.loads(content)
            with open(f'test/test.json', 'w', encoding='utf-8') as file:
                json.dump(parsed_json, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    options = uc.options.ChromeOptions()

    with uc.Chrome(options=options) as browser:
        uc_tester(browser)
