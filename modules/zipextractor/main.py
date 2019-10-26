# -*- coding: utf-8 -*-
import os
from zipfile import ZipFile
from pyzipper import AESZipFile
from core import Core
PARAM_PWD = 'pwd'

from modules.imodule import IModule


class Constructor(IModule):

    

    def __init__(self):
        self._name = "zipextractor"
        self._help = """Extract files from zip:
		Params: [""" + PARAM_PWD + """] password to extract files"""
        self._author = "BorjaPintos"
        self._params = [PARAM_PWD+"="]

    def _generateReportZip(self, targetFile, pwd):
        reportZip = {}
        binary = None
        with ZipFile(targetFile.getCompletePath(), 'r') as zip:
            for info in zip.infolist():
                try:
                    with zip.open(info.filename, 'r', pwd=pwd) as file:
                        binary = file.read()
                except:
                    try:
                        with AESZipFile(targetFile.getCompletePath(), 'r') as zf:
                            zf.pwd = pwd
                            binary = zf.read(info.filename)
                    except:
                        reportZip['error'] = "Bad password or wrong decrypted algorithm"
                        continue

                pathToSave = os.path.join(targetFile.getGeneratedFilesDirectory(), info.filename)

                with open(pathToSave, "wb") as file:
                    file.write(binary)
                reportZip[info.filename] = os.path.join(targetFile.getName(), info.filename)
                
        return reportZip


    def _getPwdParam(self, params):
        for param in params:
            if PARAM_PWD in param:
                return param.split("=")[1]


    def validFor(self, targetFile):
        if ("Zip archive data" in targetFile.getFiletype()):
            return True
        return False


    def generateReport(self, targetFile, params):
        pwd = self._getPwdParam(params)
        report = self._generateReportZip(targetFile, pwd.encode())
        return report
