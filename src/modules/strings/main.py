# -*- coding: utf-8 -*-
import string

from src.domain.targetfile import TargetFile
from src.modules.imodule import IModule

MIN = "charMin"


class Constructor(IModule):

    def __init__(self):
        self._name = "strings"
        self._help = """Module to extract strings from file.
			param: {'""" + MIN + """':4} is the minimum length that the strings must have"""
        self._author = "BorjaPintos"
        self._params = {MIN: 4}

    def _strings(self, binary: bytes, min_chars: int):
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

    def is_valid_for(self, target_file: TargetFile):
        if "ASCII text" in target_file.get_filetype():
            return False
        return True

    def _get_min_param(self, params: dict):
        if MIN in params:
            return params[MIN]

    def run(self, target_file: TargetFile, params: dict = None):
        if params is None:
            params = self._params
        try:
            min_chars = int(self._get_min_param(params))
            if min_chars:
                result = self._strings(target_file.get_binary(), min_chars)
        except:
            result = {"error": "invalid argument for module"}
        return result