import os
import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.pstostparser.main import Constructor


class PSTOSTReaderTest(unittest.TestCase):

    def test_ost(self):
        path = "./tests/examples/nromanoff@stark-research-labs.com.pst"
        target_file = TargetFile(os.path.abspath(path))
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue('Inbox' in result["folders"])
        self.assertEqual(len(result["folders"]["Inbox"]), 527)
        self.assertTrue('Sent Items' in result["folders"])
        self.assertEqual(len(result["folders"]["Sent Items"]), 8)

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(os.path.abspath(path))
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))