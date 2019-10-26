# -*- coding: utf-8 -*-
from modules.imodule import IModule

class Constructor(IModule):
	
	def __init__(self):
		self._name = "basic"
		self._help = """Module to calculate filetype"""
		self._author = "BorjaPintos"
		self._params = []
			

	def validFor(self, targetfile):
		return True

	def generateReport(self, targetfile, params : list):
		basicDict = {}
		basicDict['filetype'] = targetfile.getFiletype()
		return basicDict
