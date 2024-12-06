import os
import json
import random
from typing import Literal, List

from client.agents import user_agents
from client.headers import base_headers
from config import settings


def init_headers(platform: Literal["windows", "linux", "android", "apple"] = "windows"):
    """Inintialize headers for current session"""
    headers = base_headers
    headers["User-Agent"] = random.choice(user_agents[platform])
    
    return headers


def save_html_content(content: str, name: str = "temp.html") -> None:
    path = os.path.join(settings.HTML_DIR, name)
    
    with open(path, "w", encoding="utf-8") as html_file:
        html_file.write(content)


def save_list_to_json(content: List, path: str):
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(content, json_file, indent=4, ensure_ascii=False)
