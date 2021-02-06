import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.qrbcreader.main import Constructor


class QRBCReader_Test(unittest.TestCase):

    def test_QR(self):
        qr_path = "./tests/examples/qrhola.png"
        target_file = TargetFile(qr_path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertEqual(result['0'], "HOLA")

    def test_BC(self):
        bc_path = "./tests/examples/barcode.gif"
        target_file = TargetFile(bc_path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertEqual(result['0'], "1234-1234-1234")

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))

    def test_invalid_file(self):
        path = "./tests/examples/Prueba.c"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))

    def test_invalid_file2(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
