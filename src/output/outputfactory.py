from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.listoutput import ListOutput
from src.output.printoutput import PrintOutput


class OutputFactory:

    @staticmethod
    def get_output(conf: WhatTheFileConfiguration):
            if "output" in conf.get_whatthefile_secction():
                output = conf.get_whatthefile_secction()["output"]
                if output == "print":
                    return PrintOutput()
                if output == "list":
                    return ListOutput()
            return PrintOutput()