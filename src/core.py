# -*- coding: utf-8 -*-
import traceback

from src.domain.loadermodules import LoaderModules
from src.domain.targetdirectory import TargetDirectory
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
import os
from src.output.ioutput import IOutput
from datetime import datetime

from src.utils.safe import Safe
from src.utils.time import Time


class Core:

    def __init__(self, config: WhatTheFileConfiguration, output: IOutput):
        self._config = config
        Time.configure(config)
        Safe.configure(config)
        self._modules = LoaderModules(config).get_modules()
        self._output = output

    def run(self, input: str):
        #comprobamos el directorio de extracción para saber si cambia
        safe_output_path = Safe.safe_output_path
        mtime = os.stat(safe_output_path).st_mtime
        n_elements_inside = len(os.listdir(safe_output_path))
        self._run(input)
        #tanalizamos directorio de extracción también
        mtime2 = os.stat(safe_output_path).st_mtime
        n_elements_inside2 = len(os.listdir(safe_output_path))
        if mtime2 != mtime or n_elements_inside2 != n_elements_inside:
            Safe.next_rotation()
            self.run(safe_output_path)
        else:
            try:
                os.rmdir(Safe.safe_output_path)
            except:
                "tampoco es una obligación borrarlo sino se puede"
                pass

    def _run(self, input:str):
        try:
            if os.path.exists(input):
                begin_analysis = self.get_utc_timestamp()
                analysis = {}
                if os.path.isfile(input):
                    analysis = self._analyze_file(input)
                elif os.path.isdir(input):
                    analysis = self._analyze_dir(input)
                    for element in os.listdir(input):
                        self._run(os.path.join(input, element))
                else:
                    target_path = TargetPath(input)
                    analysis = target_path.get_info()

                end_analysis = self.get_utc_timestamp()
                analysis["begin_analysis"] = Time.change_output_date_format_from_epoch(begin_analysis)
                analysis["end_analysis"] = Time.change_output_date_format_from_epoch(end_analysis)
                analysis["total_analysis_duration"] = end_analysis - begin_analysis
                self._output.dump(analysis)
        except:
            traceback.print_exc()
            print("error en path:" + input)
            
            
    def clean_safe_output_path(self):
        Safe.reset(self._config)

    def _analyze_dir(self, dir_path: str) -> dict:

        target_directory = TargetDirectory(dir_path)
        result = target_directory.get_info()
        result.update(self._run_modules(target_directory))
        return result

    def _analyze_file(self, file_path: str) -> dict:
        target_file = TargetFile(file_path)
        result = target_file.get_info()
        result.update(self._run_modules(target_file))
        return result


    def _run_modules(self, target : TargetPath):
        result = {}
        for module in self._modules:
            if module.get_mod().is_valid_for(target):
                start_module = self.get_utc_timestamp()
                try:
                    result[module.get_name()] = {}
                    result[module.get_name()] = module.get_mod().run(target)
                except Exception as e:
                    result[module.get_name()]["error"] = str(e)
                end_module = self.get_utc_timestamp()
                result[module.get_name()]["start_module"] = Time.change_output_date_format_from_epoch(start_module)
                result[module.get_name()]["end_module"] = Time.change_output_date_format_from_epoch(end_module)
                result[module.get_name()]["total_module_duration"] = end_module - start_module
        return result


    def get_utc_timestamp(self) -> float:
        return datetime.utcnow().timestamp()
