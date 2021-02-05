# -*- coding: utf-8 -*-
import math

from src.domain.targetfile import TargetFile
from src.modules.imodule import IModule


class Constructor(IModule):

    def __init__(self):
        self._name = "entropy"
        self._help = """Module to calculate Shannon entropy"""
        self._author = "BorjaPintos"
        self._params = None

    def _shannon_entropy(self, binary):
        file_size = len(binary)

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

    def is_valid_for(self, target_file: TargetFile):
        return True

    def run(self, target_file: TargetFile, params: dict = None):
        return {"shannon": self._shannon_entropy(target_file.get_binary())}
