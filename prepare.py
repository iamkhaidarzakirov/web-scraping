from web_scraping_utils import create_proxies_json


# Preparatory operations before starting a scraping work
if __name__ == '__main__':
    # Specify proxies format and paths to create JSON file
    create_proxies_json(
        proxies_format='',  # aiohttp or requests
        source_path='../ru-proxies-list.txt',  # it is my proxies txt file main path
        result_path='DATA/ru-proxies-aiohttp.json'  # do not forget to change path when create another format
    )
