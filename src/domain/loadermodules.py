from typing import List
from src.domain.module import Module
import importlib
import traceback

from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.utils.log import Log

"""Cargará todos los modulos que se llamen main y tengan una clase llamada 'Constructor' 
del path que se le pase como parámetro
Estos módulos deben seguir la interfaz src/modules/IModule
"""


class LoaderModules:

    def __init__(self, conf: WhatTheFileConfiguration):
        self.__modules = []
        self._load_modules(conf)

    def get_modules(self) -> List[Module]:
        return self.__modules

    def _load_modules(self, conf: WhatTheFileConfiguration) -> None:
        module_index = 0
        for module_section_name in conf.get_modules_section_names():
            if conf.get_property_boolean(module_section_name, "active"):
                Log.info("Loading module: [" + module_section_name + "]")
                mod = self._import_module(conf, module_section_name, module_index)
                if mod is not None:
                    module_index += 1
                    self.__modules.append(mod)
                    Log.info("Module loaded successfully: [" + str(mod.get_index()) + "] - " + mod.get_name())
                else:
                    Log.error("Error loading module: [" + module_section_name + "]")

    @staticmethod
    def _import_module(conf: WhatTheFileConfiguration, module_section_name, position: int) -> Module:
        module_name = module_section_name.split(".")[1]
        try:
            mod = importlib.import_module(
                conf.get_property("whatthefile", "modules_package") + "." + module_name + ".main")
            py_mod = getattr(mod, "Constructor")()
            configuration = conf.get_whatthefile_secction()
            configuration.update(conf.get_section(module_section_name))
            py_mod.set_params(configuration)
            return Module(module_name, position, py_mod)
        except:
            traceback.print_exc()
            return None
