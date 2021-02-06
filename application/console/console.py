# -*- coding: utf-8 -*-
import sys

from src.core import Core
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.outputfactory import OutputFactory


class Console:

    def __init__(self):
        """Init."""

    def run(self, arguments):
        if len(arguments) != 3:
            Console.print_help(arguments)
            sys.exit()
        else:
            conf = WhatTheFileConfiguration()
            conf.parse_file(arguments[1])
            output = OutputFactory.get_output(conf)
            core = Core(conf, output)
            core.run(arguments[2])


    @staticmethod
    def print_help(arguments):
        print("Usage: " + arguments[0] + " <path-to-whatthefile.ini>" " <path-to-analyze>")

