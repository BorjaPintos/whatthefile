# -*- coding: utf-8 -*-
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.ioutput import IOutput


class PrintOutput(IOutput):

    def __init__(self, conf: WhatTheFileConfiguration = None):
        ""

    def dump(self, element: dict):
        print(element)