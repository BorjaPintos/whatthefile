# -*- coding: utf-8 -*-
def generateReportBasic(analysingFile):
	basicDict = {}
	basicDict['filetype'] = analysingFile.getFiletype()
	return basicDict

def getParams():
  return []

def validFor(analysingFile):
	return True

def generateReport(analysingFile, params):
	report = generateReportBasic(analysingFile)
	return report
