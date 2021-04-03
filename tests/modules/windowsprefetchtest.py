import os
import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.windowsprefetch.main import Constructor


class WindowsPrefetch_Test(unittest.TestCase):

    def test_CMD(self):
        path = "./tests/examples/CMD.EXE-087B4001.pf"
        target_file = TargetFile(os.path.abspath(path))
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertEqual(result["version"], 17)
        self.assertEqual(result["executable_file_name"], "CMD.EXE")
        self.assertEqual(result["run_counts"], 2)
        self.assertEqual(result["number_of_files_accessed"], 33)
        self.assertEqual(len(result["last_run_times"]), 1)

    def test_Chrome(self):
        path = "./tests/examples/CHROME.EXE-B3BA7868.pf"
        target_file = TargetFile(os.path.abspath(path))
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertEqual(result["version"], 30)
        self.assertEqual(result["executable_file_name"], "CHROME.EXE")
        self.assertEqual(result["run_counts"], 20)
        self.assertEqual(result["number_of_files_accessed"], 282)
        self.assertEqual(len(result["last_run_times"]), 8)

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(os.path.abspath(path))
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))

