from constants import *

def writeToFile (fileName, text):
    outputFile = open(fileName, FILE_MODE_WRITE)
    outputFile.write(str(text))
    outputFile.close()

def readFromFile (fileName):
    inputFile = open(fileName, FILE_MODE_READ)
    inputText = inputFile.read()
    inputFile.close()
    return inputText