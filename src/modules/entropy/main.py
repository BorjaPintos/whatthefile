# -*- coding: utf-8 -*-
import math

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "entropy"
        self._help = """Module to calculate Shannon entropy"""
        self._author = "BorjaPintos"
        
    def _shannon_entropy(self, binary):
        file_size = len(binary)
        if file_size == 0:
            return 0

        # calculate the frequency of each byte value in the file
        freq_list = []
        for b in range(256):
            ctr = 0
            for byte in binary:
                if byte == b:
                    ctr += 1
            freq_list.append(float(ctr) / file_size)

        # Shannon entropy
        ent = 0.0
        for freq in freq_list:
            if freq > 0:
                ent = ent + freq * math.log(freq, 2)
        ent = -ent
        return ent

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            return True
        return False

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        return {"shannon": self._shannon_entropy(target_file.get_binary())}
