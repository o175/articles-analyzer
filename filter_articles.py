import nltk, re, pprint, os
from nltk import word_tokenize
from natasha import Combinator
from natasha.grammars import Person
from natasha.grammars.person import PersonObject
from yargy.interpretation import InterpretationEngine
from collections import deque

SIMILARITY_LEVEL = 0.7

def loadList():
    tuples= [tuple(word_tokenize(line.rstrip('\n').replace('ё', 'е'))) for line in open('politlist.txt')]
    return(tuples)

def fuzzyMatch(str1, str2):
    minLen = min(len(str1), len(str2))
    maxLen = max(len(str1), len(str2))
    i=0
    while (i<minLen) and( str1[i]==str2[i]):
        i=i+1
    return( i/maxLen )

def searchName(string, first_name, last_name):
    tokens = word_tokenize(string)
    history = [0, 0]
    thisHistory = [0, 0]
    for i, token in enumerate(tokens):
        thisHistory = [0, 0]
        simFirst = fuzzyMatch(token, first_name)
        simLast = fuzzyMatch(token, last_name)
        if simFirst  >= SIMILARITY_LEVEL:
            thisHistory[0]=1
            if history[1]==1:
                print('found!')
                return(True)
        if simLast  >= SIMILARITY_LEVEL:
            thisHistory[1]=1
            if history[0]==1:
                return(True)
        history = thisHistory
    return(False)

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
        

interestingNames = loadList()
for filename in os.listdir('downloads'):
    path='./downloads/'+filename
    print("started %s"%path)
    needed = False
    foundNames = set()
    with open(path, 'r+') as myfile:
        data=myfile.read()
        for person in interestingNames:
            if searchName(data, person[0], person[1])==True:
                foundNames.add("# {} {} {}".format(person[0], person[1], person[2]))
                needed = True
        if not needed:
            os.remove(path)
        else:
            for line in foundNames:
                line_prepender(path, line)
        
