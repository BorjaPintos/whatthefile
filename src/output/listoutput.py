# -*- coding: utf-8 -*-
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.ioutput import IOutput


class ListOutput(IOutput):

    def __init__(self, params: dict = None):
        self._list = []

    def dump_object(self, element: dict):
        self._list.append(element)

    def dump_list(self, elements: list):
        self._list.extend(elements)

    def get_list(self):
        return self._list
