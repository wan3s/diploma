import os
import sys
import math
import random
from collections import Counter, defaultdict

import morph
import search
import gencollection
import utils
from constants import *

def checkCollections ():
    if ((not os.path.exists(COLLECTIONS_FILE_NAME)) or
            (not os.path.exists(TF_FILE_NAME)) or
                (PARAM_UPDATE_COLLECTIONS in sys.argv)):
        print('Обновление коллекций ...')
        if gencollection.createCollection() == -1:
            return -1
        print('Коллекции обновлены')

def getCollections ():
    if checkCollections() == -1:
        print('ОШИБКА: коллекции не прошли проверку')
        return -1
    return eval(utils.readFromFile(COLLECTIONS_FILE_NAME)), eval(utils.readFromFile(TF_FILE_NAME))


def getQuery ():
    return input('Пользователь >>> ')

def cmpKey (x):
    return x['weight']

def getAnswerForQuery (query, collections, mode):
    maxWeight = collections[0]['weight']
    if mode not in MIN_WEIGHT:
        mode = SEARCH_MODEL_TFIDF
    if maxWeight < MIN_WEIGHT[mode]:
        return maxWeight, random.choice(NOT_FOUND_ANSWERS)
    answers = []
    for record in collections:
        if (record['weight'] < maxWeight):
            break
        answers.append(record['assoc_output'])

    return maxWeight, '\n\t'.join(answers)

def main ():
    mode = ''
    argNameLen = len(PARAM_SEARCH_MODEL_ARG)
    for arg in sys.argv:
        if arg[:argNameLen] == PARAM_SEARCH_MODEL_ARG:
            mode = arg[argNameLen:]
    collections, termsCounter = getCollections()
    query = getQuery()
    while query != STOP_SESSION_KEY_WORD:
        query = morph.normalizeDoc(query)
        #print(query)
        searchResult = search.getSearchResults(query, collections, termsCounter, mode)

        if searchResult == -1:
            return
        
        searchResult = sorted(searchResult, key = cmpKey, reverse = True)
        maxWeight, answers = getAnswerForQuery(query, searchResult, mode)
        print('Бот (' + str(maxWeight) + ') >>> ' + answers)
        query = getQuery()


if __name__ == "__main__":
    main()