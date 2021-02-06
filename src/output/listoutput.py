# -*- coding: utf-8 -*-
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.ioutput import IOutput


class ListOutput(IOutput):

    def __init__(self, conf: WhatTheFileConfiguration = None):
        self._list = []

    def dump(self, element: dict):
        self._list.append(element)

    def get_list(self):
        return self._list