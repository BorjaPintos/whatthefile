# -*- coding: utf-8 -*-
import os
import magic
import hashlib

from src.domain.targetpath import TargetPath
from src.utils import auxiliar


class TargetFile(TargetPath):

    def __init__(self, path: str):
        super().__init__(path)
        self._validate_path()
        self._extension = os.path.splitext(self._path)[1].lower()
        "lazy"
        self._binary = None
        try:
            self._type = self._get_filetype_from_path(self._path)
        except:
            "hay un bug en la libreria magic y este es el workarround"
            self._type = self._get_filetype_from_binary(TargetFile.get_utf_8_binary(self.get_binary()))


    def _validate_path(self):
        if not self.is_file():
            raise BaseException("This is not a file")

    def get_binary(self) -> bytes:
        if self._binary is None:
            self._binary = TargetFile._read_file(self._path)
        return self._binary

    def get_extension(self) -> str:
        return self._extension

    @staticmethod
    def _get_filetype_from_path(path: str) -> str:
        return magic.from_file(path)

    @staticmethod
    def _get_filetype_from_binary(binary: bytes) -> str:
        return magic.from_buffer(binary)

    @staticmethod
    def get_utf_8_binary(binary: bytes) -> bytes:
        try:
            binary.decode("utf-8")
        except:
            try:
                return auxiliar.get_str_utf_8_from_bytes().encode("utf-8")
            except:
                pass
                "try next type"

        return binary

    @staticmethod
    def _read_file(path: str) -> bytes:
        all_binary = b""
        with open(path, "rb") as file:
            while True:
                chunk = file.read()
                if not chunk:
                    break
                all_binary = all_binary + chunk

        return all_binary


    def _get_other_info(self) -> dict:
        result = {"extension": self._extension}
        return result
