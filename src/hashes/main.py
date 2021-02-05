# -*- coding: utf-8 -*-
import hashlib
#import ssdeep
def calculateMD5(binary):
	hasher = hashlib.md5()
	hasher.update(binary)
	md5 = hasher.hexdigest()
	return md5

def calculateSHA1(binary):
	hasher = hashlib.sha1()
	hasher.update(binary)
	sha1 = hasher.hexdigest()
	return sha1

def calculateSHA224(binary):
	hasher = hashlib.sha224()
	hasher.update(binary)
	sha224 = hasher.hexdigest()
	return sha224

def calculateSHA256(binary):
	hasher = hashlib.sha256()
	hasher.update(binary)
	sha256 = hasher.hexdigest()
	return sha256

def calculateSHA384(binary):
	hasher = hashlib.sha384()
	hasher.update(binary)
	sha384 = hasher.hexdigest()
	return sha384

def calculateSHA512(binary):
	hasher = hashlib.sha512()
	hasher.update(binary)
	sha512 = hasher.hexdigest()
	return sha512

def calculateSHA3_224(binary):
	hasher = hashlib.sha3_224()
	hasher.update(binary)
	hash = hasher.hexdigest()
	return hash

def calculateSHA3_256(binary):
	hasher = hashlib.sha3_256()
	hasher.update(binary)
	hash = hasher.hexdigest()
	return hash

def calculateSHA3_384(binary):
	hasher = hashlib.sha3_384()
	hasher.update(binary)
	hash = hasher.hexdigest()
	return hash

def calculateSHA3_512(binary):
	hasher = hashlib.sha3_512()
	hasher.update(binary)
	hash = hasher.hexdigest()
	return hash
"""
Parece ser que de momento esto solo funciona para linux, tengo que hacer más pruebas para ver como lo instalo en mac
def calculateSsdeep(binary):
	return ssdeep.hash(binary)
"""

def generateReportHashes(analysingFile):
	hashesDict = {}
	hashesDict['MD5'] = calculateMD5(analysingFile.getBinary())
	hashesDict['SHA1'] = calculateSHA1(analysingFile.getBinary())
	hashesDict['SHA224'] = calculateSHA224(analysingFile.getBinary())
	hashesDict['SHA256'] = calculateSHA256(analysingFile.getBinary())
	hashesDict['SHA384'] = calculateSHA384(analysingFile.getBinary())
	hashesDict['SHA512'] = calculateSHA512(analysingFile.getBinary())
	hashesDict['SHA3_224'] = calculateSHA3_224(analysingFile.getBinary())
	hashesDict['SHA3_256'] = calculateSHA3_256(analysingFile.getBinary())
	hashesDict['SHA3_384'] = calculateSHA3_384(analysingFile.getBinary())
	hashesDict['SHA3_512'] = calculateSHA3_512(analysingFile.getBinary())
	#hashesDict['SSDEEP'] = calculateSsdeep(analysingFile.getBinary())
	return hashesDict

def getHelp():
	return """Module to calculate hashes: 
		MD5, SHA1, SHA224, SHA156, SHA384, SHA512, SHA3_224, SHA3_256, SHA3_384, SHA3_512."""

def getParams():
  return []

def validFor(analysingFile):
	return True

def generateReport(analysingFile, params):
	report = generateReportHashes(analysingFile)
	return report
