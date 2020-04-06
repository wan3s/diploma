import pymorphy2
import math
import os


import utils

from constants import *
from collections import Counter
from collections import defaultdict
from nltk.corpus import stopwords

def noramlizeWord (word):
    morphAnalyzer = pymorphy2.MorphAnalyzer()
    word = word.lower()
    word = ''.join(filter(lambda x: x in ALLOWED_CHARS, word))
    if len(word) > 0:
        return morphAnalyzer.parse(word)[0].normal_form
    return ''

def normalizeImportantWords (importantWords):
    res_arr = []
    for word in importantWords:
        word = noramlizeWord(word)
        if len(word) > 0:
            res_arr.append(word)
    return res_arr

def normalizeDoc (doc):
    resultDoc = ''
    for word in doc.split(SPLIT_WORDS):
        noramlizedWordRes = noramlizeWord(word)
        if len(noramlizedWordRes) > 0 and noramlizedWordRes not in stopwords.words('russian'):
            resultDoc += noramlizedWordRes + SPLIT_WORDS
    resultDoc = resultDoc.strip()
    return Counter(defaultdict(list)) + Counter(resultDoc.split(SPLIT_WORDS))

def normalizeArrayOfDoc (arrayOfDocs):
    resultArray = []
    resultDict = {}
    docsNum = len(arrayOfDocs)
    for i, doc in enumerate(arrayOfDocs):
        print(str(i + 1) + ' / ' + str(docsNum))
        forNormaliztion = forOutput = doc
        if SPLIT_ASSOC in doc:
            tmp = doc.split(SPLIT_ASSOC)
            forNormaliztion = tmp[0]
            forOutput = tmp[1]
        normalizedDocRes = normalizeDoc(forNormaliztion)
        if len(normalizedDocRes) > 0:
            for key in normalizedDocRes:
                if key in resultDict:
                    resultDict[key]['tf'] += normalizedDocRes[key]
                    resultDict[key]['df'] += 1
                else:
                    resultDict[key] = {
                        'tf': normalizedDocRes[key],
                        'df': 1,
                        'idf': 0
                    }
            resultArray.append({
                'assoc_output': forOutput.strip(), 
                'normalized': normalizedDocRes
            })
        with open(INTERMEDIATE_RESULTS_FILE_NAME, "w") as tmp_file:
            tmp_file.write(str(resultArray))
    for key in resultDict:
        resultDict[key]['likelihood'] = resultDict[key]['tf'] / docsNum
        resultDict[key]['idf'] = math.log10(docsNum / resultDict[key]['df'])
    return resultArray, resultDict

def normalizeArrayOfDialogues (arrayOfDialogues):
    resultArray = []
    resultDict = {}
    dialoguesNum = len(arrayOfDialogues)
    for i, doc in enumerate(arrayOfDialogues):
        print(str(i+1) + ' / ' + str(dialoguesNum))
        normalizedDocRes = normalizeDoc(doc['src'])
        if len(normalizedDocRes) > 0:
            for key in normalizedDocRes:
                if key in resultDict:
                    resultDict[key]['tf'] += normalizedDocRes[key]
                    resultDict[key]['df'] += 1
                else:
                    resultDict[key] = {
                        'tf': normalizedDocRes[key],
                        'df': 1,
                        'idf': 0
                    }
            resultArray.append({
                'src': doc['dst'].strip(), 
                'dst': normalizedDocRes,
                'weight': 0,
            })
    for key in resultDict:
        resultDict[key]['idf'] = math.log10(dialoguesNum / resultDict[key]['df'])
    return resultArray, resultDict
