# -*- coding: utf-8 -*-
import re
from modules.imodule import IModule

CODECOMMENTS = re.compile("/\*(?:.|[\r\n])*?\*/|(?://.*)")
HTMLCOMMENTS = re.compile("<!--(?:.|[\r\n])*?-->")
SCRIPTCOMMENTS = re.compile("(?:#.*)")

class Constructor(IModule):

	def __init__(self):
		self._name = "commentextractor"
		self._help = """Module to extract commets"""
		self._author = "BorjaPintos"
		self._params = []

	def _getCodeComments(self, binary):
		return re.findall(CODECOMMENTS, binary.decode('utf-8'))

	def _getHTMLComments(self, binary):
		return re.findall(HTMLCOMMENTS, binary.decode('utf-8'))

	def _getScriptComments(self, binary):
		return re.findall(SCRIPTCOMMENTS, binary.decode('utf-8'))

	def validFor(self, targetFile):
		if ("ASCII text" in targetFile.getFiletype()):
			return True
		return False

	def generateReport(self, targetFile, params):
		binary = targetFile.getBinary()
		commentsDict = {}
		commentsDict['codeComments_//_/**/'] = self._getCodeComments(binary)
		commentsDict['htmlComments'] = self._getHTMLComments(binary)
		commentsDict['scriptComments'] = self._getScriptComments(binary)
		return commentsDict
