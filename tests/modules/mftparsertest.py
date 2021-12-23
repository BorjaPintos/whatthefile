# -*- coding: utf-8 -*-
import unittest
from src.domain.targetfile import TargetFile
from src.modules.mftparser.main import Constructor
from src.output.listoutput import ListOutput
from src.output.outputfactory import OutputFactory


class MFTParserTest(unittest.TestCase):

    def test_parser_mft(self):
        path = "./tests/examples/MFT"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertEqual(len(result["mft"]), 13068)


    def test_parse_mft_with_second_output(self):
        path = "./tests/examples/MFT"
        target_file = TargetFile(path)
        module = Constructor()
        module.set_params({"needs_pipe": True, "output": "list"})
        my_lyst_output = ListOutput()
        backup_function = OutputFactory._get_list_output
        OutputFactory._get_list_output = lambda params : my_lyst_output
        result = module.run(target_file, {})
        OutputFactory._get_list_output = backup_function
        self.assertTrue(result["n_mft_objects"] != 0)
        self.assertTrue(len(my_lyst_output.get_list()), result["n_mft_objects"])

    def test_invalid_file(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
