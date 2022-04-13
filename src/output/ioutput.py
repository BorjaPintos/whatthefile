# -*- coding: utf-8 -*-
from abc import abstractmethod

from src.application.infoextractor.infoextactor import Infoextractor


class IOutput:

    def __init__(self, params: dict = None):
        self._infoextractor = Infoextractor()

    def dump_object(self, element: dict):
        element["infoextractor"] = self._infoextractor.run(element)
        self._dump_object(element)

    def dump_list(self, elements: list):
        for element in elements:
            element["infoextractor"] = self._infoextractor.run(element)
        self._dump_list(elements)

    @abstractmethod
    def _dump_object(self, element: dict):
        pass

    @abstractmethod
    def _dump_list(self, elements: list):
        pass
