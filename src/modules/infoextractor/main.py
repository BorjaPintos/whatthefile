# -*- coding: utf-8 -*-
import re
from typing import List

from src.domain.targetfile import TargetFile
from src.modules.imodule import IModule
from src.domain.targetpath import TargetPath
from src.utils.log import Log

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

    def _get_emails(self, string: str) -> list:
        return re.findall(EMAILS, string)

    def _get_urls(self, string: str) -> list:
        url_list = []
        for group1, group2 in re.findall(URLS, string):
            url_list.append(group1)
        return url_list

    def _get_ibans(self, string: str) -> list:
        return re.findall(IBAN, string)

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            return True
        return False

    def _clean(self, result: dict) -> dict:
        properties = ["emails", "URLs", "IBANs"]
        for property in properties:
            if len(result[property]) == 0:
                del result[property]
        return result

    def _get_info_module_strings(self, result_of_previos_modules: dict) -> dict:
        if "strings" in result_of_previos_modules and "elements" in result_of_previos_modules["strings"]:
            strings = result_of_previos_modules["strings"]["elements"]
            return {"emails": self._get_emails(strings),
                    "URLs": self._get_urls(strings),
                    "IBANs": self._get_ibans(strings)}
        return {}

    def _get_info_module_tika(self, result_of_previos_modules: dict) -> dict:
        if "tikaparser" in result_of_previos_modules and "content" in result_of_previos_modules["tikaparser"]:
            content = result_of_previos_modules["tikaparser"]["content"]
            return {"emails": self._get_emails(content),
                    "URLs": self._get_urls(content),
                    "IBANs": self._get_ibans(content)}
        return {}

    def _get_info_module_metadata(self, result_of_previos_modules: dict) -> dict:
        if "metadata" in result_of_previos_modules and "values" in result_of_previos_modules["metadata"]:
            values = ""
            for value in result_of_previos_modules["metadata"]["values"]:
                # reunimos todos los values en una linea para hacer el parseo más sencillo
                values = values + " " + str(value)

            return {"emails": self._get_emails(values),
                    "URLs": self._get_urls(values),
                    "IBANs": self._get_ibans(values)}
        return {}

    def _get_info_module_qrbcreader(self, result_of_previos_modules: dict) -> dict:
        if "qrbcreader" in result_of_previos_modules:
            qrbcs = ""
            for key in result_of_previos_modules["qrbcreader"]:
                # reunimos todos los qrbc en una linea para hacer el parseo más sencillo
                qrbcs = qrbcs + " " + str(result_of_previos_modules["qrbcreader"][key])

            return {"emails": self._get_emails(qrbcs),
                    "URLs": self._get_urls(qrbcs),
                    "IBANs": self._get_ibans(qrbcs)}
        return {}

    def _get_info_module_certificatereader(self, result_of_previos_modules: dict) -> dict:
        result = {}
        if "certificatereader" in result_of_previos_modules:

            result = {"emails": [],
                      "URLs": [],
                      "IBANs": []}
            if "issuer" in result_of_previos_modules["certificatereader"]:
                issuer = result_of_previos_modules["certificatereader"]["issuer"]
                result["emails"] = self._get_emails(issuer)
                result["URLs"] = self._get_urls(issuer)
                result["IBANs"] = self._get_ibans(issuer)
            if "subject" in result_of_previos_modules["certificatereader"]:
                subject = result_of_previos_modules["certificatereader"]["subject"]
                result["emails"] = self._get_emails(subject)
                result["URLs"] = self._get_urls(subject)
                result["IBANs"] = self._get_ibans(subject)

        return result

    def _get_info_module_ocrtesseract(self, result_of_previos_modules: dict) -> dict:
        if "ocrtesseract" in result_of_previos_modules:
            text = ""
            if "Thresh" in result_of_previos_modules["ocrtesseract"]:
                text = text + "" + str(result_of_previos_modules["ocrtesseract"])
            if "Blur" in result_of_previos_modules["ocrtesseract"]["Thresh"]:
                text = text + "" + str(result_of_previos_modules["ocrtesseract"]["Blur"])

            return {"emails": self._get_emails(text),
                    "URLs": self._get_urls(text),
                    "IBANs": self._get_ibans(text)}
        return {}

    def _get_info_from_binary(self, target_file: TargetFile) -> dict:
        if "ASCII text" or "UTF-8 Unicode text" in target_file.get_type():
            "obtenemos los datos del propio binario"
            string = target_file.get_binary().decode('utf-8')
            return {"emails": self._get_emails(string),
                    "URLs": self._get_urls(string),
                    "IBANs": self._get_ibans(string)}
        return {}

    def _get_info_from_path(self, target_file: TargetFile) -> dict:
        path = target_file.get_path()
        return {"emails": self._get_emails(path),
                "URLs": self._get_urls(path),
                "IBANs": self._get_ibans(path)}

    def _fusion_resuls(self, results: List[dict]) -> dict:
        keys = ["emails", "URLs", "IBANs"]
        final_result = {}
        for key in keys:
            final_result[key] = []
        for result in results:
            for key in keys:
                if key in result:
                    final_result[key].extend(result[key])
        return final_result

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:

        results = [
            self._get_info_from_binary(target_file),
            self._get_info_from_path(target_file),
            self._get_info_module_tika(result_of_previos_modules),
            self._get_info_module_strings(result_of_previos_modules),
            self._get_info_module_certificatereader(result_of_previos_modules),
            self._get_info_module_metadata(result_of_previos_modules),
            self._get_info_module_qrbcreader(result_of_previos_modules),
            self._get_info_module_ocrtesseract(result_of_previos_modules)
        ]
        return self._clean(self._fusion_resuls(results))
