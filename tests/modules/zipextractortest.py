import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.zipextractor.main import Constructor
import os


class ZipExtractorTest(unittest.TestCase):

    def test_unzip(self):
        final_file = "./tests/examples/Surprise.txt"
        if os.path.exists(final_file):
            os.remove(final_file)
        self.assertFalse(os.path.exists(final_file))

        path = "./tests/examples/Surprise.txt.zip"
        params = {"pwd": "surprise"}
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params(params)
        result = module.run(target_file)
        self.assertTrue(os.path.exists(final_file))
        self.assertEqual(result["Surprise.txt"], final_file)
        os.remove(final_file)

    def test_unzip_with_password(self):
        final_file = "./tests/examples/Surprise2.txt"
        if os.path.exists(final_file):
            os.remove(final_file)
        self.assertFalse(os.path.exists(final_file))

        path = "./tests/examples/Surprise2.txt.zip"
        params = {"pwd": "surprise"}
        target_file = TargetFile(path)
        module = Constructor()
        module.set_params(params)
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertEqual(result["Surprise2.txt"], final_file)
        self.assertTrue(os.path.exists(final_file))
        os.remove(final_file)

    def test_error_password(self):
        final_file = "./tests/examples/Surprise2.txt"
        if os.path.exists(final_file):
            os.remove(final_file)
        self.assertFalse(os.path.exists(final_file))

        path = "./tests/examples/Surprise2.txt.zip"
        params = {"pwd": "surpriseaaaa"}
        target_file = TargetFile(path)
        module = Constructor()
        module.set_params(params)
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertEqual("Bad password or wrong decrypted algorithm", result["error"])

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
