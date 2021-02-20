# -*- coding: utf-8 -*-
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
from tika import parser

TIKA_SERVER_URL = "tika_server_url"


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "tikaparser"
        self._help = """Module to extract text fom documents (pdfs, office...)"""
        self._author = "BorjaPintos"

    def _extract_text(self, path: str, url: str = None):
        if url is not None:
            parsed = parser.from_file(path, url)
        else:
            parsed = parser.from_file(path)
        return parsed["content"]

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "PDF document" in target_file.get_type():
                return True
            elif "Composite Document" in target_file.get_type():
                return True
            elif "OpenDocument" in target_file.get_type():
                return True
            elif "Microsoft Word" in target_file.get_type():
                return True
            elif "Microsoft Excel" in target_file.get_type():
                return True
            elif "Microsoft PowerPoint" in target_file.get_type():
                return True
            if isinstance(target_file, TargetFile):
                if target_file.get_extension() in [".pages", ".numbers", ".keynote"]:
                    return True
        return False

    def _get_server_param(self):
        if self.get_params() is not None and TIKA_SERVER_URL in self.get_params():
            return self.get_params()[TIKA_SERVER_URL]
        return None

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        return {"content": self._extract_text(target_file.get_path(), self._get_server_param())}
