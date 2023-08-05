from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent  # root
DATA_DIR = os.path.join(BASE_DIR, 'data')  # all data dir here

PROXIES_DIR = os.path.join(BASE_DIR, 'data/proxies')  # proxies files directory path
HTML_DIR = os.path.join(BASE_DIR, 'data/html')
JSON_DIR = os.path.join(BASE_DIR, 'data/json')
IMAGES_DIR = os.path.join(BASE_DIR, 'data/images')
SHEETS_DIR = os.path.join(BASE_DIR, 'data/spreadsheets')
