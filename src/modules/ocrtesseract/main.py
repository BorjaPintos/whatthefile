# -*- coding: utf-8 -*-
import pytesseract
import cv2

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "ocrtesseract"
        self._help = """Module to extract text fom image using ocr tesseract"""
        self._author = "BorjaPintos"

    # acondiciono el tamaño de la imagen para ict3  la cargo desde la ruta del agumento de linea de comandos y la meto en un array en la variable x
    def _extract_image_text(self, imagepath):
        image = cv2.imread(imagepath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # check to see if we should apply thresholding to preprocess the
        # image
        imageText = {}
        grayThresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # make a check to see if median blurring should be done to remove
        # noise
        grayBlur = cv2.medianBlur(gray, 3)

        imageText['Thresh'] = pytesseract.image_to_string(grayThresh)
        imageText['Blur'] = pytesseract.image_to_string(grayBlur)
        return imageText

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "JPEG image data" in target_file.get_type():
                return True
            elif "PNG image data" in target_file.get_type():
                return True
            elif "bitmap" in target_file.get_type():
                return True
            elif "GIF image data" in target_file.get_type():
                return True
        return False

    def run(self, target_file: TargetFile):
        result = self._extract_image_text(target_file.get_path())
        return result
