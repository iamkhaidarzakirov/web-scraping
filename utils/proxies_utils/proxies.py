import json
import os
from config.settings import PROXIES_DIR


with open(f"{PROXIES_DIR}/ru_proxies_aiohttp.json", 'r', encoding='utf-8') as json_file:
    AIOHTTP_PROXIES = json.load(json_file)

with open(f"{PROXIES_DIR}/ru_proxies_requests.json", 'r', encoding='utf-8') as json_file:
    REQUESTS_PROXIES = json.load(json_file)

with open(f"{PROXIES_DIR}/ru_proxies_webdriver.json", 'r', encoding='utf-8') as json_file:
    WEBDRIVER_PROXIES = json.load(json_file)
