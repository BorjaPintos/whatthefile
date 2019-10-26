# -*- coding: utf-8 -*-
import sys
import os
from modules.imodule import IModule
sys.path.insert(0, os.path.dirname(__file__))
import virustotalapi

class Constructor(IModule):

	def __init__(self):
		self._name = "virustotal"
		self._help = """Module to analyze file using virus total, only the hash will be sumitted."""
		self._author = "BorjaPintos"
		self._params = []

	def validFor(self, analysingFile):
		return True

	def generateReport(self, targetFile, params):
		virusTotalCheck = virustotalapi.checkHash(targetFile.getName())
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
