import unittest

from src.domain.targetfile import TargetFile
from src.modules.qrbcreader.main import Constructor


class QRBCReader_Test(unittest.TestCase):

    def test_QR(self):
        qr_path = "./tests/examples/qrhola.png"
        target_file = TargetFile(qr_path)
        module = Constructor()
        result = module.run(target_file)
        self.assertEqual(result['0'], "HOLA")



    def test_BC(self):
        bc_path = "./tests/examples/barcode.gif"
        target_file = TargetFile(bc_path)
        module = Constructor()
        result = module.run(target_file)
        self.assertEqual(result['0'], "1234-1234-1234")