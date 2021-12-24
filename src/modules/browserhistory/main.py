# -*- coding: utf-8 -*-
from typing import List
import traceback
from src.domain.targetfile import TargetFile
from src.modules.browserhistory.browsers import chromebrowser
from src.modules.imodule import IModule
from src.domain.targetpath import TargetPath
from src.output import utils


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "browserhistory"
        self._help = """Module to extract history from browsers"""
        self._author = "BorjaPintos"
        self._params = None

    def _get_downloads(self, target_file: TargetFile) -> List:
        if "History" in target_file.get_name():
            try:
                return chromebrowser.get_downloads(target_file.get_path())
            except:
                traceback.print_exc()
            return []

    def _get_visites(self, target_file: TargetFile) -> List:
        if "History" in target_file.get_name():
            try:
                return chromebrowser.get_visites(target_file.get_path())
            except:
                traceback.print_exc()
            return []

    def _get_searchs(self, target_file: TargetFile) -> List:
        if "History" in target_file.get_name():
            try:
                return chromebrowser.get_searchs(target_file.get_path())
            except:
                traceback.print_exc()
            return []

    def _get_info(self, target_file: TargetFile) -> dict:
        result = {"downloads": self._get_downloads(target_file),
                  "visites": self._get_visites(target_file),
                  "searchs": self._get_searchs(target_file)}
        return result

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "SQLite" in target_file.get_type() and "History" in target_file.get_name():
                return True
        return False

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        history = self._get_info(target_file)
        utils.pipe_to_another_output(self._params, history["downloads"])
        utils.pipe_to_another_output(self._params, history["visites"])
        piped = utils.pipe_to_another_output(self._params, history["searchs"])
        return {
            "n_downloads": len(history["downloads"]),
            "n_visites": len(history["visites"]),
            "n_searchs": len(history["searchs"])
        } if piped else history
