# -*- coding: utf-8 -*-
#  importo librerias tensorflow como tfw y keras
import tensorflow as tfw
import keras
from keras.applications.inception_v3 import InceptionV3, decode_predictions
from keras import backend
from keras.preprocessing import image
import os

from modules.imodule import IModule

class Constructor(IModule):

    def __init__(self):
        self._name = "imagerecognitiontensorflow"
        self._help = """Module to predict what is the image using tensorflow"""
        self._author = "BorjaPintos"
        self._params = []


    def _getPredictions(self, imagepath):
        x= image.img_to_array(image.load_img(imagepath , target_size=(299,299)))
        #acondiciono x segun las indicaciones de tensorflow para poder trabajar con ella
        x/=255
        x-=0.5
        x*=2
        #añado otro parametro a la matriz para albelgar el tensor segun la documentacion
        x =x.reshape([1, x.shape[0], x.shape[1], x.shape[2]])
        #cargo el modelo preentrenado de ict3 si no esta en el ordenador se descargara
        ict3 = InceptionV3()
        y= ict3.predict(x)
        #imprimo por pantalla resultado de la predición
        return decode_predictions(y)


    def validFor(self, targetFile):
        if ("JPEG image data" in targetFile.getFiletype()):
            return True
        elif ("PNG image data" in targetFile.getFiletype()):
            return True
        elif ("bitmap" in targetFile.getFiletype()):
            return True
        elif ("GIF image data" in targetFile.getFiletype()):
            return True

        return False

    def generateReport(self, targetFile, params):
        predictions_response =  self._getPredictions(os.path.join(targetFile.getDirectory(),targetFile.getName()))
        predictionsDict = {}
        for campo1,redictionName,probability in predictions_response[0]:
            predictionsDict[redictionName] = str(probability)
        return predictionsDict
