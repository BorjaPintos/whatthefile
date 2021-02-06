# -*- coding: utf-8 -*-
from abc import abstractmethod

from src.domain.whatthefileconfiguration import WhatTheFileConfiguration


class IOutput:

    def __init__(self, conf: WhatTheFileConfiguration = None):
        pass

    @abstractmethod
    def dump(self, element: dict):
        pass
