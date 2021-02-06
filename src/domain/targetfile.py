# -*- coding: utf-8 -*-
import os
import magic
import hashlib

from src.domain.targetpath import TargetPath


class TargetFile(TargetPath):

    def __init__(self, path: str):
        super().__init__(path)
        self._validate_path()
        self._type = self._get_filetype_from_path(self._path)
        self._extension = os.path.splitext(self._path)[1]
        "lazy"
        self._binary = None

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
        result = {}
        result["extension"] = self._extension
        return result
