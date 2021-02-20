# -*- coding: utf-8 -*-
import unittest

import pytest

from src.domain.ignoreanalysisexception import IgnoreAnalysisException
from src.domain.targetfile import TargetFile
from src.modules.ignore.main import Constructor


class IgnoreTest(unittest.TestCase):
    # ignore_greater_or_equal_than = 6000000000
    # ignore_less_or_equal_than = 6

    def test_not_ignore(self):
        path = "./tests/examples/barcode.png"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params({"file_hashes_md5_to_ignore": "./tests/examples/ignoredhashesmd5.txt",
                           "file_hashes_sha1_to_ignore": "./tests/examples/ignoredhashessha1.txt",
                           "file_extensions_to_ignore": "./tests/examples/ignoredextensions.txt",
                           "ignore_greater_or_equal_than": 6000000,
                           "ignore_less_or_equal_than": 6})

        result = module.run(target_file, {'hashes': {"MD5": "aaaaa", "SHA1": "bbbbbb"}})
        self.assertFalse(result["ignored"])

    def test_ignore_hashMD5(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params({"file_hashes_md5_to_ignore": "./tests/examples/ignoredhashesmd5.txt"})
        with pytest.raises(IgnoreAnalysisException):
            module.run(target_file, {'hashes': self._get_collie_hashes()})

    def test_ignore_hashSHA1(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params({"file_hashes_sha1_to_ignore": "./tests/examples/ignoredhashessha1.txt"})
        with pytest.raises(IgnoreAnalysisException):
            module.run(target_file, {'hashes': self._get_collie_hashes()})

    def test_ignore_extension(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params({"file_extensions_to_ignore": "./tests/examples/ignoredextensions.txt"})
        with pytest.raises(IgnoreAnalysisException):
            module.run(target_file, {'hashes': self._get_collie_hashes()})

    def test_ignore_path(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params({"file_ignore_path": "./tests/examples/ignoredpaths.txt"})
        with pytest.raises(IgnoreAnalysisException):
            module.run(target_file, {'hashes': self._get_collie_hashes()})

    def test_ignore_path2(self):
        path = "tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params({"file_ignore_path": "./tests/examples/ignoredpaths.txt"})
        with pytest.raises(IgnoreAnalysisException):
            module.run(target_file, {'hashes': self._get_collie_hashes()})

    def test_ignore_max_size(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params({"ignore_greater_or_equal_than": 19863})
        with pytest.raises(IgnoreAnalysisException):
            module.run(target_file, {'hashes': self._get_collie_hashes()})

    def test_ignore_min_size(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params({"ignore_less_or_equal_than": 19863})
        with pytest.raises(IgnoreAnalysisException):
            module.run(target_file, {'hashes': self._get_collie_hashes()})

    def _get_collie_hashes(self):
        return {"MD5": "9e30d001ac1e7e2a7c959be45e8e5bda",
                "SHA1": "85fbeea5f3ed2709867eefb9ab68859416c0bdf9"}
