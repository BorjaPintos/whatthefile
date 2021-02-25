# -*- coding: utf-8 -*-
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.ioutput import IOutput


class PrintOutput(IOutput):

    def __init__(self, params: dict = None):
        ""

    def dump_object(self, element: dict):
        print(element)

    def dump_list(self, elements: list):
        for element in elements:
            self.dump_object(element)
