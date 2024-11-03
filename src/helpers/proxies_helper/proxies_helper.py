import json
import os
from typing import List, Literal

from config import settings
from custom_exceptions.exceptions import UndefinedProxiesError

class ProxiesHelper:
    def load_proxies(self, type: Literal["httpx", "webdriver"], country: Literal["eu", "ru"]) -> List:
        file_path = os.path.join(settings.PROXIES_DIR, country.upper(), f"{country}_proxies_{type}.json")
        try:
            with open(file_path, "r", encoding="utf-8") as json_file:
                proxies = json.load(json_file)
            if not proxies:
                 raise UndefinedProxiesError("Proxies list is empty.")
            return proxies
        except FileNotFoundError:
             raise UndefinedProxiesError(f"Proxies file not found: {file_path}")

    from selenium import webdriver
import zipfile
import os

def create_proxy_extension(proxy_host, proxy_port, username=None, password=None):
    manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            }
        }
        """

    background_js = f"""
        var config = {{
                mode: "fixed_servers",
                rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{proxy_host}",
                    port: {proxy_port}
                }},
                bypassList: ["localhost"]
                }}
            }};
        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

        chrome.webRequest.onAuthRequired.addListener(
            function(details) {{
                return {{
                    authCredentials: {{
                        username: "{username or ''}",
                        password: "{password or ''}"
                    }}
                }};
            }},
            {{urls: ["<all_urls>"]}},
            ['blocking']
        );
        """

    extension_path = os.path.join(settings.PROXIES_DIR, "proxy_extension.zip")
    
    with zipfile.ZipFile(extension_path, "w") as zipf:
        zipf.writestr("manifest.json", manifest_json)
        zipf.writestr("background.js", background_js)

    create_proxy_extension("proxy_host", 8080, "username", "password")
    
    settings.options.add_extension("proxy_extension.zip")
