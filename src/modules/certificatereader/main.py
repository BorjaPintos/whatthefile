# -*- coding: utf-8 -*-
from typing import List

from cryptography.x509 import Extension

from src.domain.targetfile import TargetFile
from src.modules.imodule import IModule
from src.domain.targetpath import TargetPath
from cryptography import x509

from src.utils.time import Time


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "certificatereader"
        self._help = """Module to extract information from certificates"""
        self._author = "BorjaPintos"
        self._params = None

    def _load_certificate(self, binary):
        try:
            return x509.load_pem_x509_certificate(binary)
        except:
            try:
                return x509.load_der_x509_certificate(binary)
            except:
                pass
        return {"error": "invalid certificate"}

    def _get_info(self, binary: bytes):
        cert = self._load_certificate(binary)
        if cert is None:
            return {"error": "invalid certificate"}

        return {
            "serial_number": cert.serial_number,
            "version": cert.version.name,
            "extensions": self._parse_extensions(cert.extensions._extensions),
            "nor_valid_after": Time.change_output_date_format_from_epoch(cert.not_valid_after.timestamp()),
            "nor_valid_before": Time.change_output_date_format_from_epoch(cert.not_valid_before.timestamp()),
            "issuer": cert.issuer.rfc4514_string(),
            "subject": cert.subject.rfc4514_string(),
            "signature": cert.signature.hex(),
            "signature_algorithm_hash": cert.signature_hash_algorithm.name,
            "signature_algorithm": cert.signature_algorithm_oid._name,
            "key_size": cert.public_key().key_size,
            "public_key": self._parse_dict_value(cert.public_key().public_numbers().__dict__)
        }

    def _parse_extensions(self, extensions: List[Extension]) -> list:
        parsed_extensions = []
        for extension in extensions:
            parsed_extensions.append(
                {extension.oid._name: {"critical": extension.critical,
                                       "values": self._parse_dict_value(extension.value.__dict__)}
                 })
        return parsed_extensions

    def _parse_dict_value(self, dict_values: dict) -> dict:
        values = {}
        for key in dict_values:
            # eliminamos la _ inicial
            values[key[1:]] = dict_values[key] if type(dict_values[key]) is not bytes \
                else dict_values[key].hex()
        return values

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if isinstance(target_file, TargetFile):
                if target_file.get_extension() == ".cer" or ".crt" or ".cer" or ".der":
                    return True
        return False

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        binary = target_file.get_binary()
        return self._get_info(binary)
