# -*- coding: utf-8 -*-
import unittest
from src.domain.targetfile import TargetFile
from src.modules.mftparser.main import Constructor


class MFTParserTest(unittest.TestCase):

    def test_parser_mft(self):
        path = "./tests/examples/MFT"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertEqual(len(result["mft"]), 13068)


    def test_invalid_file(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
