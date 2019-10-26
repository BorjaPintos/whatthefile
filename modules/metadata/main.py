# -*- coding: utf-8 -*-
import exiftool
import os
from modules.imodule import IModule


class Constructor(IModule):

    def __init__(self):
        self._name = "exiftool"
        self._help = """Module to extract metadata"""
        self._author = "BorjaPintos"
        self._params = []

    def _cleanReport(self, report):
        keyToDel = []
        for key in report:
            if (('File' in key) or ('ExifTool' in key)):
                keyToDel.append(key)
        for key in keyToDel:
            del report[key]

    def validFor(self, targetFile):
        return True

    def generateReport(self, targetFile, params):
        report = {}
        with exiftool.ExifTool() as et:
            report = et.get_metadata(os.path.join(targetFile.getDirectory(),targetFile.getName()))
            self._cleanReport(report)
        return report
