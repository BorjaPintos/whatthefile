# -*- coding: utf-8 -*-
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
from src.modules.virustotal import virustotalapiv2 as virustotalapi

APIKEY = "apikey"


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "virustotal"
        self._help = """Module to analyze file using virus total, only the hash will be sumitted. 
		The param {'""" + APIKEY + """': '...'} is required"""
        self._author = "BorjaPintos"

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            return True
        return False

    def run(self, target_file: TargetFile):
        if target_file.get_extension() in ["", ".sh", ".py", ".rb", ".java", ".class",
                                           ".pl", ".exe", ".out", ".ps", ".bat", ".air",
                                           ".scr", ".vb", ".com", ".dll", ".bin", ".apk",
                                           ".app", ".cgi", ".cmd", ".wsf", ".ipa", ".pif",
                                           ".gadget", ".docm", ".dotm", ".xlsm", ".xltm",
                                           ".pptm", "potm"]:
            return {"skipped:", "extension not interesting to analyse"}

        if self.get_params() is None or APIKEY not in self.get_params():
            return {"error": APIKEY + " is required"}
        virus_total_report = virustotalapi.check_hash(self.get_params()[APIKEY],
                                                      virustotalapi.get_MD5_hash(target_file.get_binary()))
        if "error" in virus_total_report:
            return virus_total_report
        result = {'positives': 0}
        if virus_total_report['response_code'] == 1:
            result['positives'] = virus_total_report['positives']
            result['total'] = virus_total_report['total']
            avDetections = {}
            for av_name, av_data in virus_total_report['scans'].items():
                if av_data['result'] is None:
                    avDetections[av_name] = "None"
                else:
                    avDetections[av_name] = av_data['result']
            result['avDetections'] = avDetections
        return result
