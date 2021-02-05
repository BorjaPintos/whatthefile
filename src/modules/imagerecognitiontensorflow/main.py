# -*- coding: utf-8 -*-
#  importo librerias tensorflow como tfw y keras
from keras.applications.inception_v3 import InceptionV3, decode_predictions
from keras.preprocessing import image
import os

from src.domain.targetfile import TargetFile
from src.modules.imodule import IModule


class Constructor(IModule):

    def __init__(self):
        self._name = "imagerecognitiontensorflow"
        self._help = """Module to predict what is the image using tensorflow"""
        self._author = "BorjaPintos"
        self._params = None

    def _get_predictions(self, image_path: str):
        x = image.img_to_array(image.load_img(image_path, target_size=(299, 299)))
        # acondiciono x segun las indicaciones de tensorflow para poder trabajar con ella
        x /= 255
        x -= 0.5
        x *= 2
        # añado otro parametro a la matriz para albelgar el tensor segun la documentacion
        x = x.reshape([1, x.shape[0], x.shape[1], x.shape[2]])
        # cargo el modelo preentrenado de ict3 si no esta en el ordenador se descargara
        ict3 = InceptionV3()
        y = ict3.predict(x)
        # imprimo por pantalla resultado de la predición
        return decode_predictions(y)

    def is_valid_for(self, target_file: TargetFile):
        if "JPEG image data" in target_file.get_filetype():
            return True
        elif "PNG image data" in target_file.get_filetype():
            return True
        elif "bitmap" in target_file.get_filetype():
            return True
        elif "GIF image data" in target_file.get_filetype():
            return True
        return False

    def run(self, target_file: TargetFile, params: dict = None):
        predictions_response = self._get_predictions(target_file.get_path())
        result = {}
        for other, prediction_name, probability in predictions_response[0]:
            result[prediction_name] = str(probability)
        return result
