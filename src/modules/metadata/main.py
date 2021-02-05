# -*- coding: utf-8 -*-
import exiftool
import os

from src.domain.targetfile import TargetFile
from src.modules.imodule import IModule


class Constructor(IModule):

    def __init__(self):
        self._name = "exiftool"
        self._help = """Module to extract metadata"""
        self._author = "BorjaPintos"
        self._params = None

    def _clean(self, result):
        key_to_del = []
        for key in result:
            if (('File' in key) or ('ExifTool' in key)):
                key_to_del.append(key)
        for key in key_to_del:
            del result[key]

    def is_valid_for(self, target_file: TargetFile):
        return True

    def run(self, target_file: TargetFile, params: dict = None):
        result = {}
        with exiftool.ExifTool() as et:
            result = et.get_metadata(target_file.get_path())
            self._clean(result)
        return result
