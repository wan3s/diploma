import math
from collections import Counter
from collections import defaultdict

from constants import *

def checkImportantWordsInDoc(doc, importantWords):
    for word in importantWords:
        if word not in doc:
            return False
    return True

def cosBetweenVectors (v1, v2):
    res = 0
    for i in range(min(len(v1), len(v2))):
        res += v1[i] * v2[i]
    mulRes = vectorLen(v1) * vectorLen(v2)
    if mulRes == 0:
        return 0
    res /= mulRes
    return res

def vectorLen (vector):
    res = 0
    for i in vector:
        res += i * i
    return math.sqrt(res)

def tfidfModelSearch (query, collections, termsCounter, importantWords):
    print('tfidf model')
    result = []
    for record in collections:
        queryVector = []
        docVector = []
        docCounter = record['normalized']
        queryN = sum(query.values())
        docN = sum(docCounter.values())
        if not checkImportantWordsInDoc(docCounter, importantWords):
            continue
        for word in (docCounter + query):
            idf = termsCounter[word]['idf'] if word in termsCounter else 0
            queryVector.append((query[word] / queryN) * idf)
            docVector.append((docCounter[word] / docN) * idf)
        weight = cosBetweenVectors(queryVector, docVector)
        result.append({'assoc_output': record['assoc_output'], 'weight': weight})
    return result

def vectModelSearch (query, collections, importantWords):
    print('vector model')
    result = []
    for record in collections:
        queryVector = []
        docVector = []
        docCounter = record['normalized']
        if not checkImportantWordsInDoc(docCounter, importantWords):
            continue
        for word in (docCounter + query):
            queryVector.append(query[word])
            docVector.append(docCounter[word])
        weight = cosBetweenVectors(queryVector, docVector)
        result.append({'assoc_output': record['assoc_output'], 'weight': weight})
    return result

def langModelSearch (query, collections, wordsLikelihood, lambdaCoef, importantWords):
    print('lambda =', lambdaCoef)
    result = []
    for doc in collections:
        dst = doc['normalized']
        n = len(dst)
        weight = 1
        if not checkImportantWordsInDoc(dst, importantWords):
            continue
        for term in Counter(query):
            pCol = wordsLikelihood[term]['likelihood'] if term in wordsLikelihood else WORDS_LIKELIHOOD_EPS
            pDoc = dst[term] / n if term in dst else WORDS_LIKELIHOOD_EPS
            weight *= ((1 - lambdaCoef) * pCol + lambdaCoef * pDoc)
        result.append({'assoc_output': doc['assoc_output'], 'weight': weight})
    return result

def getSearchResults (query, collections, termsCounter, importantWords, mode):
    if mode == SEARCH_MODEL_VECT:
        return vectModelSearch(query, collections, importantWords)
    if mode == SEARCH_MODEL_LANG:
        return langModelSearch(query, collections, termsCounter, LANG_MODEL_LAMBDA, importantWords)
    return tfidfModelSearch(query, collections, termsCounter, importantWords)
