from domain.module import Module
import importlib
import os
import traceback

SLASH = "/"
MODULESDIR = "./modules"
MODULESPACKAGE = "modules."
MODULEMAIN = ".main"
MODULECONSTRUCTORCLASS = "Constructor"

class LoaderModules():

	def __init__(self):
		self.__modules = []
		self._loadModules(MODULESDIR)

	def get_modules(self):
		return self.__modules

	def _addModule(self, mod : Module):
		self.__modules.append(mod)
		print("Loaded module: [" + str(mod.getIndex()) + "] - " + mod.getName())

	def _loadModules(self, path : str):
		index = 0
		ls = self._listOnlyDir(path)
		for entry in ls:
			if (self._import_module(index, entry)):
				index += 1

	def _listOnlyDir(self, path : str):
		ls = os.listdir(path)
		directories = []
		for entry in ls:
			completePath = os.path.join(path, entry)
			if not os.path.isfile(completePath):
				directories.append(entry)
		return directories

	def _import_module(self, position : int, entry : str):
		try:
			mod = importlib.import_module(MODULESPACKAGE+entry+MODULEMAIN)
			py_mod = getattr(mod, MODULECONSTRUCTORCLASS)()
			self._addModule(Module(entry, position, py_mod, True, py_mod.getParams(), py_mod.getHelp()))
			return True
		except Exception as e:
			return False
		

	