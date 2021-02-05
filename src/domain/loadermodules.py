from src.domain.module import Module
import importlib
import os
import traceback


"""Cargara todos los modulos que se llamen main y tengan una clase llamada 'Constructor' 
del path que se le pase como parámetro
Estos módulos deben seguir la interfaz src/modules/IModule
"""

class LoaderModules:

    def __init__(self, relative_modules_path: str):
        self.__modules = []
        "como es relativa necesitamos quitar el primer './' para que quede en formato de modulos"
        self._modules_package = relative_modules_path.replace("/", ".")[2:]
        self._load_modules(relative_modules_path)


    def get_modules(self):
        return self.__modules

    def _add_module(self, mod: Module):
        self.__modules.append(mod)
        print("Loaded module: [" + str(mod.getIndex()) + "] - " + mod.getName())

    def _load_modules(self, path: str):
        index = 0
        ls = self._list_only_dir(path)
        for entry in ls:
            if self._import_module(index, entry):
                index += 1

    @staticmethod
    def _list_only_dir(path: str):
        ls = os.listdir(path)
        directories = []
        for entry in ls:
            complete_path = os.path.join(path, entry)
            if not os.path.isfile(complete_path):
                directories.append(entry)
        return directories

    def _import_module(self, position: int, entry: str):
        try:
            if entry == "__pycache__":
                return False
            mod = importlib.import_module(self._modules_package + "." + entry + ".main")
            py_mod = getattr(mod, "Constructor")()
            self._add_module(Module(entry, position, py_mod, True, py_mod.get_params(), py_mod.get_help()))
            return True
        except Exception:
            print("Error loading module: ["  + self._modules_package + "." + entry + ".main" + "]")
            traceback.print_exc()
            return False
