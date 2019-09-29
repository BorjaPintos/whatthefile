# -*- coding: utf-8 -*-
import re

CODECOMMENTS = re.compile("/\*(?:.|[\r\n])*?\*/|(?://.*)")
HTMLCOMMENTS = re.compile("<!--(?:.|[\r\n])*?-->")
SCRIPTCOMMENTS = re.compile("(?:#.*)")

def getCodeComments(binary):
	return re.findall(CODECOMMENTS, binary.decode('utf-8'))

def getHTMLComments(binary):
	return re.findall(HTMLCOMMENTS, binary.decode('utf-8'))

def getScriptComments(binary):
	return re.findall(SCRIPTCOMMENTS, binary.decode('utf-8'))

def generateReportComments(binary):
	commentsDict = {}
	commentsDict['codeComments_//_/**/'] = getCodeComments(binary)
	commentsDict['htmlComments'] = getHTMLComments(binary)
	commentsDict['scriptComments'] = getScriptComments(binary)
	return commentsDict

def getHelp():
	return """Module to extract commets."""

def getParams():
  return []

def validFor(analysingFile):
	if ("ASCII text" in analysingFile.getFiletype()):
		return True
	return False

def generateReport(analysingFile, params):
	report = generateReportComments(analysingFile.getBinary())
	return report
