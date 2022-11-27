# -*- coding: utf-8 -*-
import os
import traceback
from typing import List

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
import pypff

from src.output import utils
from src.utils.safe import Safe
from src.utils.time import Time
from src.utils.auxiliar import get_str_utf_8_from_bytes


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "exiftool"
        self._help = """Module to extract metadata"""
        self._author = "BorjaPintos"

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "Microsoft Outlook email" in target_file.get_type():
                return True
            if "Microsoft Outlook Personal Storage" in target_file.get_type():
                return True
        return False

    def _get_recursive(self, pypff_folder: pypff.folder, target_file:TargetFile) -> List:
        result = []
        for item in pypff_folder.sub_items:
            if isinstance(item, pypff.folder):
                n_messages = item.get_number_of_sub_messages()
                if n_messages > 0:
                    index = 0
                    while index < n_messages:
                        item_message = item.get_sub_message(index)
                        message = {}
                        try:
                            message["path"] = target_file.get_path()
                            message["email_folder"] = item.name
                            message["identifier"] = item_message.get_identifier()
                            message["subject"] = item_message.get_subject()
                            message["creation_time"] = Time.change_output_date_format_from_epoch(
                                item_message.get_creation_time().timestamp())
                            message["delivery_time"] = Time.change_output_date_format_from_epoch(
                                item_message.get_delivery_time().timestamp())
                            message["client_submit_time"] = Time.change_output_date_format_from_epoch(
                                item_message.get_client_submit_time().timestamp())
                            message["sender_name"] = item_message.get_sender_name()
                            message["headers"] = item_message.get_transport_headers()
                            message["html_body"] = get_str_utf_8_from_bytes(item_message.get_html_body()) \
                                if item_message.get_html_body() is not None else ""
                            message["plain_text_body"] = get_str_utf_8_from_bytes(item_message.get_plain_text_body()) \
                                if item_message.get_plain_text_body() is not None else ""
                            message["n_attachments"] = item_message.get_number_of_attachments()

                            if item_message.get_number_of_attachments() > 0:
                                message["attachments"] = []
                                for i in range(0, item_message.get_number_of_attachments()):
                                    base_path_to_save = message["email_folder"] + "/" + str(message[
                                        "identifier"]) + "/attachment/" + str(i)
                                    file_size =  item_message.get_attachment(i).get_size()
                                    binary = item_message.get_attachment(i).read_buffer(file_size)
                                    path_saved = Safe.create_file(
                                        os.path.join("./pstostparser", base_path_to_save), binary)
                                    message["attachments"].append(path_saved)
                        except:
                            pass
                        result.append(message)
                        index += 1

                result.extend(self._get_recursive(item, target_file))
        return result

    def _parse_pstost(self, target_file: TargetFile) -> List:
        pff_file = pypff.file()
        result = []
        try:
            pff_file.open(target_file.get_path())
            pff_root_folder = pff_file.get_root_folder()
            result = self._get_recursive(pff_root_folder, target_file)
        except:
            traceback.print_exc()
        finally:
            pff_file.close()
        return result

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        messages = self._parse_pstost(target_file)
        piped = utils.pipe_to_another_output(self._params, messages)
        return {"n_messages": len(messages)} if piped else {"messages": messages}
