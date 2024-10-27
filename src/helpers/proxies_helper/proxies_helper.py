import json
import os
from typing import List, Literal

from config.settings import PROXIES_DIR
from custom_exceptions.exceptions import UndefinedProxiesError

class ProxiesHelper:
    def load_proxies(self, type: Literal["requests", "aiohttp", "webdriver"], country: Literal["eu", "ru"]) -> List:
        file_path = os.path.join(PROXIES_DIR, country.upper(), f"{country}_proxies_{type}.json")
        try:
            with open(file_path, "r", encoding="utf-8") as json_file:
                proxies = json.load(json_file)
            if not proxies:
                 raise UndefinedProxiesError("Proxies list is empty.")
            return proxies
        except FileNotFoundError:
             raise UndefinedProxiesError(f"Proxies file not found: {file_path}")
