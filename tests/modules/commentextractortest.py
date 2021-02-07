# -*- coding: utf-8 -*-
import unittest
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.commentextractor.main import Constructor


class CommentExtractorTest(unittest.TestCase):

    def test_code_c(self):
        path = "./tests/examples/Prueba.c"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertEqual(result["//_/**/_comments"], ['/* comentario multilinea\n* que termina\naqui */', '//prueba de comentario', '//otro comentario'])

    def test_code_bash(self):
        path = "./tests/examples/addRoutesVPN.sh"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertEqual(result["#_comments"], ['#!/bin/bash', '#rutas internas de la red'])

    def test_code_html(self):
        path = "./tests/examples/index.html"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertEqual(result["<!--->Comments"], ["<!-- comentario\r\nmultiline de html\r\ny termina aqui -->"])

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))

