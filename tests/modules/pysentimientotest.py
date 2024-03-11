# -*- coding: utf-8 -*-
import unittest

from src.modules.analysis_pysentimiento.main import Constructor


class PySentimientoTest(unittest.TestCase):

    def test_strings(self):
        module = Constructor()
        module.set_params({"lang": "es"})
        result = module.run(None, {
            "strings": {"elements": "HOLA, bienvenido a whatthefile, esto es un test para probar el módulo"}
        })

        self.assertIsNotNone(result["strings"]["sentiment"])
        self.assertIsNotNone(result["strings"]["emotion"])
        self.assertIsNotNone(result["strings"]["hate"])

    def test_whit_more_modules(self):
        module = Constructor()
        module.set_params({"lang": "es"})
        result = module.run(None, self._get_info_modules_prev_dummy())

        self.assertIsNotNone(result["strings"]["sentiment"])
        self.assertIsNotNone(result["strings"]["emotion"])
        self.assertIsNotNone(result["strings"]["hate"])
        self.assertIsNotNone(result["tikaparser"]["sentiment"])
        self.assertIsNotNone(result["tikaparser"]["emotion"])
        self.assertIsNotNone(result["tikaparser"]["hate"])
        self.assertIsNotNone(result["whisper"]["sentiment"])
        self.assertIsNotNone(result["whisper"]["emotion"])
        self.assertIsNotNone(result["whisper"]["hate"])

    def _get_info_modules_prev_dummy(self):
        return {
            "tikaparser": {"content": """No te quiero ver aquí"""},
            "whisper": {"content": "Genial!, Lo has hecho de maravilla!"},
            "strings": {
                "elements": """las patatas fritas son la caña""",
                "n_elements": 1,
                ">=": 6
            },
        }
