import json
import os

from pagerank import pageRank

#Global Variables
idfData = {}
pageRankData = {}


def fetchPageRank():
    global pageRankData
    filePath = os.path.join("pageRank", 'data.json')
    if os.path.isfile(filePath):
        pageRankData=json.load(open(filePath))
        filePath.close()
        return
    return -1
    

def fetchIDFData():
    global idfData
    fHand = open(os.path.join("pageFreqFiles", "IDFData.json"))
    if os.path.isfile(fHand):
        idfData = json.load(fHand)
        fHand.close()
        return
    return -1


def get_page(URL):
    return URL[URL.rfind("/")+1:len(URL)-len(".html")] + ".json"


def checkURL(URL):
    filePath = os.path.join("pageFiles", get_page(URL))
    if os.path.isfile(filePath):
        return True
    return False


def get_Links(URL, suffix):
    if checkURL(URL):
        page = get_page(URL)
        fHand = open(os.path.join("pageFiles", page))
        data = json.load(fHand)
        fHand.close()

        if len(data) == 0:
            return None
        return data[suffix]
    return None


def get_outgoing_links(URL):
    return get_Links(URL, "outgoingLinks")


def get_incoming_links(URL):
    return get_Links(URL, "incomingLinks")


def get_page_rank(URL):
    global pageRankData
    if pageRankData == {}:
        fetchPageRank()
    if URL in pageRankData:
        return pageRankData[URL]
    return -1


def get_idf(word):
    global idfData
    if idfData == {}:
        fetchIDFData()
    if word not in idfData:
        return 0
    return idfData[word + "IDF"]


def get_tf_data(URL, word, suffix):
    if checkURL(URL):
        fhand = open(os.path.join("pageFreqFiles", get_page(URL) + "TF"))
        data = json.load(fhand)
        fhand.close()
        return data[word + suffix]
    return 0


def get_tf(URL, word):
    return get_tf_data(URL, word, "TF")


def get_tf_idf(URL, word):
    return get_tf_data(URL, word, "TFIDF")

