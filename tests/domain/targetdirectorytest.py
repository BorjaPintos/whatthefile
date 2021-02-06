import unittest

import pytest

from src.domain.targetdirectory import TargetDirectory


class TargetDirectoryTest(unittest.TestCase):

    def test_load_from_path(self):
        path = "./tests/examples/testdirectorydonotinsertmoreitems"
        target_file = TargetDirectory(path)
        self.assertEqual(target_file.get_name(), "testdirectorydonotinsertmoreitems")
        self.assertEqual(target_file.get_path(), path)
        self.assertEqual(target_file.get_directory(), "./tests/examples")
        self.assertEqual(target_file.get_info()["n_elements"], 2)

    def test_expect_error_load_file_as_directory(self):
        directory_path = "./tests/examples/collie.jpg"
        with pytest.raises(BaseException):
            TargetDirectory(directory_path)