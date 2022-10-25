import json
import math
import os.path
import searchdata

def search(phrase, boost):

    phrase = phrase.split() # making phrase into an array
    queryVector =[]
    basisVector =[]
    queryDict ={}
    csList = []

    fHand = open(os.path.join("pageFreqFiles", "IDFData.json"))
    idfData = json.load(fHand) # getting IDF values of crawled website
    fHand.close()

    for i in phrase: # adding every word in phrase to the basis vector and query dictionary
        if (i + "IDF") in idfData and idfData[i+"IDF"] != 0:
            if i not in queryDict:
                queryDict[i] =0
                basisVector.append(i)
            queryDict[i] +=1

    for i in queryDict: # filling the queryVector with Term-frequency values of each word
        queryVector.append(queryDict[i]/len(phrase))

    for i in range(len(basisVector)): # making the term-frequency values of each word into TFIDF values
        queryVector[i] = math.log(1 + queryVector[i], 2) * idfData[basisVector[i] + "IDF"]

#--------------------------------------------everthing below here is for creating the list of highest values

    filepath = os.listdir("pageFreqFiles")

    for file in filepath: # grabbing json data for each file for comparison
        if file == "IDFData.json" or file == "wordPageCount.json":
            continue
        fHand = open(os.path.join("pageFreqFiles", file))
        freqData = json.load(fHand)
        fHand.close()

        pageFreqData = [[], freqData["Title"], freqData["URL"]]

        for i in basisVector:
            if (i + "TFIDF") in freqData:
                pageFreqData[0].append(freqData[i + "TFIDF"])
            else:
                pageFreqData[0].append(0)

        if boost: # figuring boost stuff
            pageFreqData[0] = calc_CS(queryVector, pageFreqData[0]) * searchdata.get_page_rank(pageFreqData[2])
        else:
            pageFreqData[0] = calc_CS(queryVector, pageFreqData[0])

        if len(csList) ==0:
            csList.append(pageFreqData)
        elif len(csList) < 10:
            csList = insert_List(csList, pageFreqData)
        elif pageFreqData[0] > csList[-1][0]:
            csList.pop(-1)
            csList = insert_List(csList, pageFreqData)

    return (csList)


def insert_List(csList, csInfo):
    for i in range(len(csList)):
        if csInfo[0] >= csList[i][0]:
            return csList[0:i] + [csInfo] + csList[i:]

    return csList + [csInfo]

def calc_CS(queryVector, pageVector):
    numerator =0
    qEuclidNorm =0
    pEuclidNorm =0
    for i in range(len(queryVector)):
        numerator += queryVector[i] * pageVector[i]
        qEuclidNorm += queryVector[i] **2
        pEuclidNorm += pageVector[i] **2
    if qEuclidNorm ==0 or pEuclidNorm ==0:
        return 0

    return numerator / ((qEuclidNorm**0.5) * (pEuclidNorm**0.5))

list = search('coconut coconut peach tomato pear banana',True)

for i in list:
    print(i)