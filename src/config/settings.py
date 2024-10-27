from decouple import Config, RepositoryEnv
import logging.config
from pathlib import Path
from selenium import webdriver
import os


# Project paths
CONTAINER_DIR = Path(__file__).resolve().parent.parent.parent 
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROXIES_DIR = os.path.join(BASE_DIR, 'data/proxies')
HTML_DIR = os.path.join(BASE_DIR, 'data/templates')
JSON_DIR = os.path.join(BASE_DIR, 'data/json')
IMAGES_DIR = os.path.join(BASE_DIR, 'data/images')
SHEETS_DIR = os.path.join(BASE_DIR, 'data/spreadsheets')

# dotenv
config = Config(RepositoryEnv(f"{CONTAINER_DIR}/.env"))

# logging
log_config = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "[%(levelname)s]: %(asctime)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "streamLogger": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": "no"
        }
    }
}

logging.config.dictConfig(log_config)

# SELENIUM
HEADLESS = config("HEADLESS") == "True"

# SELENIUM OPTIONS 
OPTIONS = webdriver.ChromeOptions()
