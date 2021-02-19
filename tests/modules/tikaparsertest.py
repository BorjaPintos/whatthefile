# -*- coding: utf-8 -*-
import unittest
from src.domain.targetfile import TargetFile
from src.modules.tikaparser.main import Constructor


class TikaParserTest(unittest.TestCase):

    def test_parser_pdf(self):
        path = "./tests/examples/EstrellaGalicia.pdf"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        #module.set_params({"tika_server_url": "http://192.168.0.13:9998"})
        result = module.run(target_file, {})
        self.assertTrue(len(result["content"]) != 0)


    def test_parser_pages(self):
        path = "./tests/examples/pages.pages"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        #module.set_params({"tika_server_url": "http://192.168.0.13:9998"})
        result = module.run(target_file, {})
        self.assertTrue(len(result["content"]) != 0)

    def test_parser_excel(self):
        path = "./tests/examples/excel.xlsx"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        #module.set_params({"tika_server_url": "http://192.168.0.13:9998"})
        result = module.run(target_file, {})
        self.assertTrue("Prueba de texto en excel" in result["content"])

    def test_parser_word(self):
        path = "./tests/examples/word.docx"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        #module.set_params({"tika_server_url": "http://192.168.0.13:9998"})
        result = module.run(target_file, {})
        self.assertTrue("Esto es un documento de work" in result["content"])

    def test_invalid_file(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
