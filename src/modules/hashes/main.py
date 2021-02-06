# -*- coding: utf-8 -*-
import hashlib
# import ssdeep
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule

HASHES = "hashes_to_calculate"


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "hashes"
        self._help = """Module to calculate hashes: 
		MD5, SHA1, SHA224, SHA156, SHA384, SHA512, SHA3_224, SHA3_256, SHA3_384, SHA3_512. The param "hashes_to_calculate, is a list of hashes, default is MD5 and SHA1"""
        self._author = "BorjaPintos"
        self._default_params = {HASHES: "MD5,SHA1"}

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

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            return True
        return False

    def _get_hashes_param(self, params: dict):
        if params is None:
            params = self._default_params
        if HASHES in params:
            return params[HASHES].split(",")
        else:
            return self._default_params[HASHES].split(",")

    def _unkonw_hash(self, target_file: TargetFile):
        return "Hash not suported"

    def run(self, target_file: TargetFile):
        hashes_dict = {}
        switcher = {
            'MD5': self._calculateMD5,
            'SHA1': self._calculateSHA1,
            'SHA224': self._calculateSHA224,
            'SHA256': self._calculateSHA256,
            'SHA384': self._calculateSHA384,
            'SHA512': self._calculateSHA512,
            'SHA3_224': self._calculateSHA3_224,
            'SHA3_256': self._calculateSHA3_256,
            'SHA3_384': self._calculateSHA3_384,
            'SHA3_512': self._calculateSHA3_512,
            # 'SSDEEP' : self._calculateSsdeep
        }
        for hash in self._get_hashes_param(self.get_params()):
            hashes_dict[hash] = switcher.get(hash, self._unkonw_hash)(target_file.get_binary())
        return hashes_dict
