from abc import ABC, abstractmethod
from src.domain.targetfile import TargetFile


class IModule(ABC):

    def __init__(self):
        self._help = """Description for modules"""
        self._author = "Author"
        self._name = "ModuleName"
        self._params = []

    @abstractmethod
    def is_valid_for(self, target_file: TargetFile):
        pass

    @abstractmethod
    def run(self, target_file: TargetFile, params: dict = None):
        pass

    def get_help(self):
        return self._help

    def get_params(self):
        return self._params

    def get_name(self):
        return self._name
