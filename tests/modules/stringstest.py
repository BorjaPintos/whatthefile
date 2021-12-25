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
        module.set_params({"char_min": 9})
        result = module.run(target_file, {})
        self.assertEqual(result["elements"][0], "collie.jpg")
        self.assertTrue(result["n_elements"] >= 4)

    def test_string_more_than_5_characters(self):
        path = "./tests/examples/barcode.gif"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params({"char_min": 5})
        result = module.run(target_file, {})
        self.assertTrue(len(result["elements"]) >= 10)
        self.assertTrue(result["n_elements"] >= 10)

    def test_string_ignore_extensions(self):
        path = "./tests/examples/barcode.gif"
        target_file = TargetFile(path)
        module = Constructor()
        module.set_params({"char_min": 5, "ignore_extensions": ".txt,.gif"})
        self.assertFalse(module.is_valid_for(target_file))
        path = "./tests/examples/wordlist.txt"
        target_file = TargetFile(path)
        self.assertFalse(module.is_valid_for(target_file))


    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
