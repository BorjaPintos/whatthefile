# -*- coding: utf-8 -*-
from zipfile import ZipFile
from pyzipper import AESZipFile
import core
PARAM_PWD = 'pwd'


def generateReportZip(analysingFile, pwd):
    reportZip = {}
    binary = None
    with ZipFile(analysingFile.getCompletePath(), 'r') as zip:
        for info in zip.infolist():
            try:
                with zip.open(info.filename, 'r', pwd=pwd) as file:
                    binary = file.read()
            except:
                try:
                    with AESZipFile('comprimidoConPass.zip', 'r') as zf:
                        zf.pwd = pwd
                        binary = zf.read(info.filename)
                except:
                    reportZip['error'] = "Bad password or wrong decrypted algorithm"
            ident = core.run(binary, core.modules)
            reportZip[info.filename] = ident
    return reportZip


def getHelp():
    return """Extract files from zip and analyzed them with all modules:
		Params: [""" + PARAM_PWD + """] password to extract files"""


def getParams():
    return [PARAM_PWD+"="]


def getPwdParam(params):
    for param in params:
        if PARAM_PWD in param:
            return param.split("=")[1]


def validFor(analysingFile):
    if ("Zip archive data" in analysingFile.getFiletype()):
        return True
    return False


def generateReport(analysingFile, params):
    pwd = getPwdParam(params)
    report = generateReportZip(analysingFile, pwd.encode())
    return report
