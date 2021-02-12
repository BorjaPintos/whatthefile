# -*- coding: utf-8 -*-
import exiftool
import os

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "exiftool"
        self._help = """Module to extract metadata"""
        self._author = "BorjaPintos"

    def _clean(self, result:dict) -> []:
        clean_result = {}
        clean_result["key_values"] = []
        clean_result["keys"] = []
        clean_result["values"] = []
        for key in result:
            if (('File' not in key) and ('ExifTool' not in key)):
                value = str(result[key])
                clean_result["keys"].append(str(key))
                clean_result["values"].append(value)
                clean_result["key_values"].append(str(key)+":"+value)
        return clean_result

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            return True
        return False

    def run(self, target_file: TargetFile):
        cleanresult = {}
        with exiftool.ExifTool() as et:
            result = et.get_metadata(target_file.get_path())
            cleanresult = self._clean(result)
        return cleanresult
