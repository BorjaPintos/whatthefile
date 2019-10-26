from abc import ABC, abstractmethod
from domain.targetfile import TargetFile


class IModule(ABC):

	def __init__(self):
		self._help = """Description for modules"""
		self._author = "Author"
		self._name = "ModuleName"
		self._params = []

	@abstractmethod
	def validFor(self, tartgetFile : TargetFile):
		pass

	@abstractmethod
	def generateReport(self, tartgetFile: TargetFile, userParams: list):
		pass

	def getHelp(self):
		return self._help

	def getParams(self):
		return self._params
	
	def getName(self):
		return self._name