from abc import ABC, abstractmethod
from src.domain.targetpath import TargetPath


class IModule(ABC):

    def __init__(self):
        self._help = """Description for modules"""
        self._author = "Author"
        self._name = "ModuleName"
        self._params = {}

    @abstractmethod
    def is_valid_for(self, target_file: TargetPath) -> bool:
        pass

    @abstractmethod
    def run(self, target_file: TargetPath, result_of_previos_modules: dict) -> dict:
        pass

    def get_help(self) -> str:
        return self._help

    def get_params(self) -> dict:
        return self._params

    def set_params(self, params: dict) -> None:
        self._params = params

    def get_name(self) -> str:
        return self._name
