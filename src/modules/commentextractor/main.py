# -*- coding: utf-8 -*-
import re

from src.domain.targetfile import TargetFile
from src.modules.imodule import IModule
from src.domain.targetpath import TargetPath

CODECOMMENTS = re.compile("/\*(?:.|[\r\n])*?\*/|(?://.*)")
HTMLCOMMENTS = re.compile("<!--(?:.|[\r\n])*?-->")
BASHCOMMENTS = re.compile("(?:#.*)")


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "commentextractor"
        self._help = """Module to extract commets"""
        self._author = "BorjaPintos"
        self._params = None

    def _getCodeComments(self, binary):
        return re.findall(CODECOMMENTS, binary.decode('utf-8'))

    def _getHTMLComments(self, binary):
        return re.findall(HTMLCOMMENTS, binary.decode('utf-8'))

    def _getScriptComments(self, binary):
        return re.findall(BASHCOMMENTS, binary.decode('utf-8'))

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "ASCII text" in target_file.get_type():
                return True
        return False

    def run(self, target_file: TargetFile):
        """TODO Filtrar por excensiones conocidas."""
        binary = target_file.get_binary()
        result = {'codeComments_//_/**/': self._getCodeComments(binary),
                  'htmlComments': self._getHTMLComments(binary),
                  'bashComments': self._getScriptComments(binary)}
        return result
