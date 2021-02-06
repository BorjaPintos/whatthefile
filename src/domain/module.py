# -*- coding: utf-8 -*-
from src.modules.imodule import IModule


class Module():
    def __init__(self, name: str, index: int, mod: IModule):
        self._name = name
        self._index = index
        self._mod = mod

    def get_name(self) -> str:
        return self._name

    def get_index(self) -> int:
        return self._index

    def get_mod(self) -> IModule:
        return self._mod
