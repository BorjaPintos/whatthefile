# -*- coding: utf-8 -*-
import math

def entropy(binary):
    fileSize = len(binary)
 
    # calculate the frequency of each byte value in the file
    freqList = []
    for b in range(256):
        ctr = 0
        for byte in binary:
            if byte == b:
                ctr += 1
        freqList.append(float(ctr) / fileSize)
 
    # Shannon entropy
    ent = 0.0
    for freq in freqList:
        if freq > 0:
            ent = ent + freq * math.log(freq, 2)
    ent = -ent
    return ent

def generateReportEntropy(analysingFile):
	return entropy(analysingFile.getBinary())

def validFor(analysingFile):
	return True

def getHelp():
	return """Module to calculate Shannon entropy"""

def getParams():
  return []

def generateReport(analysingFile, params):
	report = generateReportEntropy(analysingFile)
	return report
