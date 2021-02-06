# -*- coding: utf-8 -*-
import os
import magic
import hashlib

from src.domain.targetpath import TargetPath


class TargetDirectory(TargetPath):

    def __init__(self, path: str):
        super().__init__(path)
        self._validate_path()
        self._type = "Directory"


    def _validate_path(self):
        if not self.is_directory():
            raise BaseException("This is not a directory")

    def _get_other_info(self):
        result = {}
        result["elements"] = os.listdir(self._path)
        result["n_elements"] = len(os.listdir(self._path))
        return result
