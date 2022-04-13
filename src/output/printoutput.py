# -*- coding: utf-8 -*-
from src.output.ioutput import IOutput


class PrintOutput(IOutput):

    def __init__(self, params: dict = None):
        super().__init__()

    def _dump_object(self, element: dict):
        print(element)

    def _dump_list(self, elements: list):
        for element in elements:
            self.dump_object(element)
