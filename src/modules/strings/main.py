# -*- coding: utf-8 -*-
import subprocess
import traceback
from typing import List

from src.domain.enumso import SO
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
from src.utils import auxiliar

MIN = "char_min"


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "strings"
        self._help = """Module to extract strings from file.
			param: {'""" + MIN + """':4} is the minimum length that the strings must have"""
        self._author = "BorjaPintos"
        self._default_params = {MIN: 4}

    @staticmethod
    def get_windows_command(path: str, min_chars: str) -> List:
        return ["strings.exe", "--accepteula", "-nobanner", "-n", str(min_chars), path]

    @staticmethod
    def get_linux_command(path: str, min_chars: int) -> List:
        return ["strings", "-n", str(min_chars), path]

    @staticmethod
    def get_mac_command(path: str, min_chars: int) -> List:
        return ["strings", "-n", str(min_chars), path]

    @staticmethod
    def get_command(path: str, min_chars: int):
        switch = {
            SO.MACOS: Constructor.get_mac_command,
            SO.LINUX: Constructor.get_linux_command,
            SO.WINDOWS: Constructor.get_windows_command,
        }
        platform = auxiliar.get_SO()
        if platform:
            return switch.get(platform)(path, min_chars)
        return None

    def _strings(self, target_file: TargetFile, min_chars: int) -> List:
        call = subprocess.run(
            Constructor.get_command(target_file.get_path(), min_chars),
            capture_output=True)
        if len(call.stderr) > 0:
            raise Exception(auxiliar.get_str_utf_8_from_bytes(call.stderr))
        else:
            data = auxiliar.get_str_utf_8_from_bytes(call.stdout).split("\n")
            return list(filter(lambda a: a != "", data))

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
                result = {"elements": self._strings(target_file, min_chars), ">=": min_chars}
                result["n_elements"] = len(result["elements"])
        except BaseException as e:
            traceback.print_exc()
            result = {"error": str(e)}
        return result
