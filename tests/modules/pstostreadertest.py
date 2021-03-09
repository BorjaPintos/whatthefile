import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.pstostparser.main import Constructor


class PSTOSTReaderTest(unittest.TestCase):

    def test_ost(self):
        path = "./tests/examples/nromanoff@stark-research-labs.com.pst"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue('Inbox' in result)
        self.assertEqual(len(result["Inbox"]), 527)
        self.assertTrue('Sent Items' in result)
        self.assertEqual(len(result["Sent Items"]), 8)

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))