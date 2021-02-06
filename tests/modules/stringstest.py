import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.strings.main import Constructor


class StringsTest(unittest.TestCase):

    def test_string_more_than_9_characters(self):
        path = "./tests/examples/collie.jpg.zip"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {"charMin": 9})
        self.assertEqual(result, ["collie.jpg", "&AtyRf!}\x0c", "7TzYid2c<", "TJ'np'C:K\x0c", 'collie.jpg\n'])

    def test_string_more_than_5_characters(self):
        path = "./tests/examples/barcode.gif"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {"charMin": 5})
        self.assertEqual(len(result), 12)

    def test_string_more_than_8_characters(self):
        path = "./tests/examples/winexe.exe"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {"charMin": 8})
        self.assertEqual(len(result), 2072)
        self.assertEqual("!This program cannot be run in DOS mode.\r\r\n$", result[0])

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
