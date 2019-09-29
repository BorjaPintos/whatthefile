# -*- coding: utf-8 -*-
import exiftool
import os

def cleanReport(report):
    keyToDel = []
    for key in report:
        if (('File' in key) or ('ExifTool' in key)):
            keyToDel.append(key)
    for key in keyToDel:
        del report[key]


def getHelp():
	return """Module to extract metadata using exiftool"""

def getParams():
  return []

def validFor(analysingFile):
	return True

def generateReport(analysingFile, params):
    report = {}
    with exiftool.ExifTool() as et:
        report = et.get_metadata(os.path.join(analysingFile.getDirectory(),analysingFile.getName()))
        cleanReport(report)
    return report
