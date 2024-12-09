from decouple import Config, RepositoryEnv
import logging.config
from pathlib import Path
from selenium import webdriver
import os
from webdriver_manager.chrome import ChromeDriverManager

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

CPU_COUNT = int(config("CPU_COUNT", 1))

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
CHROME_DRIVER_PATH = ChromeDriverManager().install()

# SELENIUM OPTIONS 
options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

if HEADLESS:
    options.add_argument('--headless')

options.add_argument('--ignore-ssl-errors')
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-extensions")
options.add_argument('--disable-blink-features=AutomationControlled')

# CAPTCHA SOLVERS API
TWOCAPTCHA_API_KEY = config("TWOCAPTCHA_API_KEY")
CAPSOLVER_API_KEY=config("CAPSOLVER_API_KEY")
