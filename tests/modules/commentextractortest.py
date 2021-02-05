import unittest

from src.domain.targetfile import TargetFile
from src.modules.commentextractor.main import Constructor


class CommentExtractorTest(unittest.TestCase):

    def test_code_c(self):
        collie_path = "./tests/examples/Prueba.c"
        target_file = TargetFile(collie_path)
        module = Constructor()
        result = module.run(target_file)
        print(result)
        self.assertEqual(result["codeComments_//_/**/"], ['/* comentario multilinea\n* que termina\naqui */', '//prueba de comentario', '//otro comentario'])

    def test_code_bash(self):
        path = "./tests/examples/addRoutesVPN.sh"
        target_file = TargetFile(path)
        module = Constructor()
        result = module.run(target_file)
        print(result)
        self.assertEqual(result["bashComments"], ['#!/bin/bash', '#rutas internas de la red'])

    def test_code_html(self):
        path = "./tests/examples/index.html"
        target_file = TargetFile(path)
        module = Constructor()
        result = module.run(target_file)
        print(result)
        self.assertEqual(result["htmlComments"], ["<!-- comentario\r\nmultiline de html\r\ny termina aqui -->"])

