# -*- coding: utf-8 -*-
import os

from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.ioutput import IOutput


class FileOutput(IOutput):

    def __init__(self, params: dict = None):
        print()
        self._outfile = open(params["path"], "w+")

    def __del__(self):
        if self._outfile:
            self._outfile.close()

    def dump_object(self, element: dict):
        self._outfile.write(str(element) + os.linesep)

    def dump_list(self, elements: list):
        for element in elements:
            self.dump_object(element)