# -*- coding: utf-8 -*-
import os
import traceback
from typing import List

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
import pypff

from src.output.outputfactory import OutputFactory
from src.utils import auxiliar
from src.utils.safe import Safe
from src.utils.time import Time


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

    def _get_recursirve(self, pypff_folder: pypff.folder) -> List:
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
                            message["folder"] = item.name
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
                            message["html_body"] = item_message.get_html_body().decode() \
                                if item_message.get_html_body() is not None else ""
                            message["plain_text_body"] = item_message.get_plain_text_body().decode() \
                                if item_message.get_plain_text_body() is not None else ""
                            message["n_attachments"] = item_message.get_number_of_attachments()

                            if item_message.get_number_of_attachments() > 0:
                                message["attachments"] = []
                                for i in range(0, item_message.get_number_of_attachments()):
                                    base_path_to_save = message["folder"] + "/" + str(message[
                                        "identifier"]) + "/attachment/" + str(i)
                                    file_size =  item_message.get_attachment(i).get_size()
                                    binary = item_message.get_attachment(i).read_buffer(file_size)
                                    path_saved = Safe.create_file(
                                        os.path.join("./pstostparser", base_path_to_save), binary)
                                    message["attachments"].append(path_saved)

                            result.append(message)
                        except:
                            pass
                        index += 1

                result.extend(self._get_recursirve(item))
        return result

    def _parse_pstost(self, target_file: TargetFile) -> List:
        pff_file = pypff.file()
        result = []
        try:
            pff_file.open(target_file.get_path())
            pff_root_folder = pff_file.get_root_folder()
            result = self._get_recursirve(pff_root_folder)
        except:
            traceback.print_exc()
        finally:
            pff_file.close()
        return result

    def _pipe_to_another_output(self, messages: list):
        if "needs_pipe" in self.get_params() \
                and auxiliar.convert_to_boolean(self.get_params()["needs_pipe"]) \
                and "output" in self.get_params():
            pipe = OutputFactory.get_output_by_dict(self.get_params())
            pipe.dump_list(messages)

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        messages = self._parse_pstost(target_file)
        self._pipe_to_another_output(messages)
        return {"messages": messages}
