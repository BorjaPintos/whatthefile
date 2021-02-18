import sys

from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from loguru import logger


class Log:

    @staticmethod
    def configure(conf: WhatTheFileConfiguration):
        output = conf.get_property("whatthefile", "log_output")

        switcher = {
            "stdout": sys.stdout,
            "stderr": sys.stderr,
            "file": conf.get_section("log_output.file")["filename"] + str("_{time}.log")
            if "filename" in conf.get_section("log_output.file") else sys.stderr
        }
        logger.remove()
        logger.add(switcher.get(output, sys.stderr),
                   format="{time} {level} {message}")

    @staticmethod
    def debug(message: str):
        logger.debug(message)

    @staticmethod
    def log(message: str):
        logger.log(message)

    @staticmethod
    def info(message: str):
        logger.info(message)

    @staticmethod
    def error(message: str):
        logger.error(message)

    @staticmethod
    def critical(message: str):
        logger.critical(message)
