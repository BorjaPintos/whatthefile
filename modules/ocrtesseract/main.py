# -*- coding: utf-8 -*-
from PIL import Image
import pytesseract
import argparse
import cv2
import os

from modules.imodule import IModule

class Constructor(IModule):

    def __init__(self):
        self._name = "ocrtesseract"
        self._help = """Module to extract text fom image using ocr tesseract"""
        self._author = "BorjaPintos"
        self._params = []

    #acondiciono el tamaño de la imagen para ict3  la cargo desde la ruta del agumento de linea de comandos y la meto en un array en la variable x
    def _extractImageText(self, imagepath):
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

    def _getImageText(self, targetFile):
        return self._extractImageText(targetFile.getCompletePath())

    def validFor(self, targetFile):
        if ("JPEG image data" in targetFile.getFiletype()):
            return True
        elif ("PNG image data" in targetFile.getFiletype()):
            return True
        elif ("bitmap" in targetFile.getFiletype()):
            return True
        elif ("GIF image data" in targetFile.getFiletype()):
            return True

        return False

    def generateReport(self, targetFile, params):
        report = {}
        report['extractedText'] = self._getImageText(targetFile)
        return report
