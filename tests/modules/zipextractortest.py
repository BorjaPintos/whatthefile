import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.zipextractor.main import Constructor
import os

from src.utils.safe import Safe


class ZipExtractorTest(unittest.TestCase):

    @staticmethod
    def _remove_test_folders(output_safe_path):
        for root, dirs, files in os.walk(output_safe_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def test_unzip(self):

        output_safe_directory = "./tests/examples/safe_directory"
        Safe.safe_output_path = os.path.abspath(output_safe_directory)
        final_file = os.path.abspath("./tests/examples/safe_directory/") + \
            "/zipextractor" + \
            os.path.abspath("./tests/examples/Surprise.txt.zip/Surprise.txt").replace(":", "")

        if os.path.exists(final_file):
            os.remove(final_file)
        self._remove_test_folders(os.path.abspath(output_safe_directory))

        self.assertFalse(os.path.exists(final_file))
        path = "./tests/examples/Surprise.txt.zip"
        target_file = TargetFile(os.path.abspath(path))
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))

        result = module.run(target_file, {})
        self.assertTrue(os.path.exists(final_file))
        self.assertTrue("Surprise.txt" in result["new_files"])
        self.assertTrue(final_file in result["new_path_files"])

        os.remove(final_file)
        self._remove_test_folders(os.path.abspath(output_safe_directory))

    def test_unzip_with_password(self):

        output_safe_directory = "./tests/examples/safe_directory"
        Safe.safe_output_path = os.path.abspath(output_safe_directory)
        final_file = os.path.abspath("./tests/examples/safe_directory/") + \
            "/zipextractor" + \
            os.path.abspath("./tests/examples/Surprise2.txt.zip/Surprise2.txt").replace(":", "")

        if os.path.exists(final_file):
            os.remove(final_file)
        self._remove_test_folders(os.path.abspath(output_safe_directory))

        self.assertFalse(os.path.exists(final_file))
        path = "./tests/examples/Surprise2.txt.zip"
        target_file = TargetFile(os.path.abspath(path))
        module = Constructor()
        params = {"pwd_dict": "./tests/examples/wordlist.txt"}
        module.set_params(params)
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue("Surprise2.txt" in result["new_files"])
        self.assertTrue(final_file in result["new_path_files"])
        self.assertEqual(result["password"], "surprise")
        self.assertTrue(os.path.exists(final_file))

        os.remove(final_file)
        self._remove_test_folders(os.path.abspath(output_safe_directory))

    def test_error_password(self):
        params = {"pwd_dict": "./tests/examples/Prueba.c"}
        path = "./tests/examples/Surprise2.txt.zip"
        target_file = TargetFile(os.path.abspath(path))
        module = Constructor()
        module.set_params(params)
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertEqual("Bad password or wrong decrypted algorithm", result["error"])

    def test_unzip_with_folder_inside(self):

        output_safe_directory = "./tests/examples/safe_directory"
        Safe.safe_output_path = os.path.abspath(output_safe_directory)
        final_file = os.path.abspath("./tests/examples/safe_directory/") + \
            "/zipextractor" + \
            os.path.abspath("./tests/examples/surprise_folder.zip/surprise_folder/Surprise.txt").replace(":", "")

        if os.path.exists(final_file):
            os.remove(final_file)
        self._remove_test_folders(os.path.abspath(output_safe_directory))

        self.assertFalse(os.path.exists(final_file))
        path = "./tests/examples/surprise_folder.zip"
        target_file = TargetFile(os.path.abspath(path))
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue(os.path.exists(final_file))
        self.assertTrue("surprise_folder/Surprise.txt" in result["new_files"])
        self.assertTrue(final_file in result["new_path_files"])

        os.remove(final_file)
        self._remove_test_folders(os.path.abspath(output_safe_directory))

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
