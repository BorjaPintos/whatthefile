# -*- coding: utf-8 -*-
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
from PIL import Image
from pyzbar.pyzbar import decode


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "qrbcreader"
        self._help = """Module to read QR and Barcodes in jpg and png images"""
        self._author = "BorjaPintos"

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "JPEG image data" in target_file.get_type():
                return True
            elif "PNG image data" in target_file.get_type():
                return True
            elif "GIF image data" in target_file.get_type():
                return True
        return False

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        decoded_list = decode(Image.open(target_file.get_path()))
        i = 0
        result = {}
        for dec in decoded_list:
            result[str(i)] = dec.data.decode("utf-8")
            i += 1
        return result
