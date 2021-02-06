import unittest

import pytest

from src.domain.targetfile import TargetFile

class TargetFileTest(unittest.TestCase):

    def test_load_from_path(self):
        collie_path = "./tests/examples/collie.jpg"
        target_file = TargetFile(collie_path)
        self.assertEqual(target_file.get_extension(), ".jpg")
        self.assertTrue("JPEG" in target_file.get_type())
        self.assertEqual(target_file.get_name(), "collie.jpg")
        self.assertEqual(len(target_file.get_binary()), 19863)
        self.assertEqual(target_file.get_path(), collie_path)
        self.assertEqual(target_file.get_directory(), "./tests/examples")
        self.assertEqual(target_file.get_info()["extension"], target_file.get_extension())


    def test_load_without_extension(self):
        collie_path = "./tests/examples/NOEXTENSION"
        target_file = TargetFile(collie_path)
        self.assertEqual(target_file.get_extension(), "")
        self.assertTrue("ASCII" in target_file.get_type())

    def test_expect_error_load_directory_as_file(self):
        directory_path = "./tests/examples/"
        with pytest.raises(BaseException):
            TargetFile(directory_path)

    def test_load_filetype_from_binary(self):
        collie_path = "./tests/examples/collie.jpg"
        target_file = TargetFile(collie_path)
        self.assertTrue("JPEG" in TargetFile._get_filetype_from_binary(target_file.get_binary()))
