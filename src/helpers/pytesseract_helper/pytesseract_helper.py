import pytesseract
from PIL import Image
from config.settings import config

class PytesseractHelper:
    ENGINE_PATH = config("PYTESSERACT_PATH")

    def recognize(self, image_path: str, config: str = "--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789") -> str:
        """Function recognizes (if it is possible) text in image"""

        pytesseract.pytesseract.tesseract_cmd = self.ENGINE_PATH
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image=image, config=config)

            return text
        except Exception as e:
            raise Exception(f"An error occurred during OCR processing: {str(e)}")
