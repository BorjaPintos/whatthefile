import unittest
from src.domain.targetpath import TargetPath

class TargetPathTest(unittest.TestCase):

    def test_directory(self):
        path = "./tests/examples/testdirectorydonotinsertmoreitems"
        target_path = TargetPath(path)
        self.assertEqual(target_path.get_name(), "testdirectorydonotinsertmoreitems")
        self.assertEqual(target_path.get_path(), path)
        self.assertEqual(target_path.get_directory(), "./tests/examples")
        info = target_path.get_info()
        self.assertEqual(info["st_size"], 128)
        self.assertTrue("st_atime" in info)
        self.assertTrue("st_ctime" in info)
        self.assertTrue("st_mtime" in info)


    def test_file(self):
        path = "./tests/examples/collie.jpg"
        target_path = TargetPath(path)
        self.assertEqual(target_path.get_name(), "collie.jpg")
        self.assertEqual(target_path.get_path(), path)
        self.assertEqual(target_path.get_directory(), "./tests/examples")
        info = target_path.get_info()
        self.assertEqual(info["st_size"], 19863)
        self.assertTrue("st_atime" in info)
        self.assertTrue("st_ctime" in info)
        self.assertTrue("st_mtime" in info)
