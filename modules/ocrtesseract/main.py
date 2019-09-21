# -*- coding: utf-8 -*-
from PIL import Image
import pytesseract
import argparse
import cv2
import os

#acondiciono el tamaño de la imagen para ict3  la cargo desde la ruta del agumento de linea de comandos y la meto en un array en la variable x

def extractImageText(imagepath):
    image = cv2.imread(imagepath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # check to see if we should apply thresholding to preprocess the
    # image
    imageText = {}
    grayThresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # make a check to see if median blurring should be done to remove
    # noise
    grayBlur = cv2.medianBlur(gray, 3)

    imageText['Thresh'] = pytesseract.image_to_string(grayThresh)
    print (pytesseract.image_to_string(grayThresh))
    imageText['Blur'] = pytesseract.image_to_string(grayBlur)
    return imageText

def getImageText(analysingFile):
    return extractImageText(analysingFile.getCompletePath())

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
    report = {}
    report['extractedText'] = getImageText(analysingFile)
    return report
