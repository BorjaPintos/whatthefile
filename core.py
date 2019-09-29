# -*- coding: utf-8 -*-
import imp
import os
import json
import hashlib
import magic

MODULESPATH = "./modules/"
FILENAME = "report.txt"
ENDLINE = "\r\n"
ANALIZEDDIRECTORY = "./analized/"
SLASH = "/"
modules = []

class Module():
	def __init__(self, name, index, mod, active, params, help):
		self._name = name
		self._index = index
		self._mod = mod
		self._active = active
		self._params = params
		self._help = help

	def getName(self):
		return self._name
	def getIndex(self):
		return self._index
	def getMod(self):
		return self._mod
	def isActive(self):
		return self._active
	def getParams(self):
		return self._params
	def getHelp(self):
		return self._help


class AnalysingFile():

	def __init__(self, binary, directory, name, filetype):
		self.binary = binary
		self.directory = directory
		self.name = name
		self.filetype = filetype

	def getBinary(self):
		return self.binary
	def getDirectory(self):
		return self.directory
	def getName(self):
		return self.name
	def getFiletype(self):
		return self.filetype
	def getCompletePath(self):
		return os.path.join(self.getDirectory(),self.getName())

def addModule(mod):
	global modules
	modules.append(mod)

def loadModules(path):
	index = 0
	ls = os.listdir(MODULESPATH)
	for entry in ls:
		completePath = os.path.join(MODULESPATH, entry)
		if not os.path.isfile(completePath):
			py_mod = imp.load_source(entry, os.path.join(completePath,"main.py"))
			addModule(Module(entry, index, py_mod, True, py_mod.getParams(), py_mod.getHelp()))
			index += 1

def calculateMD5(binary):
	hasher = hashlib.md5()
	hasher.update(binary)
	md5 = hasher.hexdigest()
	return md5

def getFiletype(binary):
	return magic.from_buffer(binary)


def createFile(analysingFile):
	if not os.path.exists(analysingFile.getDirectory()):
		os.makedirs(analysingFile.getDirectory())
		with open(os.path.join(analysingFile.getDirectory(), analysingFile.getName()), "wb+") as f:
			f.write(analysingFile.getBinary())

def generateReport(analysingFile, modulesToUse):
	report = {}
	for moduleToUse in modulesToUse:
		module = modules[moduleToUse["id"]]
		if (module.isActive() and module.getMod().validFor(analysingFile)):
			report[module.getName()] = module.getMod().generateReport(analysingFile, moduleToUse["params"])
	return report

def getExistingReport(directory):
	report = {}
	with open(os.path.join(directory,FILENAME),"r") as file:
		report = file.read()
	return json.loads(report)

def saveReport(analysingFile, report):
	with open(os.path.join(analysingFile.getDirectory(),FILENAME),"w") as file:
		file.write(json.dumps(report))

def run(binary, modulesToUse):
	md5 = calculateMD5(binary)
	directory = ANALIZEDDIRECTORY+md5 + SLASH
	filetype = getFiletype(binary)
	analysingFile = AnalysingFile(binary, directory, md5, filetype)
	createFile(analysingFile)
	report = generateReport(analysingFile, modulesToUse)
	saveReport(analysingFile, report)
	return md5

def viewReport(name):
	directory = os.path.join(ANALIZEDDIRECTORY,name)
	if not os.path.exists(directory):
		return None
	else:
		return getExistingReport(directory)

def getModules():
	array = []
	for module in modules:
		if module.isActive:
			mod = {}
			mod['name']=module.getName()
			mod['index']=module.getIndex()
			mod['params']=module.getParams()
			mod['help']=module.getHelp()
			array.append(mod)
	return array

loadModules(MODULESPATH)
