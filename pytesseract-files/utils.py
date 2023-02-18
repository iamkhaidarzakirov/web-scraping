import pytesseract
from PIL import Image
import requests


def recognize(image_path):
    # Tesseract engine
    pytesseract.pytesseract.tesseract_cmd = r'c:\tesseract\tesseract.exe'
    # Add image
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image=image, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    print(text)

