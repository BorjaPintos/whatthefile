import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.ocrtesseract.main import Constructor


class OcrTeseractTest(unittest.TestCase):

    def test_text(self):
        path = "./tests/examples/image_with_text.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        TEXT = "UN SABIO DIJO:\nNo tengas miedo de perder a\n\nquien no se siente afortunado\nde tenerte.\n"
        self.assertTrue(TEXT in result["Thresh"])
        self.assertTrue(TEXT in result["Blur"])


    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))