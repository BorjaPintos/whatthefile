import unittest

from src.domain.targetfile import TargetFile
from src.modules.entropy.main import Constructor


class EntropyTest(unittest.TestCase):

    def test_collie(self):
        collie_path = "./tests/examples/collie.jpg"
        target_file = TargetFile(collie_path)
        module = Constructor()
        result = module.run(target_file)
        self.assertEqual(result["shannon"], 7.959996962590177)

    def test_gun(self):
        path = "./tests/examples/gun.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        result = module.run(target_file)
        self.assertEqual(result["shannon"], 7.779575538213808)