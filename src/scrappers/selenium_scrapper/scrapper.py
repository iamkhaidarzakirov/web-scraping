import json
import os
import random
import time
from typing import List, Dict

from fake_useragent import UserAgent
import ipdb
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from custom_exceptions import exceptions
from config import settings
from helpers.selenium_helper.selenium_helper import SeleniumHelper
from scrappers.base_scrapper.scrapper import BaseScrapper


class SeleniumScrapper(BaseScrapper, SeleniumHelper):
    """Create browser scrapper here"""
    def __init__(self, **kwargs) -> None:
        super().__init__()  # Do not forget, super() calls just the first BaseScraper constructor
        SeleniumHelper.__init__(self, **kwargs) # If we need use the both constructors, we need call it explicitly
    
    def test_recaptcha_solver(self, url: str):
        self.logger.info("Test recaptcha solver...")

        self.session.get(url)
        time.sleep(random.randrange(2, 5))

        try:
            WebDriverWait(self.session, 15).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'google.com/recaptcha')]"))
            )
        except TimeoutError:
            self.logger.error("Captcha had not found")
        else:
            self.logger.info("Captcha has found")

            sitekey = self.session.find_element(By.ID, "g-recaptcha").get_attribute("data-sitekey")
            self.logger.info(f"Sitekey found: {sitekey}")
            time.sleep(2)
            
            token = self.captcha_helper.solve_recaptcha_2capthca(sitekey=sitekey, url=url)
            submit = self.session.find_element(By.XPATH, "//button[contains(@data-action,'demo_action')]")

            self.send_recaptcha_token(token=token, submit=submit)
            time.sleep(random.randrange(1, 3))
        
        self.logger.info("After captcha block ")
