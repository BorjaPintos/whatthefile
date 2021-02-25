from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.elasticsearchoutput import ElasticsearchOutput
from src.output.listoutput import ListOutput
from src.output.printoutput import PrintOutput
from src.output.fileoutput import FileOutput


class OutputFactory:

    @staticmethod
    def get_output_by_conf(conf: WhatTheFileConfiguration):
        if "output" in conf.get_whatthefile_secction():
            output = conf.get_whatthefile_secction()["output"]
            if output == "print":
                return OutputFactory._get_print_output(conf.get_section("output.print"))
            if output == "list":
                return OutputFactory._get_list_output(conf.get_section("output.list"))
            if output == "file":
                return OutputFactory._get_file_output(conf.get_section("output.file"))
            if output == "elasticsearch":
                return OutputFactory._get_elasticsearch_output(conf.get_section("output.elasticsearch"))
        return OutputFactory._get_print_output(conf.get_section("output.print"))

    @staticmethod
    def get_output_by_dict(params: dict):
        if "output" in params:
            output = params["output"]
            if output == "print":
                return OutputFactory._get_print_output(params)
            if output == "list":
                return OutputFactory._get_list_output(params)
            if output == "file":
                return OutputFactory._get_file_output(params)
            if output == "elasticsearch":
                return OutputFactory._get_elasticsearch_output(params)
        return OutputFactory._get_print_output(params)

    @staticmethod
    def _get_print_output(params: dict):
        return PrintOutput(params)

    @staticmethod
    def _get_list_output(params: dict):
        return ListOutput(params)

    @staticmethod
    def _get_file_output(params: dict):
        return FileOutput(params)

    @staticmethod
    def _get_elasticsearch_output(params: dict):
        return ElasticsearchOutput(params)