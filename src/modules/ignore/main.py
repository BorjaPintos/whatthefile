# -*- coding: utf-8 -*-
import os
from src.domain.ignoreanalysisexception import IgnoreAnalysisException
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule

HASHES_MD5 = "file_hashes_md5_to_ignore"
HASHES_SHA1 = "file_hashes_sha1_to_ignore"
EXTENSIONS = "file_extensions_to_ignore"
PATH = "file_ignore_path"
IGNORE_MAX = "ignore_greater_or_equal_than"
IGNORE_MIN = "ignore_less_or_equal_than"


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "ignore"
        self._help = """Modulo para ignorar el análisis de paths según nos convenga"""
        self._author = "BorjaPintos"
        self._hashes_md5 = None
        self._hashes_sha1 = None
        self._extensions = None
        self._paths = None
        self._max_size = None
        self._min_size = None

    def is_valid_for(self, target_path: TargetPath):
        return True

    def _check_paths(self, target_path: TargetPath):
        if PATH in self._params:
            if self._paths is None:
                paths_list = self._read_file(self._params[PATH])
                self._paths = []
                for path in paths_list:
                    self._paths.append(os.path.abspath(path))

            path = os.path.abspath(target_path.get_path())
            while path not in ["", ".", ".."]:
                if path in self._paths:
                    self._ignore()
                path = os.path.dirname(path)

    def _check_extensions(self, target_file: TargetPath):
        if target_file.is_file():
            if EXTENSIONS in self._params:
                if self._extensions is None:
                    self._extensions = self._read_file(self._params[EXTENSIONS])
                if isinstance(target_file, TargetFile):
                    if target_file.get_extension() in self._extensions:
                        self._ignore()

    def _check_sizes(self, target_file: TargetPath):
        info = target_file.get_info()
        if target_file.is_file() and "st_size" in info:
            if IGNORE_MAX in self._params:
                if self._max_size is None:
                    self._max_size = int(self._params[IGNORE_MAX])
                if info["st_size"] >= self._max_size:
                    self._ignore()
            if IGNORE_MIN in self._params:
                if self._min_size is None:
                    self._min_size = int(self._params[IGNORE_MIN])
                if info["st_size"] <= self._min_size:
                    self._ignore()

    def _check_hashes(self, result_of_previos_modules: dict):
        if "hashes" in result_of_previos_modules:
            if "MD5" in result_of_previos_modules["hashes"]:
                if HASHES_MD5 in self._params:
                    if self._hashes_md5 is None:
                        self._hashes_md5 = self._read_file(self._params[HASHES_MD5])
                    if result_of_previos_modules["hashes"]["MD5"] in self._hashes_md5:
                        self._ignore()

            if "SHA1" in result_of_previos_modules["hashes"]:
                if HASHES_SHA1 in self._params:
                    if self._hashes_sha1 is None:
                        self._hashes_sha1 = self._read_file(self._params[HASHES_SHA1])
                    if result_of_previos_modules["hashes"]["SHA1"] in self._hashes_sha1:
                        self._ignore()

    def _ignore(self):
        raise IgnoreAnalysisException()

    def _read_file(self, path: str):
        lines = []
        with open(path, "r") as file:
            for line in file:
                lines.append(line)
        return lines

    def run(self, target_path: TargetPath, result_of_previos_modules: dict) -> dict:
        self._check_hashes(result_of_previos_modules)
        self._check_extensions(target_path)
        self._check_paths(target_path)
        self._check_sizes(target_path)
        return {"ignored": False}
