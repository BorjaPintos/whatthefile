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
        self.assertTrue("Composite:ImageSize" in result["keys"])
        #Depende de la librería instalada en el Sistema operativo, por eso puede dar dos valores
        self.assertTrue("200x273" in result["values"] or "200 273" in result["values"])

    def test_pdf(self):
        path = "./tests/examples/EstrellaGalicia.pdf"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertTrue("PDF:Author:PPAEZ" in result["key_values"])
        self.assertTrue("PDF:Creator:PDFsam Basic v3.3.0" in result["key_values"])
        self.assertTrue("PDF:Title:Microsoft Word - MI-126 ESTRELLA GALICIA CERVECEROS DESDE 1906" in result["key_values"])


    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))