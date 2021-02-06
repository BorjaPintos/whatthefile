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

    def _clean(self, result):
        key_to_del = []
        for key in result:
            if (('File' in key) or ('ExifTool' in key)):
                key_to_del.append(key)
        for key in key_to_del:
            del result[key]

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            return True
        return False

    def run(self, target_file: TargetFile):
        result = {}
        with exiftool.ExifTool() as et:
            result = et.get_metadata(target_file.get_path())
            self._clean(result)
        return result
