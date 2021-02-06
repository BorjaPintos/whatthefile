# -*- coding: utf-8 -*-
from src.output.ioutput import IOutput


class PrintOutput(IOutput):

    def __init__(self, conf: dict = None):
        ""

    def dump(self, element: dict):
        print(element)