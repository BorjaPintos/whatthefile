import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.certificatereader.main import Constructor


class CertificateReaderTest(unittest.TestCase):

    def test_default_der(self):
        path = "./tests/examples/GeoTrust Global CA.cer"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertTrue("GeoTrust Global CA" in result["issuer"])
        self.assertTrue("GeoTrust Global CA" in result["subject"])

    def test_default_pem(self):
        path = "./tests/examples/cert.pem"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertTrue("Santiago de Compostela" in result["issuer"])
        self.assertTrue("Santiago de Compostela" in result["subject"])

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
