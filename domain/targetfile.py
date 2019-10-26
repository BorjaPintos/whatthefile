# -*- coding: utf-8 -*-
import os
import magic
import hashlib

SLASH = "/"
GENERATEDFILES = "files"

class TargetFile():

	def __init__(self, directory : str, binary : bytes):
		self._binary = binary
		self._name = self._calculateMD5(binary)
		self._filetype = self._getFiletype(binary)
		self._directory = os.path.join(directory,self._name)
		self._createFile()
		self._generated_files_directory = os.path.join(self._directory, "files")
		if not os.path.exists(self._generated_files_directory):
			os.mkdir(self._generated_files_directory)
		

	def getBinary(self):
		return self._binary
	def getDirectory(self):
		return self._directory
	def getName(self):
		return self._name
	def getFiletype(self):
		return self._filetype
	def getCompletePath(self):
		return os.path.join(self._directory, self._name)
	def getGeneratedFilesDirectory(self):
		return self._generated_files_directory

	def _calculateMD5(self, binary : bytes):
		hasher = hashlib.md5()
		hasher.update(binary)
		md5 = hasher.hexdigest()
		return md5

	def _getFiletype(self, binary : bytes):
		return magic.from_buffer(binary)

	def _createFile(self):
		if not os.path.exists(self._directory):
			os.makedirs(self._directory)
			with open(os.path.join(self._directory, self._name), "wb+") as f:
				f.write(self._binary)
