import logging
import os
import random
import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from twocaptcha import TwoCaptcha

from config import settings


class CaptchaHelper:
    def __init__(self):
        self.__rucaptcha_api_key = settings.TWOCAPTCHA_API_KEY
        self.__capsolver_api_key = settings.CAPSOLVER_API_KEY
        self.logger = logging.getLogger("streamLogger")
    
    # RECAPTCHA
    def solve_recaptcha_2capthca(self, sitekey: str, url: str):
        if self.__rucaptcha_api_key is None:
            self.logger.error("Failed solve recaptcha: [TWOCAPTCHA API KEY has not provided]")
            return None  # Возвращаем None или пустое значение
        
        solver = TwoCaptcha(self.__rucaptcha_api_key)
        
        try:
            self.logger.info("Start solving recatcha...")
            token = solver.solve_captcha(
                site_key=sitekey,
                page_url=url
            )
        except Exception as e:
            self.logger.info(f"Failed solve recaptcha with error: [{e}]")
            return None
        else:
            self.logger.info(f"Recaptcha has solved successfully. Token:\n {token}")
            return token


    def solve_recaptcha_capsolver(self):
        if self.__capsolver_api_key is None:
            return self.logger.error("Failed solve recaptcha: [CAPSOLVER API KEY has not provided]")
