# -*- coding: utf-8 -*-
from abc import abstractmethod


class IOutput:

    def __init__(self, conf: dict = None):
        ""

    @abstractmethod
    def dump(self, element: dict):
        pass
