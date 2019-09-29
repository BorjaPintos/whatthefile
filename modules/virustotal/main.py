# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import virustotalapi

def generateReportVT(analysingFile):
	virusTotalCheck = virustotalapi.checkHash(analysingFile.getName())
	virusTotalReport = {}
	virusTotalReport['positives'] = 0
	if (virusTotalCheck['response_code'] == 1):
		virusTotalReport['positives'] = virusTotalCheck['positives']
		virusTotalReport['total'] = virusTotalCheck['total']
		avDetections = {}
		for av_name, av_data in virusTotalCheck['scans'].items():
			if (av_data['result'] is None):
				avDetections[av_name] =  "None"
			else:
				avDetections[av_name] = av_data['result']
		virusTotalReport['avDetections'] = 	avDetections
	return virusTotalReport

def getHelp():
	return """Module to analyze file using virus total, only the hash will be sumitted."""

def getParams():
  return []

def validFor(analysingFile):
	return True

def generateReport(analysingFile, params):
	report = generateReportVT(analysingFile)
	return report
