# -*- coding: utf-8 -*-
from pysentimiento import create_analyzer

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule

LANG = "lang"


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "pysentimento"
        self._help = """Module to detect ironic, emotions, sentiments... in text"""
        self._author = "BorjaPintos"
        self._analyzer_sentiment = None
        self._analyzer_emotion = None
        self._analyzer_hate = None

    def _get_analyzer_sentiment(self):
        if self._analyzer_sentiment is None:
            self._analyzer_sentiment = create_analyzer(task="sentiment", lang=self._get_language_param())
        return self._analyzer_sentiment

    def _get_analyzer_emotion(self):
        if self._analyzer_emotion is None:
            self._analyzer_emotion = create_analyzer(task="emotion", lang=self._get_language_param())
        return self._analyzer_emotion

    def _get_analyzer_hate(self):
        if self._analyzer_emotion is None:
            self._analyzer_emotion = create_analyzer(task="hate_speech", lang=self._get_language_param())
        return self._analyzer_emotion

    def _get_language_param(self):
        if self.get_params() is not None and LANG in self.get_params():
            return self.get_params()[LANG]
        return "es"

    def is_valid_for(self, target_file: TargetPath):
        return False

    def _analyze_sentiment(self, text: str):
        result = {}
        analyzer = self._get_analyzer_sentiment()
        predict = analyzer.predict(text)
        result["sentiment"] = predict.output
        result["scores"] = predict.probas
        return result

    def _analyze_emotion(self, text: str):
        result = {}
        analyzer = self._get_analyzer_emotion()
        predict = analyzer.predict(text)
        result["emotion"] = predict.output
        result["scores"] = predict.probas
        return result

    def _analyze_hate(self, text: str):
        result = {}
        analyzer = self._get_analyzer_hate()
        predict = analyzer.predict(text)
        result["hate"] = predict.output
        result["scores"] = predict.probas
        return result

    def _analyze(self, text: str):
        result = {"sentiment": self._analyze_sentiment(text),
                  "emotion": self._analyze_emotion(text),
                  "hate": self._analyze_hate(text)}
        return result

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        result = {}
        if "strings" in result_of_previos_modules and "elements" in result_of_previos_modules["strings"]:
            strings = result_of_previos_modules["strings"]["elements"]
            result["strings"] = self._analyze(strings)
        if "pstostparser" in result_of_previos_modules and "messages" in result_of_previos_modules["pstostparser"]:
            for message in result_of_previos_modules["pstostparser"]["messages"]:
                if "plain_text_body" in message:
                    result["pstostparser"] = self._analyze(message["plain_text_body"])
                elif "html_body" in message:
                    result["pstostparser"] = self._analyze(message["html_body"])
        if "tikaparser" in result_of_previos_modules and "content" in result_of_previos_modules["tikaparser"]:
            content = result_of_previos_modules["tikaparser"]["content"]
            result["tikaparser"] = self._analyze(content)
        if "whisper" in result_of_previos_modules and "content" in result_of_previos_modules["whisper"]:
            content = result_of_previos_modules["whisper"]["content"]
            result["whisper"] = self._analyze(content)

        return result
