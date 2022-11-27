# -*- coding: utf-8 -*-
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
import whisper

from src.utils import auxiliar

MODEL_TYPE = "model_type"
USE_FP16 = "use_fp16"


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "whisper"
        self._help = """Module to extract transcript fom audio files (mp3, wav, aac)"""
        self._author = "BorjaPintos"
        self._model = None
        self._use_fp16 = None

    def _get_model(self):
        if self._model is None:
            self._model = whisper.load_model(self._get_model_param())
        return self._model

    def _get_model_param(self):
        if self.get_params() is not None and MODEL_TYPE in self.get_params():
            return self.get_params()[MODEL_TYPE]
        return "tiny"

    def _get_use_fp16_param(self):
        if self._use_fp16 is None:
            if self.get_params() is not None and USE_FP16 in self.get_params():
                self._use_fp16 = auxiliar.convert_to_boolean(self.get_params()[USE_FP16])
            else:
                self._use_fp16 = False
        return self._use_fp16

    def _extract_text(self, path: str):
        model = self._get_model()
        result = model.transcribe(path, fp16=self._get_use_fp16_param())
        return result["text"]

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "AAC" in target_file.get_type():
                return True
            elif " WAVE audio" in target_file.get_type():
                return True
            elif "Audio file" in target_file.get_type():
                return True
            if isinstance(target_file, TargetFile):
                if target_file.get_extension() in [".mp3", ".acc", ".wav"]:
                    return True
        return False

    def run(self, target_file: TargetFile, result_of_previous_modules: dict) -> dict:
        return {"content": self._extract_text(target_file.get_path())}
