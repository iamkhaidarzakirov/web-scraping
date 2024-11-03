import logging
import os
import re
from typing import Any, List

from config import settings

logger = logging.getLogger("streamLogger")


def chunk_list(data: List, chunk_size: int) -> Any:
    """Generate specified size chunks from data list"""
    logger.debug(f"Data length: [{len(data)}] Chunking by: [{chunk_size}] items")

    for i in range(0, len(data), chunk_size):
        limit = i + chunk_size
        yield data[i:limit]


def del_special_symbols(some_string: str) -> str:
    """Delete all special symbols in string using re module"""
    edited_string = re.sub(r"[^\w\s]+|\d+", r'', string=some_string).strip()
    return edited_string


def save_html(context: str, name: str = "temp",  ):
    if not context:
        raise ValueError("Source code is empty")

    with open(os.path.join(settings.HTML_DIR, f"{name}.html"), "w") as html_file:
        html_file.write(context)
        logger.info(f"SUCCESS: [{name}.html]")