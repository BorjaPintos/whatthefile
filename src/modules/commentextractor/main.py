# -*- coding: utf-8 -*-
import re

from src.domain.targetfile import TargetFile
from src.modules.imodule import IModule
from src.domain.targetpath import TargetPath

CODECOMMENTS = re.compile(r"/\*(?:.|[\r\n])*?\*/|(?://.*)")
XMLCOMMENTS = re.compile("<!--(?:.|[\r\n])*?-->")
SHARPCOMMENTS = re.compile("(?:#.*)")


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "commentextractor"
        self._help = """Module to extract comments"""
        self._author = "BorjaPintos"
        self._params = None

    def _get_code_comments(self, binary):
        return re.findall(CODECOMMENTS, binary.decode('utf-8'))

    def _get_XML_comments(self, binary):
        return re.findall(XMLCOMMENTS, binary.decode('utf-8'))

    def _get_sharp_comments(self, binary):
        return re.findall(SHARPCOMMENTS, binary.decode('utf-8'))

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "ASCII text" in target_file.get_type():
                return True
            if "UTF-8 Unicode text" in target_file.get_type():
                return True
        return False

    def run(self, target_file: TargetFile):
        binary = target_file.get_binary()
        result = {}
        if target_file.get_extension() in [".c", ".cpp", ".java", ".js", ".php", ".sql"]:
            result["//_/**/_comments"] = self._get_code_comments(binary)
        if target_file.get_extension() in [".xml", ".html", ".htm", ".xhtml", ".jhtml", ".php"]:
            result["<!--->Comments"] = self._get_XML_comments(binary)
        if target_file.get_extension() in [".sh", ".py", ".rb", ".yml", ".yaml" ".pl"]:
            result["#_comments"] = self._get_sharp_comments(binary)
        return result
