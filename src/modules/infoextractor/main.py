# -*- coding: utf-8 -*-
import re

from src.domain.targetfile import TargetFile
from src.modules.imodule import IModule
from src.domain.targetpath import TargetPath

EMAILS = re.compile(r"\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,4}")
URLS = re.compile(r"""(([a-zA-Z]+://){1}[^'"\s]+)""")
IBAN = re.compile(
    r"[A-Z]{2}\d{22}|[A-Z]{2}\d{2}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}|[A-Z]{2}\d{2}[-]\d{4}[-]\d{4}[-]\d{4}[-]\d{4}[-]\d{4}")


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "infotextractor"
        self._help = """Module to extract information like, emails, ulrs, ibans .."""
        self._author = "BorjaPintos"
        self._params = None

    def _get_emails(self, binary):
        return re.findall(EMAILS, binary.decode('utf-8'))

    def _get_urls(self, binary):
        url_list = []
        for group1, group2 in re.findall(URLS, binary.decode('utf-8')):
            url_list.append(group1)
        return url_list

    def _get_ibans(self, binary):
        return re.findall(IBAN, binary.decode('utf-8'))

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "ASCII text" in target_file.get_type():
                return True
            if "UTF-8 Unicode text" in target_file.get_type():
                return True
        return False

    def run(self, target_file: TargetFile):
        binary = target_file.get_binary()
        result = {"emails": self._get_emails(binary),
                  "URLs": self._get_urls(binary),
                  "IBANs": self._get_ibans(binary)}
        return result
