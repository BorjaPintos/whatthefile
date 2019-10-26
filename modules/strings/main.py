# -*- coding: utf-8 -*-
import string
from modules.imodule import IModule

MIN = "charMin"

class Constructor(IModule):

	def __init__(self):
		self._name = "strings"
		self._help = """Module to extract strings from file.
			param: [""" + MIN + """] is the minimum length that the strings must have"""
		self._author = "BorjaPintos"
		self._params = [MIN+"=4"]


	def _strings(self, binary, min):
		bytesPrintables = []
		for char in string.printable:
			bytesPrintables.append(char.encode("utf-8"))
		words = []
		result = ""
		# c es un entero pero necesita pasarse a 1 byte
		for c in binary:
			byte = c.to_bytes(1, byteorder='big')
			if byte in bytesPrintables:
				result += byte.decode("utf-8")
				continue
			if len(result) >= min:
				words.append(result)
			result = ""
		return words

	def _generateReportStrings(self, targetFile, min):
		return self._strings(targetFile.getBinary(), min)

	def validFor(self, targetFile):
		if ("ASCII text" in targetFile.getFiletype()):
			return False
		return True

	def _getMinParam(self, params):
		for param in params:
			if MIN in param:
				return param.split("=")[1]

	def generateReport(self, targetFile, params):
		try:
			min = int(self._getMinParam(params))
			if (min):
				report = self._generateReportStrings(targetFile, min)
		except:
			report = {"error":"invalid argument for module"}
		return report
