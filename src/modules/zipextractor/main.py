# -*- coding: utf-8 -*-
import os
from zipfile import ZipFile
from pyzipper import AESZipFile

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule

PARAM_PWD = 'pwd'


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "zipextractor"
        self._help = """Extract files from zip:
		Params: {'""" + PARAM_PWD + """': <password>] password to extract files"""
        self._author = "BorjaPintos"

    def _run(self, target_file : TargetPath, pwd):
        result = {}
        binary = None
        with ZipFile(target_file.get_path(), 'r') as zip:
            for info in zip.infolist():
                try:
                    with zip.open(info.filename, 'r', pwd=pwd) as file:
                        binary = file.read()
                except:
                    try:
                        with AESZipFile(target_file.get_path(), 'r') as zf:
                            zf.pwd = pwd
                            binary = zf.read(info.filename)
                    except:
                        result['error'] = "Bad password or wrong decrypted algorithm"
                        continue

                safe_name = info.filename.replace("..", ".")
                path_to_save = os.path.join(target_file.get_directory(), safe_name)

                with open(path_to_save, "wb+") as file:
                    file.write(binary)
                result[safe_name] = os.path.join(target_file.get_directory(), safe_name)

        return result

    def _get_pwd_param(self, params):
        if PARAM_PWD in params:
            return params[PARAM_PWD]

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if ("Zip archive data" in target_file.get_type()):
                return True
        return False

    def run(self, target_file: TargetFile):
        pwd = self._get_pwd_param(self.get_params())
        report = self._run(target_file, pwd.encode())
        return report
