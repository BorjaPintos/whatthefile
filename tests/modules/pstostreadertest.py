import os
import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.pstostparser.main import Constructor
from src.output.listoutput import ListOutput
from src.output.outputfactory import OutputFactory


class PSTOSTReaderTest(unittest.TestCase):

    def test_ost(self):
        path = "./tests/examples/nromanoff@stark-research-labs.com.pst"
        target_file = TargetFile(os.path.abspath(path))
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue('messages' in result)
        self.assertEqual(len(result["messages"]), 532)

    def test_parse_mft_with_second_output(self):
        path = "./tests/examples/nromanoff@stark-research-labs.com.pst"
        target_file = TargetFile(path)
        module = Constructor()
        module.set_params({"needs_pipe": True, "output": "list"})
        my_lyst_output = ListOutput()
        backup_function = OutputFactory._get_list_output
        OutputFactory._get_list_output = lambda params : my_lyst_output
        result = module.run(target_file, {})
        OutputFactory._get_list_output = backup_function
        self.assertTrue(result["n_messages"] != 0)
        self.assertTrue(len(my_lyst_output.get_list()), result["n_messages"])

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(os.path.abspath(path))
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))