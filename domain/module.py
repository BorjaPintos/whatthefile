# -*- coding: utf-8 -*-

class Module():
	def __init__(self, name : str, index : int, mod, active : bool, params, help):
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
