# -*- coding: utf-8 -*-
import traceback
from threading import Thread, current_thread

from src.domain.ignoreanalysisexception import IgnoreAnalysisException
from src.domain.loadermodules import LoaderModules
from src.domain.targetdirectory import TargetDirectory
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
import os
from src.output.ioutput import IOutput
from datetime import datetime

from src.utils.log import Log
from src.utils.queue import Queue
from src.utils.safe import Safe
from src.utils.time import Time


class Core:

    def __init__(self, config: WhatTheFileConfiguration, output: IOutput):
        self._config = config
        Log.configure(config)
        Time.configure(config)
        Safe.configure(config)
        self._modules = LoaderModules(config).get_modules()
        self._output = output
        self._queue = Queue()
        self._n_threads_running = 0

    def _run_threads(self):
        try:
            n_threads = self._config.get_property_int("whatthefile", "n_threads")
        except :
            n_threads = 1
        Log.debug("n_threads:" + str(n_threads))
        threads = []
        for i in range(self._n_threads_running, n_threads):
            Log.debug("creando thread:")
            thread = Thread(target=self._run, daemon=False)
            Log.debug("creado thread:" + thread.getName())
            threads.append(thread)
            thread.start()
            self._n_threads_running = self._n_threads_running + 1
        return threads

    def run(self, input: str):
        # comprobamos el directorio de extracción para saber si cambia
        safe_output_path = Safe.safe_output_path
        mtime = os.stat(safe_output_path).st_mtime
        n_elements_inside = len(os.listdir(safe_output_path))
        self._queue.put(input)
        Log.debug(str(id) + " - Añadido elemento a la cola:" + input)
        threads = self._run_threads()
        Log.debug("- Esperando threads...")
        self._queue.join()
        Log.debug("- Cola terminada...")
        self._queue.unblock_gets()
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

    def _run(self):
        id = current_thread().getName()
        Log.debug("I AM: " + str(id))

        while True:
            Log.debug(str(id) + " - Vamos a coger un elemento")
            input = self._queue.get()
            if input is None:
                break

            Log.debug(str(id) + " - Elemento obtenido: " + str(input))
            try:
                if os.path.exists(input):
                    begin_analysis = self.get_utc_timestamp()
                    analysis = {}
                    if os.path.isfile(input):
                        analysis = self._analyze_file(input)
                    elif os.path.isdir(input):
                        analysis = self._analyze_dir(input)
                        for element in os.listdir(input):
                            Log.debug(str(id) + " - Añadido elemento a la cola:" + os.path.join(input, element))
                            self._queue.put(os.path.join(input, element))
                    else:
                        target_path = TargetPath(input)
                        analysis = target_path.get_info()

                    end_analysis = self.get_utc_timestamp()
                    analysis["begin_analysis"] = Time.change_output_date_format_from_epoch(begin_analysis)
                    analysis["end_analysis"] = Time.change_output_date_format_from_epoch(end_analysis)
                    analysis["total_analysis_duration"] = end_analysis - begin_analysis
                    self._output.dump_object(analysis)
            except IgnoreAnalysisException:
                "ignore and get next targetpath"
                pass
            except Exception:
                traceback.print_exc()
                Log.error("error en path:" + input)
            finally:
                self._queue.task_done()
        self._n_threads_running = self._n_threads_running - 1
        Log.debug(str(id) + "- DONE")

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

    def _run_modules(self, target: TargetPath):
        result = {}
        for module in self._modules:
            if module.get_mod().is_valid_for(target):
                start_module = self.get_utc_timestamp()
                try:
                    result[module.get_name()] = {}
                    result[module.get_name()] = module.get_mod().run(target, result)
                except IgnoreAnalysisException:
                    raise IgnoreAnalysisException()
                except Exception as e:
                    result[module.get_name()]["error"] = str(e)
                end_module = self.get_utc_timestamp()
                result[module.get_name()]["start_module"] = Time.change_output_date_format_from_epoch(start_module)
                result[module.get_name()]["end_module"] = Time.change_output_date_format_from_epoch(end_module)
                result[module.get_name()]["total_module_duration"] = end_module - start_module
        return result

    def get_utc_timestamp(self) -> float:
        return datetime.utcnow().timestamp()
