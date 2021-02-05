import unittest

from src.domain.targetfile import TargetFile
from src.modules.ocrtesseract.main import Constructor


class OcrTeseract_Test(unittest.TestCase):

    def test_text(self):
        path = "./tests/examples/image_with_text.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        result = module.run(target_file)
        TEXT = "UN SABIO DIJO:\nNo tengas miedo de perder a\n\nquien no se siente afortunado\nde tenerte.\n"
        self.assertTrue(TEXT in result["Thresh"])
        self.assertTrue(TEXT in result["Blur"])
