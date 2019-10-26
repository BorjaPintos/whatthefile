# -*- coding: utf-8 -*-
import math
from modules.imodule import IModule
from PIL import Image
from pyzbar.pyzbar import decode


class Constructor(IModule):

    def __init__(self):
        self._name = "qrbcreader"
        self._help = """Module to read QR and Barcodes in jpg and png images"""
        self._author = "BorjaPintos"
        self._params = []

    def _readBCQR(self, targetFile):
        decodedList = decode(Image.open(targetFile.getCompletePath()))
        i = 0
        reportList = {}
        for dec in decodedList:
            reportList[str(i)] = dec.data.decode("utf-8")
            i+=1
        return reportList

    def validFor(self, targetFile):
        if ("JPEG image data" in targetFile.getFiletype()):
            return True
        elif ("PNG image data" in targetFile.getFiletype()):
            return True
        return False

    def generateReport(self, targetFile, params):
        return self._readBCQR(targetFile)
