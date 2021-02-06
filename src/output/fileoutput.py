# -*- coding: utf-8 -*-
import os

from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.ioutput import IOutput


class FileOutput(IOutput):

    def __init__(self, conf: WhatTheFileConfiguration = None):
        custom_configuration = conf.get_section("output.file")
        self._outfile = open(custom_configuration["path"], "w+")

    def __del__(self):
        if self._outfile:
            self._outfile.close()

    def dump(self, element: dict):
        self._outfile.write(str(element) + os.linesep)