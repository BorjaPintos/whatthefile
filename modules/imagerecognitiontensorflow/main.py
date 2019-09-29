# -*- coding: utf-8 -*-
#  importo librerias tensorflow como tfw y keras
import tensorflow as tfw
import keras
from keras.applications.inception_v3 import InceptionV3, decode_predictions
from keras import backend
from keras.preprocessing import image
import os

#acondiciono el tamaño de la imagen para ict3  la cargo desde la ruta del agumento de linea de comandos y la meto en un array en la variable x

def getPredictions(imagepath):
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


def generateReportPredictions(analysingFile):
    predictions_response =  getPredictions(os.path.join(analysingFile.getDirectory(),analysingFile.getName()))
    predictionsDict = {}
    for campo1,redictionName,probability in predictions_response[0]:
        predictionsDict[redictionName] = str(probability)
    return predictionsDict

def getHelp():
	return """Module to predict what is the image using tensorflow"""

def getParams():
  return []

def validFor(analysingFile):
    if ("JPEG image data" in analysingFile.getFiletype()):
        return True
    elif ("PNG image data" in analysingFile.getFiletype()):
        return True
    elif ("bitmap" in analysingFile.getFiletype()):
        return True
    elif ("GIF image data" in analysingFile.getFiletype()):
        return True

    return False

def generateReport(analysingFile, params):
    report = generateReportPredictions(analysingFile)
    return report
