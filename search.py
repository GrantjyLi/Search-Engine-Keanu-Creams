import json
import math
import os.path
import searchdata
import crawler

def search(phrase, boost):
    phrase = phrase.split() # making phrase into an array
    queryVector =[]
    basisVector =[]
    queryDict ={}

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

    filepath = os.listdir("pageFreqFiles")
    for file in filepath:
        fHand = open(os.path.join(filepath, file))
        freqData = json.load(fHand)
        fHand.close()
        pageFreqData = [[], freqData[]]





search("kiwi kiwi lime banana banana apple apple apple", True)





