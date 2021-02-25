# -*- coding: utf-8 -*-
import traceback
from collections import OrderedDict
from typing import List
import xmltodict
from evtx import PyEvtxParser
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
import datetime

from src.output.elasticsearchoutput import ElasticsearchOutput
from src.output.outputfactory import OutputFactory
from src.utils import aux
from src.utils.time import Time


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "evtxreader"
        self._help = """Extract events from .evtx files"""
        self._author = "BorjaPintos"

    def is_valid_for(self, target_file: TargetPath):
        if "Event Log" in target_file.get_type() and \
                target_file.is_file() and \
                isinstance(target_file, TargetFile) and \
                target_file.get_extension() == ".evtx":
            return True
        return False

    def _extract_info_in_data_parsed(self, data: List, properties: List[str]) -> dict:
        info = {}
        for element in data["Data"]:
            if element["@Name"] in properties:
                info[element["@Name"]] = element["#text"]
        return info

    def _get_system_info(self, parsed):
        event_id = parsed["Event"]["System"]["EventID"]
        if isinstance(event_id, OrderedDict):
            id = int(event_id["#text"])
        else:
            id = int(event_id)
        timestamp = parsed["Event"]["System"]["TimeCreated"]["@SystemTime"]
        try:
            timestamp_parsed = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f UTC')
        except:
            try:
                timestamp_parsed = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S UTC')
            except:
                return {"error": "invalid timestamp:" + timestamp}
        return {
            "EventID": id,
            "EventRecordID": parsed["Event"]["System"]["EventRecordID"],
            "Timestamp": Time.change_output_date_format_from_epoch(timestamp_parsed.timestamp()),
            "Level": parsed["Event"]["System"]["Level"],
            "Channel": parsed["Event"]["System"]["Channel"],
            "Computer": parsed["Event"]["System"]["Computer"],
        }

    def _get_loggin_info(self, parsed: dict) -> dict:
        info = self._get_system_info(parsed)
        info.update(self._extract_info_in_data_parsed(parsed["Event"]["EventData"],
                                                      ["TargetUserName", "TargetUserSid", "TargetDomainName",
                                                       "TargetLogonId", "LogonType"]))
        info["Type"] = "login"

        return info

    def _get_logout_info(self, parsed):
        info = self._get_system_info(parsed)
        info.update(self._extract_info_in_data_parsed(parsed["Event"]["EventData"],
                                                      ["TargetUserName", "TargetUserSid", "TargetDomainName",
                                                       "TargetLogonId", "LogonType"]))
        info["Type"] = "logout"

        return info

    def _get_start_info(self, parsed):
        info = self._get_system_info(parsed)
        info["Type"] = "start_system"
        return info

    def _get_info_interesting(self, parsed):
        event_id = parsed["Event"]["System"]["EventID"]
        if isinstance(event_id, OrderedDict):
            id = int(event_id["#text"])
        else:
            id = int(event_id)
        swither = {
            4624: self._get_loggin_info,
            4647: self._get_logout_info,
            6005: self._get_start_info
        }
        function = swither.get(id, None)
        return function(parsed) if function is not None else None

    def _pipe_to_another_output(self, events: list):
        if "needs_pipe" in self.get_params() \
                and aux.convert_to_boolean(self.get_params()["needs_pipe"]) \
                and "output" in self.get_params():
            pipe = OutputFactory.get_output_by_dict(self.get_params())
            pipe.dump_list(events)


    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        events = []
        parser = PyEvtxParser(target_file.get_path())
        for record in parser.records():
            try:
                parsed = xmltodict.parse(record["data"])
                event = self._get_info_interesting(parsed)
                if event is not None:
                    events.append(event)
            except:
                pass
        self._pipe_to_another_output(events)
        return {"events": events}
