import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.zipextractor.main import Constructor
import os


class ZipExtractorTest(unittest.TestCase):

    def test_unzip(self):
        params = {"extracted_output_path" : "./tests/examples/safe_directory"}
        final_file = os.path.join(params["extracted_output_path"], "Surprise.txt")

        if os.path.exists(final_file):
            os.remove(final_file)
        self.assertFalse(os.path.exists(final_file))
        path = "./tests/examples/Surprise.txt.zip"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params(params)
        result = module.run(target_file)
        self.assertTrue(os.path.exists(final_file))
        self.assertEqual(result["Surprise.txt"], final_file)
        os.remove(final_file)

    def test_unzip_with_password(self):
        params = {"extracted_output_path" : "./tests/examples/safe_directory",
                  "pwd_dict" : "./tests/examples/wordlist.txt"}
        final_file = os.path.join(params["extracted_output_path"], "Surprise2.txt")
        if os.path.exists(final_file):
            os.remove(final_file)

        self.assertFalse(os.path.exists(final_file))
        path = "./tests/examples/Surprise2.txt.zip"
        target_file = TargetFile(path)
        module = Constructor()
        module.set_params(params)
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        print(result)
        print(final_file)
        self.assertEqual(result["Surprise2.txt"], final_file)
        self.assertEqual(result["password"], "surprise")
        self.assertTrue(os.path.exists(final_file))
        os.remove(final_file)

    def test_error_password(self):
        params = {"extracted_output_path" : "./tests/examples/safe_directory",
                  "pwd_dict" : "./tests/examples/Prueba.c"}
        final_file = os.path.join(params["extracted_output_path"], "/Surprise2.txt")
        if os.path.exists(final_file):
            os.remove(final_file)
        self.assertFalse(os.path.exists(final_file))
        path = "./tests/examples/Surprise2.txt.zip"
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
