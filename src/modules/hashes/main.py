# -*- coding: utf-8 -*-
import hashlib
#import ssdeep
from src.domain.targetfile import TargetFile
from src.modules.imodule import IModule

class Constructor(IModule):

    def __init__(self):
        self._name = "hashes"
        self._help = """Module to calculate hashes: 
		MD5, SHA1, SHA224, SHA156, SHA384, SHA512, SHA3_224, SHA3_256, SHA3_384, SHA3_512."""
        self._author = "BorjaPintos"
        self._params = None

    def _calculateMD5(self, binary):
        hasher = hashlib.md5()
        hasher.update(binary)
        md5 = hasher.hexdigest()
        return md5

    def _calculateSHA1(self, binary):
        hasher = hashlib.sha1()
        hasher.update(binary)
        sha1 = hasher.hexdigest()
        return sha1

    def _calculateSHA224(self, binary):
        hasher = hashlib.sha224()
        hasher.update(binary)
        sha224 = hasher.hexdigest()
        return sha224

    def _calculateSHA256(self, binary):
        hasher = hashlib.sha256()
        hasher.update(binary)
        sha256 = hasher.hexdigest()
        return sha256

    def _calculateSHA384(self, binary):
        hasher = hashlib.sha384()
        hasher.update(binary)
        sha384 = hasher.hexdigest()
        return sha384

    def _calculateSHA512(self, binary):
        hasher = hashlib.sha512()
        hasher.update(binary)
        sha512 = hasher.hexdigest()
        return sha512

    def _calculateSHA3_224(self, binary):
        hasher = hashlib.sha3_224()
        hasher.update(binary)
        hash = hasher.hexdigest()
        return hash

    def _calculateSHA3_256(self, binary):
        hasher = hashlib.sha3_256()
        hasher.update(binary)
        hash = hasher.hexdigest()
        return hash

    def _calculateSHA3_384(self, binary):
        hasher = hashlib.sha3_384()
        hasher.update(binary)
        hash = hasher.hexdigest()
        return hash

    def _calculateSHA3_512(self, binary):
        hasher = hashlib.sha3_512()
        hasher.update(binary)
        hash = hasher.hexdigest()
        return hash
    """
    Parece ser que de momento esto solo funciona para linux, tengo que hacer más pruebas para ver como lo instalo en mac
    def _calculateSsdeep(self, binary):
        return ssdeep.hash(binary)
    """

    def is_valid_for(self, target_file: TargetFile):
        return True

    def run(self, target_file: TargetFile, params: dict = None):
        hashes_dict = {}
        hashes_dict['MD5'] = self._calculateMD5(target_file.get_binary())
        hashes_dict['SHA1'] = self._calculateSHA1(target_file.get_binary())
        hashes_dict['SHA224'] = self._calculateSHA224(target_file.get_binary())
        hashes_dict['SHA256'] = self._calculateSHA256(target_file.get_binary())
        hashes_dict['SHA384'] = self._calculateSHA384(target_file.get_binary())
        hashes_dict['SHA512'] = self._calculateSHA512(target_file.get_binary())
        hashes_dict['SHA3_224'] = self._calculateSHA3_224(target_file.get_binary())
        hashes_dict['SHA3_256'] = self._calculateSHA3_256(target_file.get_binary())
        hashes_dict['SHA3_384'] = self._calculateSHA3_384(target_file.get_binary())
        hashes_dict['SHA3_512'] = self._calculateSHA3_512(target_file.get_binary())
        #hashesDict['SSDEEP'] = self._calculateSsdeep(target_file.get_binary())
        return hashes_dict