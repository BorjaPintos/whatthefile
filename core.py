# -*- coding: utf-8 -*-
import imp
import os
import json
from domain.module import Module
from domain.loadermodules import LoaderModules
from domain.targetfile import TargetFile


REPORTNAME = "report.txt"
REPORTDIRECTORY = "./analyzed/"

class Core():

	def __init__(self):
		self.__modules = LoaderModules().get_modules()

	def _generateReport(self, targetFile : TargetFile, modulesToUse: list):
		report = {}
		for moduleToUse in modulesToUse:
			module = self.__modules[moduleToUse["id"]]
			if (module.isActive() and module.getMod().validFor(targetFile)):
				report[module.getName()] = module.getMod().generateReport(targetFile, moduleToUse["params"])
		return report

	def _getExistingReport(self, directory : str):
		report = {}
		with open(os.path.join(directory, REPORTNAME),"r") as file:
			report = file.read()
		return json.loads(report)

	def _saveReport(self, targetFile : TargetFile, report : dict):
		with open(os.path.join(targetFile.getDirectory(), REPORTNAME),"w") as file:
			file.write(json.dumps(report))

	def _createReport(self, targetFile: TargetFile, modulesToUse : list):
		report = self._generateReport(targetFile, modulesToUse)
		self._saveReport(targetFile, report)
		return report

	def run(self, binary: bytes, modulesToUse: list):
		targetFile = TargetFile(REPORTDIRECTORY, binary)
		self._createReport(targetFile, modulesToUse)
		return targetFile.getName()

	def viewReport(self, name: str):
		directory = os.path.join(REPORTDIRECTORY,name)
		if not os.path.exists(directory):
			return None
		else:
			return self._getExistingReport(directory)
	
	def getFilePath(self, hash, name):
		directory = os.path.join(REPORTDIRECTORY,hash)
		directoryfiles = os.path.join(directory,"files")
		filePath = os.path.join(directoryfiles, name)
		if not os.path.exists(filePath):
			return None
		else:
			return filePath

	def getModules(self):
		array = []
		for module in self.__modules:
			if module.isActive:
				mod = {}
				mod['name']=module.getName()
				mod['index']=module.getIndex()
				mod['params']=module.getParams()
				mod['help']=module.getHelp()
				array.append(mod)
		return array


