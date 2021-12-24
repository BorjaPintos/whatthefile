# -*- coding: utf-8 -*-
import string

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule

MIN = "char_min"


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "strings"
        self._help = """Module to extract strings from file.
			param: {'""" + MIN + """':4} is the minimum length that the strings must have"""
        self._author = "BorjaPintos"
        self._default_params = {MIN: 4}

    def _strings(self, binary: bytes, min_chars: int) -> list:
        bytes_printables = []
        for char in string.printable:
            bytes_printables.append(char.encode("utf-8"))
        words = []
        result = ""
        # c es un entero pero necesita pasarse a 1 byte
        for c in binary:
            byte = c.to_bytes(1, byteorder='big')
            if byte in bytes_printables:
                result += byte.decode("utf-8")
                continue
            if len(result) >= min_chars:
                words.append(result)
            result = ""
        return words

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "ignore_extensions" in self.get_params():
                if isinstance(target_file, TargetFile):
                    if target_file.get_extension() in self.get_params()["ignore_extensions"].split(","):
                        return False
            return True
        return False


    def _get_min_param(self, params: dict):
        if params is None:
            params = self._default_params
        if MIN in params:
            return params[MIN]
        else:
            return self._default_params[MIN]

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        result = {}
        try:
            min_chars = int(self._get_min_param(self.get_params()))
            if min_chars:
                result = {"elements": self._strings(target_file.get_binary(), min_chars), ">=": min_chars}
                result["n_elements"] = len(result["elements"])
        except:
            result = {"error": "invalid argument for module"}
        return result
