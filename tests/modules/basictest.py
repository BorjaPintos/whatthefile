import unittest

from src.domain.targetfile import TargetFile
from src.modules.basic.main import Constructor


class BasicTest(unittest.TestCase):

    def test_run(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        result = module.run(target_file)
        self.assertEqual(result["filetype"], target_file.get_filetype())