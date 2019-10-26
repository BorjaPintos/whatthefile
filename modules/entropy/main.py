# -*- coding: utf-8 -*-
import math
from modules.imodule import IModule

class Constructor(IModule):

    def __init__(self):
        self._name = "entropy"
        self._help = """Module to calculate Shannon entropy"""
        self._author = "BorjaPintos"
        self._params = []

    def _entropy(self, binary):
        fileSize = len(binary)
    
        # calculate the frequency of each byte value in the file
        freqList = []
        for b in range(256):
            ctr = 0
            for byte in binary:
                if byte == b:
                    ctr += 1
            freqList.append(float(ctr) / fileSize)
    
        # Shannon entropy
        ent = 0.0
        for freq in freqList:
            if freq > 0:
                ent = ent + freq * math.log(freq, 2)
        ent = -ent
        return ent

    def validFor(self, targetFile):
        return True

    def generateReport(self, targetFile, params):
        return self._entropy(targetFile.getBinary())
