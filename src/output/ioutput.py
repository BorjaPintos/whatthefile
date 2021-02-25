# -*- coding: utf-8 -*-
from abc import abstractmethod

from src.domain.whatthefileconfiguration import WhatTheFileConfiguration


class IOutput:

    def __init__(self, params: dict = None):
        pass

    @abstractmethod
    def dump_object(self, element: dict):
        pass

    @abstractmethod
    def dump_list(self, elements: list):
        pass
