# -*- coding: utf-8 -*-
import os
import magic
import hashlib


class TargetFile:

    def __init__(self, path: str):
        TargetFile._validate_file(path)
        self._path = path
        self._directory = os.path.dirname(self._path)
        self._name = os.path.basename(self._path)
        self._extension = os.path.splitext(self._path)[1]
        self._filetype = self._get_filetype_from_path(self._path)
        "lazy"
        self._binary = None

    def get_binary(self):
        if self._binary is None:
            self._binary = TargetFile._read_file(self._path)
        return self._binary

    def get_path(self):
        return self._path

    def get_directory(self):
        return self._directory

    def get_name(self):
        return self._name

    def get_extension(self):
        return self._extension

    def get_filetype(self):
        return self._filetype

    """
    def _createFile(self):
        if not os.path.exists(self._directory):
            os.makedirs(self._directory)
            with open(os.path.join(self._directory, self._name), "wb+") as f:
                f.write(self._binary)
    """

    @staticmethod
    def _validate_file(path):
        if not os.path.isfile(path):
            raise BaseException("This is not a file")

    @staticmethod
    def _get_filetype_from_path(path: str):
        return magic.from_file(path)

    @staticmethod
    def _get_filetype_from_binary(binary: bytes):
        return magic.from_buffer(binary)

    @staticmethod
    def _read_file(path: str):
        all_binary = b""
        with open(path, "rb") as file:
            while True:
                chunk = file.read()
                if not chunk:
                    break
                all_binary = all_binary + chunk
        return all_binary
