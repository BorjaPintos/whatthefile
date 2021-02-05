# -*- coding: utf-8 -*-
from src.domain.targetfile import TargetFile
from src.modules.imodule import IModule


class Constructor(IModule):

    def __init__(self):
        self._name = "basic"
        self._help = """Module to calculate filetype"""
        self._author = "BorjaPintos"
        self._params = None

    def is_valid_for(self, target_file: TargetFile):
        return True

    def run(self, target_file: TargetFile, params: dict = None):
        return {'filetype': target_file.get_filetype()}
