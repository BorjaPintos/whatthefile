# -*- coding: utf-8 -*-
import binwalk

def binwalk(binary):
    module = binwalk.scan(binary, signature=True, string=True)
    print(module)
    """Solo hay un fichero"""
    return module.results[0]

def generateReportBinwalk(analysingFile):
	return binwalk(analysingFile.getBinary())

def validFor(analysingFile):
	return True

def getParams():
  return []

def generateReport(analysingFile, params):
	report = generateReportBinwalk(analysingFile)
	return report