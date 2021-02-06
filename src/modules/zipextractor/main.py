# -*- coding: utf-8 -*-
import os
from zipfile import ZipFile
from pyzipper import AESZipFile

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule

PARAM_PWD_DICT = 'pwd_dict'
EXTRACTED_OUTPUT_PATH = 'extracted_output_path'


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "zipextractor"
        self._help = """Extract files from zip"""
        self._author = "BorjaPintos"

    def _run(self, target_file : TargetFile, extracted_output_path:str, pwd_list: list):
        result = {}
        binary = None
        decripted_password = None
        with ZipFile(target_file.get_path(), 'r') as zip:
            for info in zip.infolist():
                try:
                    with zip.open(info.filename, 'r') as file:
                        binary = file.read()
                except:
                    pass
                if not binary:
                    "probamos con contraseña"
                    for pwd in pwd_list:
                        try:
                            binary = self.decrypt_with_password(info.filename, pwd)
                            if binary:
                                decripted_password = pwd
                                break;
                        except:
                            pass
                if not binary:
                    "probamos con contraseña y algoritmo de cifrado AES"
                    for pwd in pwd_list:
                        try:
                            binary = self.decrypt_AES_WithPassword(target_file, info.filename, pwd)
                            if binary:
                                decripted_password = pwd
                                break;
                        except:
                            pass
                if binary:
                    safe_name = info.filename.replace("..", ".")
                    path_to_save = os.path.join(extracted_output_path, safe_name)
                    result[info.filename] = path_to_save
                    if decripted_password:
                        result["password"] = decripted_password.decode()
                    with open(path_to_save, "wb+") as file:
                        file.write(binary)
                else:
                    result["error"] = "Bad password or wrong decrypted algorithm"

        return result


    def decrypt_with_password(self, file_name, pwd):
        with zip.open(file_name, 'r', pwd=pwd) as file:
            binary = file.read()
        return binary

    def decrypt_AES_WithPassword(self, target_file: TargetFile, file_name, pwd):
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

    def _get_extracted_output_path(self, params):
        if not EXTRACTED_OUTPUT_PATH in params:
            return None
        return params[EXTRACTED_OUTPUT_PATH]

    def run(self, target_file: TargetFile):
        extracted_output_path = self._get_extracted_output_path(self.get_params())
        if not extracted_output_path:
            return {"error" : "property: " + EXTRACTED_OUTPUT_PATH + " is required for unzip"}
        pwd_list = self._get_password_list(self.get_params())
        report = self._run(target_file, extracted_output_path, pwd_list)
        return report
