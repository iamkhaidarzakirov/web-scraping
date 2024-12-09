import logging
import random
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

from config import settings


class SeleniumHelper:
    def __init__(self, **kwargs) -> None:
        self._options = webdriver.ChromeOptions()
        self._session_params = kwargs if kwargs else {}
        self._session = None
        self._actions = None
    
    @property
    def session(self):
        return self._session

    def __enter__(self):
        self.create_session(**self._session_params)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()
    
    def create_session(self, **kwargs):
        if self._session is None:
            if kwargs.get("proxy") is not None:
                proxy = kwargs["proxy"]
                self.logger.info(f"BROWSER USE PROXY: [{proxy}] IN THIS SESSION")
                self._options.add_argument(f"--proxy-server={proxy}")

            for option in settings.options.arguments:
                self.logger.debug(f"Add an extra option to the session: [{option}]")
                self._options.add_argument(option) 

            self._session = webdriver.Chrome(service=Service(executable_path=settings.CHROME_DRIVER_PATH), options=self._options)
            self._actions = ActionChains(self._session)
            self.logger.info(f"Session created: {self._session}")
    
    def close_session(self):
        if self._session is not None:
            self._session.quit()
            self.logger.info(f"Session closed: {self._session} ")
            self._session = None

    def send_recaptcha_token(self, token: str, submit: WebElement):
        self.logger.info("Insert token into web element...")
        
        try:
            WebDriverWait(self.session, 10).until(
                EC.presence_of_element_located((By.ID, "g-recaptcha-response"))
            )
        except TimeoutError:
            self.logger.info("Failed locate recaptcha response element")
            return None
    
        self._session.execute_script("""
            document.getElementById('g-recaptcha-response').style.display = 'block';
            document.getElementById('g-recaptcha-response').value = arguments[0];
            document.getElementById('g-recaptcha-response').style.display = 'none';
            """,
            token
        )
        time.sleep(1)
        
        self.logger.info("Submit form")
        self._session.execute_script("arguments[0].click();", submit)

        time.sleep(random.randrange(2, 5))
