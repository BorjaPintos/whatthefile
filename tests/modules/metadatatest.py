import unittest

from src.domain.targetfile import TargetFile
from src.modules.metadata.main import Constructor


class MetadataTest(unittest.TestCase):

    def test_collie(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        result = module.run(target_file)
        self.assertEqual(result["Composite:ImageSize"], "200x273")

    def test_pdf(self):
        path = "./tests/examples/EstrellaGalicia.pdf"
        target_file = TargetFile(path)
        module = Constructor()
        result = module.run(target_file)
        self.assertEqual(result["PDF:Author"], "PPAEZ")
        self.assertEqual(result["PDF:Creator"], "PDFsam Basic v3.3.0")
        self.assertEqual(result["PDF:Title"], "Microsoft Word - MI-126 ESTRELLA GALICIA CERVECEROS DESDE 1906")