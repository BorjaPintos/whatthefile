from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.listoutput import ListOutput
from src.output.printoutput import PrintOutput
from src.output.fileoutput import FileOutput


class OutputFactory:

    @staticmethod
    def get_output(conf: WhatTheFileConfiguration):
        if "output" in conf.get_whatthefile_secction():
            output = conf.get_whatthefile_secction()["output"]
            if output == "print":
                return PrintOutput(conf)
            if output == "list":
                return ListOutput(conf)
            if output == "file":
                return FileOutput(conf)
        return PrintOutput(conf)
