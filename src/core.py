# -*- coding: utf-8 -*-
from typing import List

from src.domain.loadermodules import LoaderModules
from src.domain.targetdirectory import TargetDirectory
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
import os
from src.output.ioutput import IOutput
from datetime import datetime


class Core:

    def __init__(self, config: WhatTheFileConfiguration, output: IOutput):
        self._config = config
        self._modules = LoaderModules(config).get_modules()
        self._output = output

    def run(self, input: str):
        if os.path.exists(input):
            if os.path.isfile(input):
                self._output.dump(self._analyze_file(input))
            elif os.path.isdir(input):
                self._output.dump(self._analyze_dir(input))
                for element in os.listdir(input):
                    self.run(os.path.join(input, element))
            else:
                target_path = TargetPath(input)
                self._output.dump(target_path.get_info())

    def _analyze_dir(self, dir_path: str) -> dict:
        begin_analysis = self.get_utc_timestamp()
        target_directory = TargetDirectory(dir_path)
        result = target_directory.get_info()

        for module in self._modules:
            if module.get_mod().is_valid_for(target_directory):
                start_module = self.get_utc_timestamp()
                result[module.get_name()] = module.get_mod().run(target_directory)
                result[module.get_name()]["start_module"] = start_module
                result[module.get_name()]["end_module"] = self.get_utc_timestamp()
        result["begin_analysis"] = begin_analysis
        result["end_analysis"] = self.get_utc_timestamp()
        return result

    def _analyze_file(self, file_path: str) -> dict:
        begin_analysis = self.get_utc_timestamp()
        target_file = TargetFile(file_path)
        result = target_file.get_info()
        for module in self._modules:
            if module.get_mod().is_valid_for(target_file):
                start_module = self.get_utc_timestamp()
                result[module.get_name()] = module.get_mod().run(target_file)
                result[module.get_name()]["start_module"] = start_module
                result[module.get_name()]["end_module"] = self.get_utc_timestamp()
        result["begin_analysis"] = begin_analysis
        result["end_analysis"] = self.get_utc_timestamp()
        return result

    def get_utc_timestamp(self) -> float:
        return datetime.utcnow().timestamp()
