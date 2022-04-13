# -*- coding: utf-8 -*-
import re
from typing import List

EMAILS = re.compile(r"[\w.+]+@[a-zA-Z_]+?\.[a-zA-Z]{2,4}")
URLS = re.compile(r"""(([a-zA-Z]+://){1}[^'"\s]+)""")
IBAN = re.compile(
    r"[A-Z]{2}\d{22}|[A-Z]{2}\d{2}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}|[A-Z]{2}\d{2}[-]\d{4}[-]\d{4}[-]\d{4}[-]\d{4}[-]\d{4}")
BITCOIN = re.compile(r"([13]{1}[a-km-zA-HJ-NP-Z1-9]{26,33}|bc1[a-z0-9]{39,59})")


class Infoextractor:

    def __init__(self):
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

    def _get_bitcoin_address(self, string: str) -> list:
        return re.findall(BITCOIN, string)

    def _clean(self, result: dict) -> dict:
        properties = ["emails", "URLs", "IBANs", "Bitcoin"]
        for property in properties:
            if len(result[property]) == 0:
                del result[property]
        return result

    def _get_info_module_strings(self, resume: dict) -> dict:
        try:

            if "strings" in resume and "elements" in resume["strings"]:
                strings = resume["strings"]["elements"]
                return {"emails": self._get_emails(strings),
                        "URLs": self._get_urls(strings),
                        "IBANs": self._get_ibans(strings),
                        "Bitcoin": self._get_bitcoin_address(strings)}
        except:
            pass
        return {}

    def _get_info_module_tika(self, resume: dict) -> dict:
        try:
            if "tikaparser" in resume and "content" in resume["tikaparser"]:
                content = resume["tikaparser"]["content"]
                return {"emails": self._get_emails(content),
                        "URLs": self._get_urls(content),
                        "IBANs": self._get_ibans(content),
                        "Bitcoin": self._get_bitcoin_address(content)}
        except:
            pass
        return {}

    def _get_info_module_metadata(self, resume: dict) -> dict:
        try:
            if "metadata" in resume and "values" in resume["metadata"]:
                values = ""
                for value in resume["metadata"]["values"]:
                    # reunimos todos los values en una linea para hacer el parseo más sencillo
                    values = values + " " + str(value)

                return {"emails": self._get_emails(values),
                        "URLs": self._get_urls(values),
                        "IBANs": self._get_ibans(values),
                        "Bitcoin": self._get_bitcoin_address(values)}
        except:
            pass
        return {}

    def _get_info_module_qrbcreader(self, resume: dict) -> dict:
        try:
            if "qrbcreader" in resume:
                qrbcs = ""
                for key in resume["qrbcreader"]:
                    # reunimos todos los qrbc en una linea para hacer el parseo más sencillo
                    qrbcs = qrbcs + " " + str(resume["qrbcreader"][key])

                return {"emails": self._get_emails(qrbcs),
                        "URLs": self._get_urls(qrbcs),
                        "IBANs": self._get_ibans(qrbcs),
                        "Bitcoin": self._get_bitcoin_address(qrbcs)}
        except:
            pass
        return {}

    def _get_info_module_pstostparser(self, resume: dict) -> dict:
        try:
            if "pstostparser" in resume and "messages" in resume["pstostparser"]:
                return self._get_info_module_pstostparser_first_output(resume)
            else:
                if "html_body" in resume or "plain_text_body" in resume or "headers" in resume:
                    return self._get_info_module_pstostparser_second_output(resume)
        except:
            pass
        return {}

    def _get_info_module_pstostparser_first_output(self, resume: dict) -> dict:
        try:
            all_messages = ""
            for message in resume["pstostparser"]["messages"]:
                all_messages = all_messages + " " + str(message["html_body"]) + " " \
                               + str(message["plain_text_body"]) + " " + str(message["headers"])

            return {"emails": self._get_emails(all_messages),
                    "URLs": self._get_urls(all_messages),
                    "IBANs": self._get_ibans(all_messages),
                    "Bitcoin": self._get_bitcoin_address(all_messages)}
        except:
            pass
        return {}

    def _get_info_module_pstostparser_second_output(self, resume: dict) -> dict:
        try:
            message = ""
            if "html_body" in resume:
                message += str(resume["html_body"])
            if "plain_text_body" in resume:
                message += " " + str(resume["plain_text_body"])
            if "headers" in resume:
                message += " " + str(resume["headers"])
            return {"emails": self._get_emails(message),
                    "URLs": self._get_urls(message),
                    "IBANs": self._get_ibans(message),
                    "Bitcoin": self._get_bitcoin_address(message)}
        except:
            pass
        return {}

    def _get_info_module_certificatereader(self, resume: dict) -> dict:
        result = {}
        try:
            if "certificatereader" in resume:

                result = {"emails": [],
                          "URLs": [],
                          "IBANs": []}
                if "issuer" in resume["certificatereader"]:
                    issuer = resume["certificatereader"]["issuer"]
                    result["emails"].extend(self._get_emails(issuer))
                    result["URLs"].extend(self._get_urls(issuer))
                    result["IBANs"].extend(self._get_ibans(issuer))
                    result["Bitcoin"].extend(self._get_bitcoin_address(issuer))
                if "subject" in resume["certificatereader"]:
                    subject = resume["certificatereader"]["subject"]
                    result["emails"].extend(self._get_emails(subject))
                    result["URLs"].extend(self._get_urls(subject))
                    result["IBANs"].extend(self._get_ibans(subject))
                    result["Bitcoin"].extend(self._get_bitcoin_address(subject))
        except:
            pass

        return result

    def _get_info_module_ocrtesseract(self, resume: dict) -> dict:
        try:
            if "ocrtesseract" in resume:
                text = ""
                if "Thresh" in resume["ocrtesseract"]:
                    text = text + "" + str(resume["ocrtesseract"])
                if "Blur" in resume["ocrtesseract"]["Thresh"]:
                    text = text + "" + str(resume["ocrtesseract"]["Blur"])

                return {"emails": self._get_emails(text),
                        "URLs": self._get_urls(text),
                        "IBANs": self._get_ibans(text),
                        "Bitcoin": self._get_bitcoin_address(text)}
        except:
            pass
        return {}

    def _get_info_from_path(self, resume: dict) -> dict:
        try:
            path = resume["path"]
            return {"emails": self._get_emails(path),
                    "URLs": self._get_urls(path),
                    "IBANs": self._get_ibans(path),
                    "Bitcoin": self._get_bitcoin_address(path)}

        except:
            pass
        return {}

    def _fusion_resuls(self, results: List[dict]) -> dict:
        keys = ["emails", "URLs", "IBANs", "Bitcoin"]
        final_result = {}
        for key in keys:
            final_result[key] = []
        for result in results:
            for key in keys:
                if key in result:
                    final_result[key].extend(result[key])
        return final_result

    def run(self, resume: dict) -> dict:
        results = [
            self._get_info_from_path(resume),
            self._get_info_module_tika(resume),
            self._get_info_module_strings(resume),
            self._get_info_module_certificatereader(resume),
            self._get_info_module_metadata(resume),
            self._get_info_module_qrbcreader(resume),
            self._get_info_module_ocrtesseract(resume),
            self._get_info_module_pstostparser(resume)
        ]
        return self._clean(self._fusion_resuls(results))
