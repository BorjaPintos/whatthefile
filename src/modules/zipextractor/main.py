# -*- coding: utf-8 -*-
import os
from zipfile import ZipFile
from pyzipper import AESZipFile

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
from src.utils.safe import Safe

PARAM_PWD_DICT = 'pwd_dict'
EXTRACTED_OUTPUT_PATH = 'extracted_output_path'


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "zipextractor"
        self._help = """Extract files from zip"""
        self._author = "BorjaPintos"

    def _run(self, target_file : TargetFile, pwd_list: list):
        result = {}
        result["new_files"] = []
        result["new_path_files"] = []
        binary = None
        decripted_password = None
        with ZipFile(target_file.get_path(), 'r') as zip:
            for info in zip.infolist():
                if info.filename[-1] == '/':
                    #it is a dir, so ignore, then we create the dirs
                    continue

                try:
                    with zip.open(info.filename, 'r') as file:
                        binary = file.read()
                except:
                    pass
                if not binary:
                    "probamos con contraseña"
                    for pwd in pwd_list:
                        try:
                            binary = self._decrypt_with_password(info.filename, pwd)
                            if binary:
                                decripted_password = pwd
                                break;
                        except:
                            pass
                if not binary:
                    "probamos con contraseña y algoritmo de cifrado AES"
                    for pwd in pwd_list:
                        try:
                            binary = self._decrypt_AES_WithPassword(target_file, info.filename, pwd)
                            if binary:
                                decripted_password = pwd
                                break;
                        except:
                            pass
                if binary:
                    path_saved = Safe.create_file(os.path.join("./zipextractor", os.path.join(target_file.get_path(), info.filename)),  binary)
                    result["new_files"].append(info.filename)
                    result["new_path_files"].append(path_saved)
                    if decripted_password:
                        result["password"] = decripted_password.decode()
                else:
                    result["error"] = "Bad password or wrong decrypted algorithm"

        return result


    def _decrypt_with_password(self, file_name, pwd):
        with zip.open(file_name, 'r', pwd=pwd) as file:
            binary = file.read()
        return binary

    def _decrypt_AES_WithPassword(self, target_file: TargetFile, file_name, pwd):
        try:
            with AESZipFile(target_file.get_path(), 'r') as zf:
                zf.pwd = pwd
                binary = zf.read(file_name)
                return binary
        except:
            return None

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if ("Zip archive data" in target_file.get_type()):
                return True
        return False

    def _get_password_list(self, params):
        list = []
        if PARAM_PWD_DICT in params:
            password_list_path = params[PARAM_PWD_DICT]
            with open(password_list_path, "r") as password_list_file:
                line = password_list_file.readline().strip()
                while line:
                    list.append(line.encode())
                    line = password_list_file.readline().strip()

        return list


    def run(self, target_file: TargetFile):
        pwd_list = self._get_password_list(self.get_params())
        report = self._run(target_file, pwd_list)
        return report