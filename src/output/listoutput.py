# -*- coding: utf-8 -*-
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.ioutput import IOutput


class ListOutput(IOutput):

    def __init__(self, params: dict = None):
        super().__init__()
        self._list = []

    def _dump_object(self, element: dict):
        self._list.append(element)

    def _dump_list(self, elements: list):
        self._list.extend(elements)

    def get_list(self):
        return self._list
