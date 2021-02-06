import configparser


class WhatTheFileConfiguration:

    def __init__(self):
        self._config = configparser.ConfigParser()

    def parse_file(self, file_paht) -> None:
        self._config.read(file_paht)

    def parse_string(self, string: str) -> None:
        self._config.read_string(string)

    def parse_dict(self, dictionary: dict) -> None:
        self._config.read_dict(dictionary)

    def get_property(self, section_name: str, property_name) -> str:
        return self._config.get(section_name, property_name)

    def get_property_boolean(self, section_name:str, property_name) -> bool:
        return self._config.getboolean(section_name, property_name)

    def get_property_float(self, section_name:str, property_name) -> float:
        return self._config.getfloat(section_name, property_name)

    def get_property_int(self, section_name : str, property_name) -> int:
        return self._config.getint(section_name, property_name)

    def get_property_list(self, section_name : str, property_name) -> list:
        return self._config.get(section_name, property_name).split(",")

    def get_section(self, section_name : str) ->dict:
        if section_name in self._config:
            return dict(self._config.items(section_name))
        return {}

    def get_whatthefile_secction(self):
        return dict(self._config.items("whatthefile"))

    def get_modules_section_names(self):
        modules_names = []
        for section in self._config.sections():
            if section.startswith("module."):
                modules_names.append(section)
        return modules_names

    def get_modules_names(self):
        modules_names = []
        for section in self._config.sections():
            if section.startswith("module."):
                modules_names.append(section.split("module.")[1])
        return modules_names
