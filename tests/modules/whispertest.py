# -*- coding: utf-8 -*-
import unittest
from src.domain.targetfile import TargetFile
from src.modules.whisper.main import Constructor


class WhisperTest(unittest.TestCase):

    def test_parser_aac(self):
        path = "./tests/examples/audio/test.aac"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params({"model_type": "tiny", "use_fp16": False})
        result = module.run(target_file, {})
        self.assertTrue("Niños pasar para cama pero ya" in result["content"])

    def test_parser_mp3(self):
        path = "./tests/examples/audio/test2.mp3"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        module.set_params({"model_type": "tiny", "use_fp16": False})
        result = module.run(target_file, {})
        self.assertTrue("desde vigo buenas noches" in result["content"])

    def test_invalid_file(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
