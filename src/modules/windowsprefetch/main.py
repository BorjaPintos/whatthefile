# -*- coding: utf-8 -*-
from datetime import timezone

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
import pyscca

from src.utils.time import Time


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "windowsprefetch"
        self._help = """Module to parse windows prefetch files"""
        self._author = "BorjaPintos"

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file() \
                and isinstance(target_file, TargetFile) \
                and target_file.get_extension() == ".pf":
            return True
        return False

    def _parse_prefecth_file(self, path: str):
        scca = pyscca.open(path)
        all_strings = []
        for entry_index, file_metrics in enumerate(scca.file_metrics_entries):
            all_strings.append(file_metrics.filename)

        last_run_times = []
        for exe_timestamp in range(scca.run_count):
            try:
                if scca.get_last_run_time_as_integer(exe_timestamp) > 0:
                    time = Time.change_output_date_format_from_epoch(
                        scca.get_last_run_time(exe_timestamp).replace(tzinfo=timezone.utc).timestamp())
                    last_run_times.append(time)
            except OSError:
                # No hay mas fechas de ejecucion guardadas
                break

        volume_serial_number = []
        volume_device_path = []
        volume_timestamp = []
        for volume_information in iter(scca.volumes):
            volume_serial_number.append(format(volume_information.serial_number, 'x').upper())
            volume_device_path.append(str(volume_information.device_path))
            volume_timestamp.append(Time.change_output_date_format_from_epoch(
                volume_information.creation_time.replace(tzinfo=timezone.utc).timestamp()))

        return {
            "version": scca.format_version,
            "executable_file_name": str(scca.executable_filename),
            "hash": format(scca.prefetch_hash, 'x').upper(),
            "number_of_files_accessed": scca.number_of_file_metrics_entries,
            "directories_accessed": all_strings,
            "number_of_volumes": scca.number_of_volumes,
            "run_counts": scca.run_count,
            "last_run_times": last_run_times,
            "volume_timestamp": volume_timestamp,
            "volume_device_path": volume_device_path,
            "volume_serial_number": volume_serial_number
        }

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        result = self._parse_prefecth_file(target_file.get_path())
        return result
