import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.metadata.main import Constructor


class MetadataTest(unittest.TestCase):

    def test_collie(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertTrue("200" in result["Composite:ImageSize"])
        self.assertTrue("273" in result["Composite:ImageSize"])

    def test_pdf(self):
        path = "./tests/examples/EstrellaGalicia.pdf"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertEqual(result["PDF:Author"], "PPAEZ")
        self.assertEqual(result["PDF:Creator"], "PDFsam Basic v3.3.0")
        self.assertEqual(result["PDF:Title"], "Microsoft Word - MI-126 ESTRELLA GALICIA CERVECEROS DESDE 1906")


    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))