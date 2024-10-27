import logging
import os
import pandas as pd
import re

from helpers.captcha_helper.captcha_helper import CaptchaHelper
from helpers.proxies_helper.proxies_helper import ProxiesHelper
from helpers.pytesseract_helper.pytesseract_helper import PytesseractHelper
from config import settings


class BaseScrapper:
    def __init__(self) -> None:
        self.proxies_helper = ProxiesHelper()
        self.captcha_helper = CaptchaHelper()
        self.pytesseract_helper = PytesseractHelper()
        self.logger =  logging.getLogger("streamLogger")
    
    def add_rows_to_xlsx(self, file_name: str, source: dict, sheet_title: str = 'Sheet1') -> None:
        """
        Add one / or many (depending on DataFrame) strings to .xlsx spreadsheet.
        It allows to create table with many sheets and add a row to specific sheet depending on which sheet name had specified.
        """
        df = pd.DataFrame(source)
        path = os.path.join(settings.SHEETS_DIR, file_name)
        
        if not os.path.exists(path):
            df.to_excel(path, sheet_name=sheet_title, index=False)
        else:
            with pd.ExcelFile(path, engine="openpyxl") as reader:
                sheet_titles = reader.sheet_names
                if sheet_title in sheet_titles:
                    info = reader.parse(sheet_name=sheet_title)
                    rows = len(info)
                    start = rows + 1
                    with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                        df.to_excel(writer, startrow=start, sheet_name=sheet_title, index=False, header=False)
                else:
                    with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                        df.to_excel(writer, startrow=0, sheet_name=sheet_title, index=False)

    def del_special_symbols(some_string: str) -> str:
        """Delete all special symbols in string using re module"""

        edited_string = re.sub(r"[^\w\s]+|\d+", r'', string=some_string).strip()
        return edited_string
