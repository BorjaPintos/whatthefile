# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import List
import xmltodict
from evtx import PyEvtxParser
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
import datetime

from src.output import utils
from src.utils.time import Time


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "evtxreader"
        self._help = """Extract events from .evtx files"""
        self._author = "BorjaPintos"
        self._filter_ids = []

    def is_valid_for(self, target_file: TargetPath):
        if "Event Log" in target_file.get_type() and \
                target_file.is_file() and \
                isinstance(target_file, TargetFile) and \
                target_file.get_extension() == ".evtx":
            return True
        return False

    def _get_filter_ids_from_params(self):
        str_list_ids = self.get_params().get("filter_ids", '').split(",")
        returned_list = []
        for id in str_list_ids:
            if id:
                try:
                    returned_list.append(int(id))
                except:
                    pass
        return returned_list

    def _extract_info_in_data_parsed(self, data: List) -> dict:
        info = {}
        for element in data["Data"]:
            if "#text" in element:
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

    def _get_info(self, parsed, target_file: TargetFile):
        event_id = parsed["Event"]["System"]["EventID"]
        if isinstance(event_id, OrderedDict):
            id = int(event_id["#text"])
        else:
            id = int(event_id)

        if self._filter_ids:
            if id not in self._filter_ids:
                return None

        info = self._get_system_info(parsed)
        info.update(self._extract_info_in_data_parsed(parsed["Event"]["EventData"]))
        info["path"] = target_file.get_path()
        return info

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        events = []
        self._filter_ids = self._get_filter_ids_from_params()
        parser = PyEvtxParser(target_file.get_path())
        for record in parser.records():
            try:
                parsed = xmltodict.parse(record["data"])
                event = self._get_info(parsed, target_file)
                if event is not None:
                    events.append(event)
            except:
                pass
        piped = utils.pipe_to_another_output(self._params, events)
        return {"n_events": len(events)} if piped else {"events": events}
