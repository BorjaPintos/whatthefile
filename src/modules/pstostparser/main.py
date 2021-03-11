# -*- coding: utf-8 -*-
import traceback

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
import pypff


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "exiftool"
        self._help = """Module to extract metadata"""
        self._author = "BorjaPintos"

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file() and "Microsoft Outlook email" in target_file.get_type():
            return True
        return False

    def _get_recursirve(self, pypff_folder: pypff.folder) -> dict:
        result = {}
        for item in pypff_folder.sub_items:
            if isinstance(item, pypff.folder):
                n_messages = item.get_number_of_sub_messages()
                if n_messages > 0:
                    result[item.name] = []
                    index = 0
                    while index < n_messages:
                        item_message = item.get_sub_message(index)
                        message = {}
                        try:
                            message["identifier"] = item_message.get_identifier()
                            message["subject"] = item_message.get_subject()
                            message["sender_name"] = item_message.get_sender_name()
                            message["headers"] = item_message.get_transport_headers()
                            message["html_body"] = item_message.get_html_body().decode() \
                                if item_message.get_html_body() is not None else ""
                            message["plain_text_body"] = item_message.get_plain_text_body().decode() \
                                if item_message.get_plain_text_body() is not None else ""
                            message["n_attachments"] = item_message.get_number_of_attachments()
                            """
                            if item_message.get_number_of_attachments() > 0:
                                "En esta librería no está implementado la extracción de adjuntos"
                            """
                            result[item.name].append(message)
                        except:
                            pass
                        index += 1

                result.update(self._get_recursirve(item))
        return result

    def _parse_pstost(self, target_file: TargetFile) -> dict:
        pff_file = pypff.file()
        result = {}
        try:
            pff_file.open(target_file.get_path())
            pff_root_folder = pff_file.get_root_folder()
            result = self._get_recursirve(pff_root_folder)
        except:
            traceback.print_exc()
        finally:
            pff_file.close()
        return result

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        return {"folders": self._parse_pstost(target_file)}
