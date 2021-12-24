# -*- coding: utf-8 -*-
from src.domain.targetfile import TargetFile
from src.modules.browserhistory.browsers.chromehistory import ChromeHistory
from src.modules.browserhistory.browsers.firefoxhistory import FirefoxHistory
from src.modules.browserhistory.browsers.ibrowserhistory import IBrowserHistory
from src.modules.browserhistory.browsers.safarihistory import SafaryHistory
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

    def _getBrowser(self, target_file: TargetFile) -> IBrowserHistory:
        if "History" in target_file.get_name():
            if ".db" in target_file.get_extension():
                return SafaryHistory(target_file.get_path())
            else:
                return ChromeHistory(target_file.get_path())
        else:
            if "places" in target_file.get_name():
                return FirefoxHistory(target_file.get_path())
        return None

    def _get_info(self, target_file: TargetFile) -> dict:
        browser = self._getBrowser(target_file)
        if browser:
            return {"downloads": browser.get_downloads(),
                    "visites": browser.get_visites(),
                    "searchs": browser.get_searchs()}
        return None

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "SQLite" in target_file.get_type() and ("History" in target_file.get_name() \
                    or "places" in target_file.get_name()):
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
