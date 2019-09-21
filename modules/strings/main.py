# -*- coding: utf-8 -*-
import string

MIN = "charMin"

def strings(binary, min):
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

def generateReportStrings(analysingFile, min):
	return strings(analysingFile.getBinary(), min)

def validFor(analysingFile):
	if ("ASCII text" in analysingFile.getFiletype()):
		return False
	return True

def getParams():
  return [MIN+"=4"]

def getMinParam(params):
	for param in params:
		if MIN in param:
			return param.split("=")[1]

def generateReport(analysingFile, params):
	try:
		min = int(getMinParam(params))
		if (min):
			report = generateReportStrings(analysingFile, min)
	except:
		report = {"error":"invalid argument for module"}
	return report
