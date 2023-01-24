from rest import requests_debugger
import requests
from bs4 import BeautifulSoup
import json
# test your code here!


def test():

    with open('myProxies.json', 'r', encoding='utf-8') as file:
        proxies = json.load(file)
        print(proxies)


if __name__ == '__main__':
    test()


