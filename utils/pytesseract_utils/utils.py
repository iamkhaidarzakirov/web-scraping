import pytesseract
from PIL import Image


def recognize(image_path: str, is_win: bool = False) -> str:
    """Function recognizes (if it is possible) text in image"""

    # Tesseract engine path
    if is_win:  # linux chosen as default system. if you need allow windows tesseract engine, specify is_win parameter
        pytesseract.pytesseract.tesseract_cmd = ''
    else:
        pytesseract.pytesseract.tesseract_cmd = ''
    # Add image
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image=image, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')

    return text

