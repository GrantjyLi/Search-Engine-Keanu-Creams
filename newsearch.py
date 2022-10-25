import json
import math
import os.path
from pagerank import pageRank
import searchdata

#Global Variables
phrase = []
queryVector =[]
basisVector =[]
queryDict ={}
csList = []
idfData = {}
pageRankData = {}

#Functions
def insert_List(csInfo):
    global csList
    list = csList
    for i in range(len(list)):
        if csInfo['score'] >= list[i]['score']:
            prev = list[0:i]
            post = list[i:]
            tempList = prev+[csInfo]+post
            return tempList
    
    return list + [csInfo]


def calc_CS(queryVector, pageVector, boost):
    global pageRankData
    numerator =0
    qEuclidNorm =0
    pEuclidNorm =0
    for i in range(len(queryVector)):
        numerator += (queryVector[i] * pageVector['score'][i])
        qEuclidNorm += queryVector[i] **2
        pEuclidNorm += pageVector['score'][i] **2
    if qEuclidNorm ==0 or pEuclidNorm ==0:
        return 0
    if boost:
        return (numerator / ((qEuclidNorm**0.5) * (pEuclidNorm**0.5)))*pageRankData[pageVector['url']]
    return numerator / ((qEuclidNorm**0.5) * (pEuclidNorm**0.5))


def fetchPageRank():
    filePath = os.path.join("pageRank", 'data.json')
    if os.path.isfile(filePath):
        data=json.load(open(filePath))
        return data


def init(input, boost):
    global phrase
    global idfData
    global pageRankData

    if boost:#Loading pagerank if nessasary
        pageRankData = fetchPageRank()
        
    phrase = input.split()
    fHand = open(os.path.join("pageFreqFiles", "IDFData.json"))
    idfData = json.load(fHand) # getting IDF values of crawled website
    fHand.close()


def populateBasisVector():
    global phrase
    global basisVector
    global queryDict
    global idfData
    for i in phrase: # adding every word in phrase to the basis vector and query dictionary
        if (i + "IDF") in idfData and idfData[i+"IDF"] != 0:
            if i not in queryDict:
                queryDict[i] =0
                basisVector.append(i)
            queryDict[i] +=1


def populateQueryVector():
    global idfData
    global phrase
    global queryVector
    global queryDict
    global basisVector
    for i in queryDict: # filling the queryVector with Term-frequency values of each word
        queryVector.append(queryDict[i]/len(phrase))
    for i in range(len(basisVector)): # making the term-frequency values of each word into TFIDF values
        queryVector[i] = math.log(1 + queryVector[i], 2) * idfData[basisVector[i] + "IDF"]


def compareScore(freqData):
    global csList
    if len(csList) ==0:
        csList+=[freqData]
    elif len(csList) < 10:
        csList = insert_List(freqData)
    elif freqData['score'] > csList[-1]['score']:
        csList.pop(-1)
        csList = insert_List(freqData)


def calculateScore(boost):
    global csList
    global pageRankData
    filepath = os.listdir("pageFreqFiles")

    for file in filepath: # grabbing json data for each file for comparison
        if file == "IDFData.json" or file == "wordPageCount.json":
            continue
        fHand = open(os.path.join("pageFreqFiles", file))
        freqData = json.load(fHand)
        fHand.close()

        pageFreqData = {'url':freqData["URL"], 'title':freqData["Title"],  'score':[]}

        for i in basisVector:
            if (i + "TFIDF") in freqData:
                pageFreqData['score'].append(freqData[i + "TFIDF"])
            else:
                pageFreqData['score'].append(0)

        pageFreqData['score'] = calc_CS(queryVector, pageFreqData,boost)
        compareScore(pageFreqData)


#Main Function
def search(input, boost):
    init(input, boost)
    populateBasisVector()
    populateQueryVector()
    calculateScore(boost)
    return csList

list = search('coconut coconut peach tomato pear banana',True)

for i in list:
    print(i)