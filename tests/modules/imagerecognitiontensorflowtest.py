import unittest

from src.domain.targetfile import TargetFile
from src.modules.imagerecognitiontensorflow.main import Constructor


class ImageRecognitionTensorFlow_Test(unittest.TestCase):

    def test_collie(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue("collie" in result["prediction_names"])

    def test_gun(self):
        path = "./tests/examples/gun.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue("revolver" in result["prediction_names"])

    def test_invalid_file(self):
        path = "./tests/examples/Prueba.c"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
