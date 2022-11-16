import datetime
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import fake_useragent

# test your code here!


def test():
    curr_date = datetime.datetime.now()
    for i in range(10):
        print(curr_date, '# ' * 10, sep='\n')
        time.sleep(10)
        curr_date = datetime.datetime.now()


def main():
    test()


if __name__ == '__main__':
    main()


