# -*- coding: utf-8 -*-
import os
from abc import abstractmethod

from src.utils.time import Time


class TargetPath:

    def __init__(self, path: str):
        self._path = path
        self._directory = os.path.dirname(self._path)
        self._name = os.path.basename(self._path)
        self._type = None
        self._is_file = os.path.isfile(self._path)
        self._is_directory = os.path.isdir(self._path)
        self._is_link = os.path.islink(self._path)

    def get_path(self) ->str:
        return self._path

    def get_directory(self) -> str:
        return self._directory

    def get_name(self) -> str:
        return self._name

    def get_type(self) -> str:
        return self._type

    def is_file(self) -> bool:
        return self._is_file

    def is_directory(self) -> bool:
        return self._is_directory

    def is_link(self) -> bool:
        return self._is_link

    def get_info(self) -> dict:
        result = {}
        result["path"] = self._path
        result["directory"] = self._directory
        result["name"] = self._name
        result["is_file"] = self._is_file
        result["is_directory"] = self._is_directory
        result["is_link"] = self._is_link
        result["type"] = self._type
        result.update(self.get_stat_info())
        result.update(self._get_other_info())
        return result


    def get_stat_info(self):
        stat = os.stat(self._path)
        result = {}
        result["st_atime"] = Time.change_output_date_format_from_epoch(stat.st_atime)
        result["st_ctime"] = Time.change_output_date_format_from_epoch(stat.st_ctime)
        result["st_mtime"] = Time.change_output_date_format_from_epoch(stat.st_mtime)
        result["st_blksize"] = stat.st_blksize
        result["st_blocks"] = stat.st_blocks
        result["st_gid"] = stat.st_gid
        result["st_uid"] = stat.st_uid
        result["st_size"] = stat.st_size
        result["st_mode"] = stat.st_mode
        result["st_device"] = stat.st_dev
        try:
            #it depends on SO
            result["st_birthtime"] = stat.st_birthtime
        except:
            pass
        try:
            #it depends on SO
            result["st_flags"] = stat.st_flags
        except:
            pass
        return result

    @abstractmethod
    def _get_other_info(self):
        return {}
