# -*- coding: utf-8 -*-
import unittest
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.infoextractor.main import Constructor


class InfoExtractorTest(unittest.TestCase):

    def test_info(self):
        path = "./tests/examples/importantinfo.txt"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertEqual(result["emails"], ['cosa@cosa.com', 'cosita2@cosita.com', 'cosita3@pron.com'])
        self.assertEqual(result["IBANs"],
                         ['ES12 3456 7890 1234 5678 9012', 'ES1234567890123456789012', 'ES12-3456-7890-1234-5678-9011'])
        self.assertEqual(result["URLs"], ['http://google.es', 'http://facebook.com', 'ftp://localhost:2222',
                                          'mysql://host:puerto/database', 'http://iamgenmolona.com'])


    def test_with_not_info(self):
        path = "./tests/examples/Prueba.c"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertTrue("emails" not in result)
        self.assertTrue("URLs" not in result)
        self.assertTrue("IBANs" not in result)

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
